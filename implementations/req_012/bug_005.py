# Fault: condicao invertida na guarda de entrada (>= 0 em vez de < 0).
# Com a guarda invertida, todo rendimento valido (>= 0) retorna 0.0 e apenas
# negativos seriam tributados — o oposto do especificado.
from decimal import Decimal, ROUND_HALF_UP


def _round2(x: Decimal) -> float:
    return float(x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def income_tax(income: float) -> float:
    inc = Decimal(str(income))
    if inc >= 0:  # DEFEITO: condicao invertida (deveria ser inc < 0)
        return 0.0

    b1 = Decimal("2000")
    b2 = Decimal("3000")
    b3 = Decimal("4500")

    tax = Decimal("0")
    if inc > b1:
        part = min(inc, b2) - b1
        tax += part * Decimal("0.075")
    if inc > b2:
        part = min(inc, b3) - b2
        tax += part * Decimal("0.15")
    if inc > b3:
        part = inc - b3
        tax += part * Decimal("0.225")

    return _round2(tax)
