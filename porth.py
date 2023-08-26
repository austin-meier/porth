import sys
import subprocess

from lexer import lex_file

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
        file.write("dump:\n")
        file.write("    mov     r9, -3689348814741910323\n")
        file.write("    sub     rsp, 40\n")
        file.write("    mov     BYTE [rsp+31], 10\n")
        file.write("    lea     rcx, [rsp+30]\n")
        file.write(".L2:\n")
        file.write("    mov     rax, rdi\n")
        file.write("    lea     r8, [rsp+32]\n")
        file.write("    mul     r9\n")
        file.write("    mov     rax, rdi\n")
        file.write("    sub     r8, rcx\n")
        file.write("    shr     rdx, 3\n")
        file.write("    lea     rsi, [rdx+rdx*4]\n")
        file.write("    add     rsi, rsi\n")
        file.write("    sub     rax, rsi\n")
        file.write("    add     eax, 48\n")
        file.write("    mov     BYTE [rcx], al\n")
        file.write("    mov     rax, rdi\n")
        file.write("    mov     rdi, rdx\n")
        file.write("    mov     rdx, rcx\n")
        file.write("    sub     rcx, 1\n")
        file.write("    cmp     rax, 9\n")
        file.write("    ja      .L2\n")
        file.write("    lea     rax, [rsp+32]\n")
        file.write("    mov     edi, 1\n")
        file.write("    sub     rdx, rax\n")
        file.write("    xor     eax, eax\n")
        file.write("    lea     rsi, [rsp+32+rdx]\n")
        file.write("    mov     rdx, r8\n")
        file.write("    mov     rax, 1\n")
        file.write("    syscall\n")
        file.write("    add     rsp, 40\n")
        file.write("    ret\n")
        file.write("global _start\n")
        file.write("_start:\n")

        assert COUNT_OPS == 4, "Exhaustive handling of operation in simulation"
        for op in program:
            if car(op) == OP_PUSH:
                file.write(f"    ;; push {cdr(op)};;\n")
                file.write(f"    push {cdr(op)}\n")
            elif car(op) == OP_PLUS:
                file.write(f"    ;; plus ;;\n")
                file.write(f"    pop rax\n")
                file.write(f"    pop rbx\n")
                file.write(f"    add rax, rbx\n")
                file.write(f"    push rax\n")
            elif car(op) == OP_MINUS:
                file.write(f"    ;; minus ;;\n")
                file.write(f"    pop rax\n")
                file.write(f"    pop rbx\n")
                file.write(f"    sub rbx, rax\n")
                file.write(f"    push rbx\n")
            elif car(op) == OP_DUMP:
                file.write(f"    ;; dump ;;\n")
                file.write(f"    pop rdi\n")
                file.write(f"    call dump\n")
            else:
                print(car(op))
                assert False, "unreachable"
            file.write("\n")

        file.write("    mov rax, 60\n")
        file.write("    mov rdi, 29\n")
        file.write("    syscall\n")

def usage(program: str):
    print(f"Usage: {program} <SUBCOMMAND> [ARGS]")
    print("SUBCOMMANDS: ")
    print("    sim <file>   Simulate the program (Default if no args provided)")
    print("    comp <file>  Compile the program")

def token_prompt(token: tuple) -> str:
    return f"{token[0]}:{token[1]}:{token[2]}:\t"

def parse_token_as_op(token: tuple) -> int:
    (file, line, col, word) = token
    assert COUNT_OPS == 4, "Exhaustive op handling in parse_token_as_op"
    if word == '+':
        return plus()
    elif word == '-':
        return minus()
    elif word == '.':
        return dump()
    else:
        try:
            return push(int(word))
        except ValueError as e:
            print(token_prompt(token) + str(e))
            exit(1)

def load_program_from_file(file_path: str):
   return [parse_token_as_op(token) for token in lex_file(file_path)]

def call_cmd(cmd: list[str]):
    print(' '.join(cmd))
    subprocess.call(cmd)

def uncons(coll):
    return (coll[0], coll[1:])

if __name__ == "__main__":

    output_name = "output"
    argv = sys.argv

    assert len(argv) >= 1
    (program_name, argv) = uncons(argv)       # remove program name from args list

    if len(argv) < 1:
        usage(program_name)
        print("ERROR: No subcommand provided")
        exit(1)

    (subcommand, argv) = uncons(argv)

    if subcommand == "sim":
        if len(argv) < 1:
            usage(program_name)
            print("ERROR: No file is provided for the simulation")
            exit(1)
        (program_path, argv) = uncons(argv)
        program = load_program_from_file(program_path)

        simulate_program(program)
    elif subcommand == "comp" or subcommand == "compile":
        if len(argv) < 1:
            usage(program_name)
            print("ERROR: No file is provided for the compilation")
            exit(1)
        (program_path, argv) = uncons(argv)
        program = load_program_from_file(program_path)
        compile_program(program, f"{output_name}.asm")
        call_cmd(["nasm", "-felf64", f"{output_name}.asm"])
        call_cmd(["ld", "-o", output_name, f"{output_name}.o"])
    elif subcommand == "help":
        usage(program_name)
        exit(1)
    else:
        usage(program_name)
        print(f"ERROR: unknown subcommand {subcommand}")
        exit(1)
