# Fault: caso ausente (não trata "sem desconto" para value <= 100).
# Aplica desconto mesmo em compras de R$ 100 ou menos.
def calculate_final_price(value: float, customer_type: str) -> float:
    if value < 0:
        return 0.0
    if customer_type == "premium":
        return round(value * 0.90, 2)
    return round(value * 0.95, 2)
