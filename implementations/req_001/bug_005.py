# Fault: caso ausente (não trata "sem desconto" para value <= 100).
# Aplica desconto mesmo em compras de R$ 100 ou menos.
from decimal import Decimal, ROUND_HALF_UP


def _round2(x: Decimal) -> float:
    return float(x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def calculate_final_price(value: float, customer_type: str) -> float:
    v = Decimal(str(value))
    if v < 0:
        return 0.0
    rate = Decimal("0.90") if customer_type == "premium" else Decimal("0.95")
    return _round2(v * rate)
