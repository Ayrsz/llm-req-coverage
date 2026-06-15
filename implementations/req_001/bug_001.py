# Fault: off-by-one na fronteira (< em vez de <=).
# Aplica desconto em compras de exatamente R$ 100.
def calculate_final_price(value: float, customer_type: str) -> float:
    if value < 0:
        return 0.0
    if value < 100:
        return round(float(value), 2)
    if customer_type == "premium":
        return round(value * 0.90, 2)
    return round(value * 0.95, 2)
