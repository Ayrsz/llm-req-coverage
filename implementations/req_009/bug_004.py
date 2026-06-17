from datetime import date

# Fault: constante/literal errado no sentinela (-999999 -> 0).
# Entradas inválidas passam a colidir com o caso legítimo "mesma data".
INVALID = 0


def days_between(start: str, end: str) -> int:
    try:
        d_start = date.fromisoformat(start)
        d_end = date.fromisoformat(end)
    except (ValueError, TypeError):
        return INVALID
    return (d_end - d_start).days
