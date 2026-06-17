# Fault: guarda ausente (saque sempre efetivado, mesmo sem saldo suficiente).
# O saldo pode ficar negativo, violando a invariante.


def final_balance(initial: float, operations: list) -> float:
    balance = initial
    for op_type, amount in operations:
        if op_type == "deposit":
            balance += amount
        elif op_type == "withdraw":
            balance -= amount
    return round(balance, 2)
