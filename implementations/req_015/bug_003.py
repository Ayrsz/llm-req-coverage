# Fault: ramo/retorno trocado (inc e dec invertidos).


def apply_commands(start: int, commands: list) -> int:
    counter = start
    for command in commands:
        if command == "inc":
            if counter > 0:
                counter -= 1
        elif command == "dec":
            counter += 1
        elif command == "double":
            counter *= 2
        elif command == "reset":
            counter = 0
    return counter
