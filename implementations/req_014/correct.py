# Saldo final após uma sequência de operações.
# Saque ignorado se insuficiente; tipo desconhecido ignorado; saldo nunca negativo.


def final_balance(initial: float, operations: list) -> float:
    balance = initial
    for op_type, amount in operations:
        if op_type == "deposit":
            balance += amount
        elif op_type == "withdraw":
            # Só efetiva o saque se houver saldo suficiente (fronteira fechada).
            if amount <= balance:
                balance -= amount
        # Tipo desconhecido: operação ignorada.
    return round(balance, 2)
