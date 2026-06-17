from datetime import date

# Sentinela inteiro para entradas inválidas (preserva o tipo de retorno int).
INVALID = -999999


def days_between(start: str, end: str) -> int:
    try:
        # Parse estrito de ISO "YYYY-MM-DD"; datas inexistentes levantam ValueError.
        d_start = date.fromisoformat(start)
        d_end = date.fromisoformat(end)
    except (ValueError, TypeError):
        return INVALID
    # Diferença com sinal: positivo se end > start, negativo se end < start.
    return (d_end - d_start).days
