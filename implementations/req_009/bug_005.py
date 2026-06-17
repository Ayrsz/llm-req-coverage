from datetime import date

# Fault: guarda ausente (sem o try/except que captura datas inválidas).
# Entradas inválidas levantam ValueError em vez de retornar o sentinela.
INVALID = -999999


def days_between(start: str, end: str) -> int:
    d_start = date.fromisoformat(start)
    d_end = date.fromisoformat(end)
    return (d_end - d_start).days
