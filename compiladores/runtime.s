    # runtime.s - Rotinas de suporte corrigidas (x86_64, AT&T)
    .section .data
buffer:
    .zero 32

    .section .text
    .globl imprime_num
    .type imprime_num, @function
imprime_num:
    push %rbp
    mov %rsp, %rbp
    push %rbx
    push %rcx
    push %rdx
    push %rsi
    push %rdi

    # rdi = &buffer
    lea buffer(%rip), %rdi
    # rsi = buffer + 31 (posição final para term. nulo)
    lea 31(%rdi), %rsi
    movb $0, (%rsi)
    dec %rsi

    mov %rax, %rbx        # salva valor original em rbx
    mov $10, %rcx

    cmp $0, %rax
    jge .L_conv
    neg %rax

.L_conv:
    xor %rdx, %rdx
    div %rcx              # rax = q, rdx = rem
    add $48, %dl
    mov %dl, (%rsi)
    dec %rsi
    test %rax, %rax
    jnz .L_conv

    cmp $0, %rbx
    jge .L_finish
    movb $45, (%rsi)      # '-'
    dec %rsi

.L_finish:
    inc %rsi              # rsi -> início da string
    lea buffer(%rip), %rax
    lea 32(%rax), %rdx    # rdx = buffer + 32
    sub %rsi, %rdx        # rdx = tamanho = (buffer+32) - rsi

    mov $1, %rax          # sys_write
    mov $1, %rdi          # stdout (fd = 1)
    # rsi = ponteiro (já em rsi), rdx = tamanho
    syscall

    pop %rdi
    pop %rsi
    pop %rdx
    pop %rcx
    pop %rbx
    pop %rbp
    ret

    .globl sair
sair:
    mov $60, %rax
    xor %rdi, %rdi
    syscall
