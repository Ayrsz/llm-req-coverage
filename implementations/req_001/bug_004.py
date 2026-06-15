# Fault: constante errada no desconto comum (0.90 em vez de 0.95).
def calculate_final_price(value: float, customer_type: str) -> float:
    if value < 0:
        return 0.0
    if value <= 100:
        return round(float(value), 2)
    if customer_type == "premium":
        return round(value * 0.90, 2)
    return round(value * 0.90, 2)
