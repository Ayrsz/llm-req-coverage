def average_above(values: list, threshold: float) -> float:
    # Mantém apenas os elementos estritamente maiores que o limiar.
    qualified = [x for x in values if x > threshold]
    # Nenhum qualificado (ou lista vazia) => 0.0 por definição.
    if not qualified:
        return 0.0
    # Média aritmética arredondada a 2 casas com o round() nativo.
    return round(sum(qualified) / len(qualified), 2)
