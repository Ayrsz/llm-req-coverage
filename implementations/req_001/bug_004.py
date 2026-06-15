# Fault: constante errada no desconto comum (0.90 em vez de 0.95).
from decimal import Decimal, ROUND_HALF_UP


def _round2(x: Decimal) -> float:
    return float(x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def calculate_final_price(value: float, customer_type: str) -> float:
    v = Decimal(str(value))
    if v < 0:
        return 0.0
    if v <= 100:
        return _round2(v)
    rate = Decimal("0.90") if customer_type == "premium" else Decimal("0.90")
    return _round2(v * rate)
