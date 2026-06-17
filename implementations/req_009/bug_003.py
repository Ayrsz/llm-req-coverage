from datetime import date

# Fault: ramo/retorno trocado (retorna o valor absoluto em vez do com sinal).
# Datas com end < start passam a devolver positivo em vez de negativo.
INVALID = -999999


def days_between(start: str, end: str) -> int:
    try:
        d_start = date.fromisoformat(start)
        d_end = date.fromisoformat(end)
    except (ValueError, TypeError):
        return INVALID
    return abs((d_end - d_start).days)
