
iota_counter = 0

def iota(reset: bool = False) -> int:
    global iota_counter
    if reset: iota_counter = 0
    counter = iota_counter
    iota_counter += 1
    return counter

OP_PUSH = iota(True)
OP_PLUS = iota()
OP_DUMP = iota()
COUNT_OPS = iota()

def push(x: int) -> tuple[int, int]:
    return (OP_PUSH, x)

def plus():
    return (OP_PLUS, )

def dump():
    return (OP_DUMP, )

def car(x: tuple) -> int:
    return x[0]

def cdr(x: tuple) -> int:
    return x[1]


def simulate_program(program):
    stack = []
    for op in program:
        assert COUNT_OPS == 3, "Exhaustive handling of operation in simulation"
        if car(op) == OP_PUSH:
            stack.append(cdr(op))
        elif car(op) == OP_PLUS:
            a = stack.pop()
            b = stack.pop()
            stack.append(a + b)
        elif car(op) == OP_DUMP:
            a = stack.pop()
            print(a)
        else:
            assert False, "Unreachable"

def compile_program(program):
    assert False, "Not implemented yet"

program = [
    push(34),
    push(35),
    plus(),
    dump()
]

simulate_program(program)

