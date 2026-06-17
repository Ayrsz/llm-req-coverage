# Fault: guarda ausente (dec sem o piso em 0).
# O contador pode ficar negativo, violando a invariante.


def apply_commands(start: int, commands: list) -> int:
    counter = start
    for command in commands:
        if command == "inc":
            counter += 1
        elif command == "dec":
            counter -= 1
        elif command == "double":
            counter *= 2
        elif command == "reset":
            counter = 0
    return counter
