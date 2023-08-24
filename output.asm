segment .text
global _start
_start:
    ;; push 34;;
    push 34

    ;; push 35;;
    push 35

    ;; plus ;;
    pop rax 
    pop rbx 
    add rax, rbx 
    push rax 

    ;; dump ;;
    ;; TODO: not implemented ;;

    ;; push 500;;
    push 500

    ;; push 80;;
    push 80

    ;; minus ;;
    pop rax 
    pop rbx 
    sub rax, rbx 
    push rax 

    ;; dump ;;
    ;; TODO: not implemented ;;

    mov rax, 60
    mov rdi, 29
    syscall
