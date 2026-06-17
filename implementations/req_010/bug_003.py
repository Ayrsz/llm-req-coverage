# Fault: ramo/retorno trocado (retorna a soma em vez da média).
def average_above(values: list, threshold: float) -> float:
    qualified = [x for x in values if x > threshold]
    if not qualified:
        return 0.0
    return round(sum(qualified), 2)
