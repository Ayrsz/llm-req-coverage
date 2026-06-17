# Fault: ramo/retorno trocado (regioes baratas e caras trocadas).
# "sul"/"sudeste" recebem base 20.0 e "norte"/etc recebem base 10.0.
from decimal import Decimal, ROUND_HALF_UP


def _round2(x: Decimal) -> float:
    return float(x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


_BASE_BY_REGION = {
    "sul": Decimal("20.0"),       # DEFEITO: ramo trocado (deveria ser 10.0)
    "sudeste": Decimal("20.0"),   # DEFEITO: ramo trocado (deveria ser 10.0)
    "norte": Decimal("10.0"),     # DEFEITO: ramo trocado (deveria ser 20.0)
    "nordeste": Decimal("10.0"),  # DEFEITO: ramo trocado (deveria ser 20.0)
    "centro-oeste": Decimal("10.0"),  # DEFEITO: ramo trocado (deveria ser 20.0)
}
_DEFAULT_BASE = Decimal("25.0")

_WEIGHT_THRESHOLD = Decimal("5")
_PER_KG = Decimal("2.0")
_EXPRESS_FACTOR = Decimal("1.5")


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
