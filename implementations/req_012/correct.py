from decimal import Decimal, ROUND_HALF_UP


def _round2(x: Decimal) -> float:
    return float(x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def income_tax(income: float) -> float:
    # Imposto progressivo: cada faixa tributa só a parcela dentro do intervalo.
    inc = Decimal(str(income))
    if inc < 0:
        return 0.0

    # Limites superiores das faixas (fechados na faixa de baixo).
    b1 = Decimal("2000")  # topo da faixa isenta
    b2 = Decimal("3000")  # topo da faixa 7.5%
    b3 = Decimal("4500")  # topo da faixa 15%

    tax = Decimal("0")
    # Faixa 2: parcela acima de 2000 até 3000, a 7.5%.
    if inc > b1:
        part = min(inc, b2) - b1
        tax += part * Decimal("0.075")
    # Faixa 3: parcela acima de 3000 até 4500, a 15%.
    if inc > b2:
        part = min(inc, b3) - b2
        tax += part * Decimal("0.15")
    # Faixa 4: parcela acima de 4500, a 22.5%.
    if inc > b3:
        part = inc - b3
        tax += part * Decimal("0.225")

    return _round2(tax)
