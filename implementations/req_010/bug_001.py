# Fault: fronteira/off-by-one (>= em vez de >).
# Inclui elementos iguais ao limiar, que deveriam ser descartados.
def average_above(values: list, threshold: float) -> float:
    qualified = [x for x in values if x >= threshold]
    if not qualified:
        return 0.0
    return round(sum(qualified) / len(qualified), 2)
