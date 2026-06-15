#!/usr/bin/env python3
"""Infraestrutura compartilhada de acesso ao LLM (Gemini).

Reaproveita a lógica que já funcionava no pipeline antigo de embeddings:

- carregamento automático de ``.env`` (sobe a árvore de diretórios);
- ``with_retry``: retry só quando ajuda (limite por minuto / instabilidade) e
  falha rápido em erros não recuperáveis (chave/acesso) ou cota DIÁRIA esgotada;
- cache em disco por hash do conteúdo (essencial no free tier: execuções
  interrompidas por quota retomam sem regastar requisições);
- ``generate``: uma chamada de geração de texto genérica, com cache.

Use ``build_client`` para obter um ``genai.Client`` pronto.
"""

import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

# Carrega variáveis de um .env, se existir. find_dotenv sobe a árvore a partir
# do cwd, então funciona com o .env na raiz do projeto ou em uma pasta pai.
try:
    from dotenv import find_dotenv, load_dotenv

    load_dotenv(find_dotenv(usecwd=True))
except ImportError:  # python-dotenv é opcional
    pass

try:
    from google import genai
    from google.genai import types
except ImportError:  # pragma: no cover
    sys.exit(
        "Pacote 'google-genai' não encontrado. Instale com:\n"
        "    pip install google-genai"
    )


# Erros 4xx que NÃO se resolvem com retry (acesso/chave/projeto/argumento).
NON_RETRYABLE = {400, 401, 403, 404}

DEFAULT_MODEL = "gemini-2.5-flash"


def _status_code(exc):
    m = re.match(r"\s*(\d{3})\b", str(exc))
    return int(m.group(1)) if m else None


def _parse_retry_delay(exc):
    """Extrai o retryDelay sugerido pela API (em segundos), se houver."""
    m = re.search(r"retry(?:Delay)?['\"]?:?\s*['\"]?(\d+(?:\.\d+)?)\s*s", str(exc))
    return float(m.group(1)) if m else None


def _is_daily_quota(exc):
    s = str(exc)
    return "PerDay" in s or "RequestsPerDay" in s


def with_retry(fn, *, retries=5, base_delay=2.0, max_delay=70.0):
    """Executa ``fn`` com retry, mas só quando o retry pode ajudar.

    - 4xx de acesso/argumento (403, 401, 400, 404): falha rápido com mensagem
      clara -- retry nunca resolve.
    - Cota DIÁRIA (429 PerDay): falha rápido -- não recupera em minutos.
    - Demais 429/5xx (limite por minuto, instabilidade): retry respeitando o
      retryDelay sugerido pela API quando disponível.
    """
    last_exc = None
    for attempt in range(retries):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001 - precisamos classificar a falha
            last_exc = exc
            code = _status_code(exc)

            if code in NON_RETRYABLE:
                raise RuntimeError(
                    f"Erro {code} não recuperável: {str(exc)[:300]}\n"
                    "Retry não resolve. Verifique a API key, se a Gemini API está\n"
                    "habilitada no projeto, faturamento e restrições de região."
                ) from exc

            if _is_daily_quota(exc):
                raise RuntimeError(
                    "Quota DIÁRIA do free tier esgotada para este modelo "
                    "(GenerateRequestsPerDay; ~20/dia no gemini-2.5-flash).\n"
                    "Opções:\n"
                    "  - trocar de modelo:  --model gemini-2.5-flash-lite\n"
                    "  - aguardar o reset diário (~24h)\n"
                    "O cache preserva o que já foi gerado para a próxima execução."
                ) from exc

            if attempt == retries - 1:
                break
            api_delay = _parse_retry_delay(exc)
            wait = min(api_delay or base_delay * (2 ** attempt), max_delay)
            print(
                f"  [retry {attempt + 1}/{retries}] {code or type(exc).__name__}: "
                f"aguardando {wait:.0f}s",
                file=sys.stderr,
            )
            time.sleep(wait)
    raise last_exc


# --- Cache em disco -------------------------------------------------------
# Persiste gerações por hash do conteúdo. No free tier isso é essencial: se a
# execução for interrompida por quota, ao reiniciar ela reaproveita o que já
# foi calculado em vez de gastar requisições de novo.


def cache_key(*parts):
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()


def cache_get(cache_dir, kind, key):
    if cache_dir is None:
        return None
    path = Path(cache_dir) / kind / f"{key}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def cache_put(cache_dir, kind, key, value):
    if cache_dir is None:
        return
    folder = Path(cache_dir) / kind
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{key}.json").write_text(json.dumps(value), encoding="utf-8")


def resolve_api_key(explicit=None):
    """Resolve a chave da API: argumento explícito > GEMINI_TOKEN > GEMINI_API_KEY."""
    return (
        explicit
        or os.environ.get("GEMINI_TOKEN")
        or os.environ.get("GEMINI_API_KEY")
    )


def build_client(api_key=None):
    """Cria um ``genai.Client``. Encerra com mensagem clara se faltar a chave."""
    key = resolve_api_key(api_key)
    if not key:
        sys.exit(
            "Chave da API ausente. Defina GEMINI_TOKEN / GEMINI_API_KEY no ambiente "
            "ou passe --api-key."
        )
    return genai.Client(api_key=key)


def generate(client, model, user_prompt, *, system_prompt=None, temperature=0.0,
             cache_dir=None, sleep=0.0):
    """Geração de texto genérica, com cache em disco.

    A chave de cache cobre modelo, temperatura, system_prompt e user_prompt, então
    re-rodar com os mesmos parâmetros é praticamente gratuito.
    """
    key = cache_key(
        "gen", model, f"{temperature}", system_prompt or "", user_prompt
    )
    cached = cache_get(cache_dir, "gen", key)
    if cached is not None:
        return cached["text"]

    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=temperature,
    )
    resp = with_retry(
        lambda: client.models.generate_content(
            model=model, contents=user_prompt, config=config
        )
    )
    text = resp.text
    cache_put(cache_dir, "gen", key, {"text": text})
    if sleep:
        time.sleep(sleep)
    return text
