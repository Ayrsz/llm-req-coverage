# Fault: constante errada no desconto premium (0.95 em vez de 0.90).
from decimal import Decimal, ROUND_HALF_UP


def _round2(x: Decimal) -> float:
    return float(x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def calculate_final_price(value: float, customer_type: str) -> float:
    v = Decimal(str(value))
    if v < 0:
        return 0.0
    if v <= 100:
        return _round2(v)
    rate = Decimal("0.95") if customer_type == "premium" else Decimal("0.95")
    return _round2(v * rate)
