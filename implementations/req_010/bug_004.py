# Fault: constante/literal errado (arredonda para 1 casa em vez de 2).
def average_above(values: list, threshold: float) -> float:
    qualified = [x for x in values if x > threshold]
    if not qualified:
        return 0.0
    return round(sum(qualified) / len(qualified), 1)
