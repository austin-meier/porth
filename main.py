import sys

iota_counter = 0

def iota(reset: bool = False) -> int:
    global iota_counter
    if reset: iota_counter = 0
    counter = iota_counter
    iota_counter += 1
    return counter

OP_PUSH = iota(True)
OP_PLUS = iota()
OP_MINUS = iota()
OP_DUMP = iota()
COUNT_OPS = iota()

def push(x: int) -> tuple[int, int]:
    return (OP_PUSH, x)

def plus():
    return (OP_PLUS, )

def minus():
    return (OP_MINUS, )

def dump():
    return (OP_DUMP, )

def car(x: tuple) -> int:
    return x[0]

def cdr(x: tuple) -> int:
    return x[1]


def simulate_program(program):
    stack = []
    for op in program:
        assert COUNT_OPS == 4, "Exhaustive handling of operation in simulation"
        if car(op) == OP_PUSH:
            stack.append(cdr(op))
        elif car(op) == OP_PLUS:
            a = stack.pop()
            b = stack.pop()
            stack.append(a + b)
        elif car(op) == OP_MINUS:
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)
        elif car(op) == OP_DUMP:
            a = stack.pop()
            print(a)
        else:
            assert False, "Unreachable"


def compile_program(program):
    assert False, "Not implemented yet"

def print_usage():
    print("Usage: porth <SUBCOMMAND> [ARGS]")
    print("SUBCOMMANDS: ")
    print("    sim    Simulate the program (Default if no args provided)")
    print("    comp   Compile the program")
    return

program = [
    push(34),
    push(35),
    plus(),
    dump(),
    push(500),
    push(80),
    minus(),
    dump()
]

if __name__ == "__main__":

    default_subcommand = "sim"

    if len(sys.argv) > 1:
        subcommand = sys.argv[1].lower()
        print("TEST")
    else:
        subcommand = default_subcommand

    if subcommand == "sim":
        simulate_program(program)
    elif subcommand == "comp" or subcommand == "compile":
        compile_program(program)
    elif subcommand == "help":
        print_usage()
        exit(1)
    else:
        print_usage()
        print(f"ERROR: unknown subcommand {subcommand}")
        exit(1)