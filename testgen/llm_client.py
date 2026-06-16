"""Cliente LLM atrás de uma interface, para permitir mock em testes.

``LLMClient`` define o contrato (gerar texto + embeddings). ``GeminiClient`` é a
implementação real usando o SDK ``google-genai``. Qualquer objeto que satisfaça
o protocolo — incluindo um fake nos testes — pode ser injetado no pipeline.
"""

from __future__ import annotations

import time
from typing import Callable, Protocol, runtime_checkable

from . import config


@runtime_checkable
class LLMClient(Protocol):
    """Contrato mínimo que o pipeline precisa de um provedor de LLM."""

    def generate(self, system_instruction: str, prompt: str, temperature: float | None = None) -> str:
        ...

    def embed(self, text: str) -> list[float]:
        ...


# Códigos HTTP transitórios em que vale a pena tentar de novo.
_RETRYABLE_STATUS = {429, 500, 502, 503, 504}


class QuotaExhaustedError(RuntimeError):
    """Cota diária esgotada — esperar não adianta, falha rápido."""


def _is_daily_quota(exc) -> bool:
    """Detecta esgotamento de cota *diária* (vs. limite por minuto)."""
    return "PerDay" in str(exc)


def _server_retry_delay(exc) -> float | None:
    """Extrai o retryDelay sugerido pela API (RetryInfo), em segundos."""
    details = getattr(exc, "details", None) or {}
    error = details.get("error", {}) if isinstance(details, dict) else {}
    for detail in error.get("details", []):
        if "RetryInfo" in detail.get("@type", ""):
            raw = detail.get("retryDelay", "")  # ex.: "6s"
            try:
                return float(raw.rstrip("s"))
            except (ValueError, AttributeError):
                return None
    return None


class GeminiClient:
    """Implementação usando o SDK google-genai (Gemini).

    Inclui retry com backoff exponencial para erros transitórios da API
    (429 rate limit, 5xx sobrecarga), evitando que uma falha pontual derrube
    a execução inteira do experimento.
    """

    def __init__(
        self,
        api_key: str | None = None,
        generation_model: str = config.GENERATION_MODEL,
        embedding_model: str = config.EMBEDDING_MODEL,
        default_temperature: float = config.GENERATION_TEMPERATURE,
        max_retries: int = 5,
        base_delay: float = 2.0,
    ):
        from google import genai

        self._genai = genai
        self._client = genai.Client(api_key=api_key or config.get_api_key())

        self.generation_model = generation_model
        self.embedding_model = embedding_model
        self.default_temperature = default_temperature
        self.max_retries = max_retries
        self.base_delay = base_delay

    def _with_retry(self, func: Callable[[], object], label: str):
        """Executa ``func`` com retry em erros transitórios.

        - Cota diária esgotada: falha rápido (esperar não adianta).
        - Demais erros transitórios (429 por minuto, 5xx): respeita o
          ``retryDelay`` sugerido pela API, ou usa backoff exponencial.
        """
        from google.genai import errors

        for attempt in range(self.max_retries):
            try:
                return func()
            except errors.APIError as exc:
                status = getattr(exc, "code", None)

                if _is_daily_quota(exc):
                    raise QuotaExhaustedError(
                        f"[{label}] cota diária do free tier esgotada — "
                        "aguarde o reset (≈meia-noite no Pacífico) ou ative billing."
                    ) from exc

                is_last = attempt == self.max_retries - 1
                if status not in _RETRYABLE_STATUS or is_last:
                    raise

                delay = _server_retry_delay(exc) or self.base_delay * (2 ** attempt)
                print(f"  [{label}] erro {status} transitório; retry em {delay:.0f}s "
                      f"(tentativa {attempt + 1}/{self.max_retries})")
                time.sleep(delay)

    def generate(self, system_instruction: str, prompt: str, temperature: float | None = None) -> str:
        from google.genai import types

        temp = self.default_temperature if temperature is None else temperature

        def _call():
            return self._client.models.generate_content(
                model=self.generation_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=temp,
                ),
            )

        return self._with_retry(_call, label="generate").text

    def embed(self, text: str) -> list[float]:
        from google.genai import types

        def _call():
            return self._client.models.embed_content(
                model=self.embedding_model,
                contents=text,
                config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY"),
            )

        result = self._with_retry(_call, label="embed")
        return list(result.embeddings[0].values)
