# Fault: operador errado (< em vez de >).
# Seleciona os elementos abaixo do limiar em vez de acima.
def average_above(values: list, threshold: float) -> float:
    qualified = [x for x in values if x < threshold]
    if not qualified:
        return 0.0
    return round(sum(qualified) / len(qualified), 2)
