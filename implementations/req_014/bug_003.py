# Fault: ramo/retorno trocado (deposit e withdraw invertidos).


def final_balance(initial: float, operations: list) -> float:
    balance = initial
    for op_type, amount in operations:
        if op_type == "withdraw":
            balance += amount
        elif op_type == "deposit":
            if amount <= balance:
                balance -= amount
    return round(balance, 2)
