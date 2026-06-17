# Fault: guarda ausente (não trata o caso de nenhum qualificado).
# Em lista vazia/sem qualificados ocorre divisao por zero em vez de 0.0.
def average_above(values: list, threshold: float) -> float:
    qualified = [x for x in values if x > threshold]
    return round(sum(qualified) / len(qualified), 2)
