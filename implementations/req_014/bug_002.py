# Fault: operador errado (deposit subtrai em vez de somar).


def final_balance(initial: float, operations: list) -> float:
    balance = initial
    for op_type, amount in operations:
        if op_type == "deposit":
            balance -= amount
        elif op_type == "withdraw":
            if amount <= balance:
                balance -= amount
    return round(balance, 2)
