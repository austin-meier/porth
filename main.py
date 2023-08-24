import sys
import subprocess

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

    assert COUNT_OPS == 4, "Exhaustive handling of operation in simulation"
    for op in program:
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


def compile_program(program, out_file_path: str):
    with open(out_file_path, "w") as file:
        file.write("segment .text\n")
        file.write("global _start\n")
        file.write("_start:\n")

        assert COUNT_OPS == 4, "Exhaustive handling of operation in simulation"
        for op in program:
            if car(op) == OP_PUSH:
                file.write(f"    ;; push {cdr(op)};;\n")
                file.write(f"    push {cdr(op)}\n")
            elif car(op) == OP_PLUS:
                file.write(f"    ;; plus ;;\n")
                file.write(f"    pop rax \n")
                file.write(f"    pop rbx \n")
                file.write(f"    add rax, rbx \n")
                file.write(f"    push rax \n")
            elif car(op) == OP_MINUS:
                file.write(f"    ;; minus ;;\n")
                file.write(f"    pop rax \n")
                file.write(f"    pop rbx \n")
                file.write(f"    sub rax, rbx \n")
                file.write(f"    push rax \n")
            elif car(op) == OP_DUMP:
                file.write(f"    ;; dump ;;\n")
                file.write(f"    ;; TODO: not implemented ;;\n")
            else:
                print(car(op))
                assert False, "unreachable"
            file.write("\n")

        file.write("    mov rax, 60\n")
        file.write("    mov rdi, 29\n")
        file.write("    syscall\n")

def print_usage():
    print("Usage: porth <SUBCOMMAND> [ARGS]")
    print("SUBCOMMANDS: ")
    print("    sim    Simulate the program (Default if no args provided)")
    print("    comp   Compile the program")
    return

def call_cmd(cmd: list[str]):
    print(' '.join(cmd))
    subprocess.call(cmd)

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
    output_name = "output"

    if len(sys.argv) > 1:
        subcommand = sys.argv[1].lower()
    else:
        subcommand = default_subcommand

    if subcommand == "sim":
        simulate_program(program)
    elif subcommand == "comp" or subcommand == "compile":
        compile_program(program, f"{output_name}.asm")
        call_cmd(["nasm", "-felf64", f"{output_name}.asm"])
        call_cmd(["ld", "-o", output_name, f"{output_name}.o"])
    elif subcommand == "help":
        print_usage()
        exit(1)
    else:
        print_usage()
        print(f"ERROR: unknown subcommand {subcommand}")
        exit(1)
