# Fault: constante/literal errado (arredonda para 1 casa em vez de 2).


def final_balance(initial: float, operations: list) -> float:
    balance = initial
    for op_type, amount in operations:
        if op_type == "deposit":
            balance += amount
        elif op_type == "withdraw":
            if amount <= balance:
                balance -= amount
    return round(balance, 1)
