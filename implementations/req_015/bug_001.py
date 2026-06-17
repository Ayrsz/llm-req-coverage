# Fault: fronteira/off-by-one (>= em vez de >).
# Permite decrementar quando counter == 0, gerando -1 (viola o piso).


def apply_commands(start: int, commands: list) -> int:
    counter = start
    for command in commands:
        if command == "inc":
            counter += 1
        elif command == "dec":
            if counter >= 0:
                counter -= 1
        elif command == "double":
            counter *= 2
        elif command == "reset":
            counter = 0
    return counter
