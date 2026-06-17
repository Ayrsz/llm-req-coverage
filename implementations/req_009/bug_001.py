from datetime import date, timedelta

# Fault: fronteira/off-by-one no resultado (soma 1 dia ao delta correto).
# days_between(d, d) retorna 1 em vez de 0; toda diferença fica deslocada em +1.
INVALID = -999999


def days_between(start: str, end: str) -> int:
    try:
        d_start = date.fromisoformat(start)
        d_end = date.fromisoformat(end)
    except (ValueError, TypeError):
        return INVALID
    return (d_end - d_start).days + 1
