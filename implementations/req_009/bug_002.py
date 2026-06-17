from datetime import date

# Fault: operador errado (start - end em vez de end - start).
# Inverte o sinal: diferenças positivas viram negativas e vice-versa.
INVALID = -999999


def days_between(start: str, end: str) -> int:
    try:
        d_start = date.fromisoformat(start)
        d_end = date.fromisoformat(end)
    except (ValueError, TypeError):
        return INVALID
    return (d_start - d_end).days
