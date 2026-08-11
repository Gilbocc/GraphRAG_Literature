"""OpenRouter-backed clients.

OpenRouter is OpenAI-schema-compatible on both /chat/completions and /embeddings,
so neo4j-graphrag's OpenAILLM / OpenAIEmbeddings work by overriding base_url.
Both surfaces authenticate with the same OPENROUTER_API_KEY.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any, TypeVar

import neo4j
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from neo4j_graphrag.llm import OpenAILLM
from openai import OpenAI
from pydantic import BaseModel, ValidationError

from ..config import OPENROUTER_BASE_URL, Config, provider_routing

log = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


def neo4j_driver(cfg: Config) -> neo4j.Driver:
    driver = neo4j.GraphDatabase.driver(
        cfg.neo4j_uri, auth=(cfg.neo4j_user, cfg.neo4j_password)
    )
    driver.verify_connectivity()
    return driver


def embedder(cfg: Config) -> OpenAIEmbeddings:
    """neo4j-graphrag Embedder; kwargs are forwarded to openai.OpenAI."""
    return OpenAIEmbeddings(
        model=cfg.embedding_model,
        api_key=cfg.openrouter_api_key,
        base_url=OPENROUTER_BASE_URL,
    )


def graphrag_llm(cfg: Config) -> OpenAILLM:
    """neo4j-graphrag LLM used for answer generation in GraphRAG pipelines."""
    extra_body: dict[str, Any] = {}
    if cfg.llm_reasoning_effort:
        extra_body["reasoning"] = {"effort": cfg.llm_reasoning_effort}
    routing = provider_routing(cfg)
    if routing:
        extra_body["provider"] = routing
    # The timeout matters as much here as on the extraction client: a request
    # with none blocks forever, and an answer that never returns is
    # indistinguishable from a slow one. **kwargs reaches the underlying
    # OpenAI client.
    return OpenAILLM(
        model_name=cfg.llm_model,
        model_params={"temperature": 0.0, "extra_body": extra_body or None},
        api_key=cfg.openrouter_api_key,
        base_url=OPENROUTER_BASE_URL,
        timeout=cfg.llm_timeout,
        max_retries=2,
    )


def raw_client(cfg: Config) -> OpenAI:
    """Plain OpenAI client pointed at OpenRouter, for structured extraction."""
    return OpenAI(
        api_key=cfg.openrouter_api_key,
        base_url=OPENROUTER_BASE_URL,
        timeout=cfg.llm_timeout,
        max_retries=2,
    )


# A call slower than this is worth a line of its own: normal calls land in a
# few seconds, so anything past this is contention, a retry, or a stall.
SLOW_CALL_SECONDS = 20.0


class StructuredLLM:
    """Calls OpenRouter and validates the reply against a Pydantic model.

    Tries native json_schema structured output first; falls back to json_object
    plus an embedded schema, since not every OpenRouter-routed model supports
    json_schema. A validation failure is retried once with the error fed back.
    """

    def __init__(self, cfg: Config) -> None:
        self.client = raw_client(cfg)
        self.calls = 0
        self.seconds = 0.0
        self.model = cfg.llm_model
        self.max_tokens = cfg.llm_max_tokens
        self.extra_body: dict[str, Any] = {}
        if cfg.llm_reasoning_effort:
            # OpenRouter-wide reasoning control; ignored by non-reasoning models.
            self.extra_body["reasoning"] = {"effort": cfg.llm_reasoning_effort}
        routing = provider_routing(cfg)
        if routing:
            self.extra_body["provider"] = routing

    def parse(self, system: str, user: str, schema: type[T], *, max_retries: int = 2) -> T:
        """Call the model and validate the reply, timing every attempt.

        Timing lives here because it is the only place every call passes
        through. Without it, a pass that takes twenty minutes is indistinguisha-
        ble from one that is stuck, and both look like silence.
        """
        started = time.monotonic()
        json_schema = schema.model_json_schema()
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
        last_error: Exception | None = None

        for attempt in range(max_retries + 1):
            use_native = attempt == 0
            kwargs = {}
            if use_native:
                kwargs["response_format"] = {
                    "type": "json_schema",
                    "json_schema": {
                        "name": schema.__name__,
                        "strict": False,
                        "schema": json_schema,
                    },
                }
            else:
                kwargs["response_format"] = {"type": "json_object"}
                messages = messages[:2] + [
                    {
                        "role": "user",
                        "content": (
                            "Reply with a single JSON object conforming to this JSON Schema. "
                            "No prose, no markdown fences.\n"
                            f"{json.dumps(json_schema)}"
                            + (f"\n\nYour previous reply failed validation: {last_error}"
                               if last_error else "")
                        ),
                    }
                ]

            try:
                resp = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.0,
                    max_tokens=self.max_tokens,
                    extra_body=self.extra_body or None,
                    **kwargs,
                )
                choice = resp.choices[0]
                if choice.finish_reason == "length":
                    raise ValueError(
                        f"response hit max_tokens ({self.max_tokens}); raise LLM_MAX_TOKENS"
                    )
                content = choice.message.content or ""
                parsed = schema.model_validate_json(_strip_fences(content))
                elapsed = time.monotonic() - started
                self.calls += 1
                self.seconds += elapsed
                if elapsed > SLOW_CALL_SECONDS:
                    log.warning("slow %s: %.1fs (%d prompt chars, %s completion "
                                "tokens, attempt %d)", schema.__name__, elapsed,
                                len(system) + len(user),
                                getattr(resp.usage, "completion_tokens", "?"),
                                attempt + 1)
                else:
                    log.debug("%s in %.1fs", schema.__name__, elapsed)
                return parsed
            except (ValidationError, json.JSONDecodeError, ValueError) as exc:
                last_error = exc
                log.warning("Structured parse failed (attempt %d): %s", attempt + 1, exc)
            except Exception as exc:  # transport / unsupported response_format
                last_error = exc
                log.warning("LLM call failed (attempt %d): %s", attempt + 1, exc)

        log.error("%s failed after %d attempts in %.1fs",
                  schema.__name__, max_retries + 1, time.monotonic() - started)
        raise RuntimeError(f"Could not get valid {schema.__name__} from model: {last_error}")


def _strip_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3]
    return text.strip()
