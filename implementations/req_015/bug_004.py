# Fault: constante/literal errado (reset zera para 1 em vez de 0).


def apply_commands(start: int, commands: list) -> int:
    counter = start
    for command in commands:
        if command == "inc":
            counter += 1
        elif command == "dec":
            if counter > 0:
                counter -= 1
        elif command == "double":
            counter *= 2
        elif command == "reset":
            counter = 1
    return counter
