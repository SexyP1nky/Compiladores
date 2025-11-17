#!/usr/bin/env python3
"""
Compilador CI - Constantes Inteiras
Versão corrigida
"""

import sys
import os
import re

def ler_arquivo(nome_arquivo):
    """Lê o conteúdo do arquivo fonte"""
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read().strip()
            print(f"Conteúdo lido: '{conteudo}'")
            return conteudo
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
        sys.exit(2)
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        sys.exit(2)

def analisar_sintaxe(conteudo):
    """Analisa se o conteúdo é uma constante inteira válida"""
    if not conteudo:
        return None, "Erro: Arquivo vazio"
    
    if not conteudo.isdigit():
        return None, f"Erro de sintaxe: '{conteudo}' não é uma constante inteira válida"
    
    if len(conteudo) > 20:
        return None, f"Erro: Número muito grande (máximo 20 dígitos)"
    
    return conteudo, None

def gerar_codigo_assembly(constante):
    """Gera o código assembly completo"""
    num = int(constante)
    if num <= 0x7FFFFFFF:
        instrucao_mov = f"    mov ${num}, %rax"
    else:
        instrucao_mov = f"    movabs ${num}, %rax"
    
    return f""".section .text
.globl _start
_start:
{instrucao_mov}
    call imprime_num
    call sair
.include "runtime.s"
"""

def compilar(nome_arquivo_entrada):
    """Função principal do compilador"""
    print(f"Compilando: {nome_arquivo_entrada}")
    
    conteudo = ler_arquivo(nome_arquivo_entrada)
    constante, erro = analisar_sintaxe(conteudo)
    
    if erro:
        print(erro)
        return None
    
    print(f"Constante válida: {constante}")
    
    codigo_assembly = gerar_codigo_assembly(constante)
    nome_saida = os.path.splitext(nome_arquivo_entrada)[0] + '.s'
    
    try:
        with open(nome_saida, 'w', encoding='utf-8') as arquivo:
            arquivo.write(codigo_assembly)
        print(f"✓ Arquivo assembly gerado: {nome_saida}")
        return nome_saida
    except Exception as e:
        print(f"Erro ao escrever arquivo: {e}")
        return None

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 compilador_ci.py <arquivo.ci>")
        sys.exit(2)
    
    nome_arquivo = sys.argv[1]
    
    if not os.path.exists(nome_arquivo):
        print(f"Erro: Arquivo '{nome_arquivo}' não existe!")
        sys.exit(2)
    
    resultado = compilar(nome_arquivo)
    
    if resultado:
        print("Compilação concluída com sucesso!")
        nome_base = os.path.splitext(nome_arquivo)[0]
        print(f"\nPara montar e executar:")
        print(f"  as --64 -o {nome_base}.o {nome_base}.s")
        print(f"  ld -o {nome_base} {nome_base}.o")
        print(f"  ./{nome_base}")
        sys.exit(0)
    else:
        print("Compilação falhou!")
        sys.exit(1)

if __name__ == "__main__":
    main()