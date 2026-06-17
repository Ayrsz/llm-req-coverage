# Fault: constante/literal errado (fator expresso 2.0 em vez de 1.5).
# A modalidade expressa dobra o subtotal em vez de acrescentar 50%.
from decimal import Decimal, ROUND_HALF_UP


def _round2(x: Decimal) -> float:
    return float(x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


_BASE_BY_REGION = {
    "sul": Decimal("10.0"),
    "sudeste": Decimal("10.0"),
    "norte": Decimal("20.0"),
    "nordeste": Decimal("20.0"),
    "centro-oeste": Decimal("20.0"),
}
_DEFAULT_BASE = Decimal("25.0")

_WEIGHT_THRESHOLD = Decimal("5")
_PER_KG = Decimal("2.0")
_EXPRESS_FACTOR = Decimal("2.0")     # DEFEITO: deveria ser 1.5


def shipping_cost(weight: float, region: str, express: bool) -> float:
    w = Decimal(str(weight))
    if w <= 0:
        return 0.0

    base = _BASE_BY_REGION.get(region, _DEFAULT_BASE)

    excess = w - _WEIGHT_THRESHOLD
    if excess > 0:
        base += excess * _PER_KG

    if express:
        base *= _EXPRESS_FACTOR

    return _round2(base)
