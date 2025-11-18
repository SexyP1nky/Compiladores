import sys
import os
import re

def ler_arquivo(nome_arquivo):
    """Tenta abrir e ler o arquivo fonte .ci"""
    try:
        # Abre o arquivo no modo leitura
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            # Lê tudo e remove espaços em branco do começo e fim
            conteudo = arquivo.read().strip()
            # Mostra o que foi lido para debug
            print(f"Conteúdo lido: '{conteudo}'")
            return conteudo
    except FileNotFoundError:
        # Se o arquivo não existe, avisa e sai
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
        sys.exit(2)
    except Exception as e:
        # Outros erros genéricos de leitura
        print(f"Erro ao ler arquivo: {e}")
        sys.exit(2)

def analisar_sintaxe(conteudo):
    """Confere se o conteúdo é só número mesmo"""
    # Primeiro vê se não está vazio
    if not conteudo:
        return None, "Erro: Arquivo vazio"
    
    # Verifica se tem só dígitos de 0 a 9
    if not conteudo.isdigit():
        return None, f"Erro de sintaxe: '{conteudo}' não é uma constante inteira válida"
    
    # Opcional: não deixa número muito grande
    if len(conteudo) > 20:
        return None, f"Erro: Número muito grande (máximo 20 dígitos)"
    
    # Se passou em todas as verificações, tá certo
    return conteudo, None

def gerar_codigo_assembly(constante):
    """Monta o código assembly completo com o número"""
    # Converte a string para número inteiro
    num = int(constante)
    
    # Escolhe a instrução certa dependendo do tamanho do número
    if num <= 0x7FFFFFFF:
        # Números normais usam mov simples
        instrucao_mov = f"    mov ${num}, %rax"
    else:
        # Números muito grandes precisam de movabs
        instrucao_mov = f"    movabs ${num}, %rax"
    
    # Monta o código assembly completo com o modelo
    return f""".section .text
.globl _start
_start:
{instrucao_mov}
    call imprime_num
    call sair
.include "runtime.s"
"""

def compilar(nome_arquivo_entrada):
    """Função principal que coordena a compilação"""
    print(f"Compilando: {nome_arquivo_entrada}")
    
    # Passo 1: Ler o arquivo
    conteudo = ler_arquivo(nome_arquivo_entrada)
    
    # Passo 2: Verificar se é número válido
    constante, erro = analisar_sintaxe(conteudo)
    
    # Se deu erro na análise, mostra e para aqui
    if erro:
        print(erro)
        return None
    
    # Se chegou aqui, o número é válido
    print(f"Constante válida: {constante}")
    
    # Passo 3: Gerar o código assembly
    codigo_assembly = gerar_codigo_assembly(constante)
    
    # Cria nome do arquivo de saída (mesmo nome com .s)
    nome_saida = os.path.splitext(nome_arquivo_entrada)[0] + '.s'
    
    try:
        # Passo 4: Escrever o arquivo .s
        with open(nome_saida, 'w', encoding='utf-8') as arquivo:
            arquivo.write(codigo_assembly)
        # Avisa que deu certo
        print(f"✓ Arquivo assembly gerado: {nome_saida}")
        return nome_saida
    except Exception as e:
        # Se deu erro na escrita
        print(f"Erro ao escrever arquivo: {e}")
        return None

def main():
    """Ponto de entrada quando executa o script"""
    # Precisa receber exatamente 1 argumento além do nome do script
    if len(sys.argv) != 2:
        print("Uso: python3 compilador_ci.py <arquivo.ci>")
        sys.exit(2)
    
    # Pega o nome do arquivo que veio como argumento
    nome_arquivo = sys.argv[1]
    
    # Confere se o arquivo realmente existe
    if not os.path.exists(nome_arquivo):
        print(f"Erro: Arquivo '{nome_arquivo}' não existe!")
        sys.exit(2)
    
    # Manda compilar o arquivo
    resultado = compilar(nome_arquivo)
    
    # Verifica se a compilação deu certo
    if resultado:
        print("Compilação concluída com sucesso!")
        # Pega o nome base sem extensão
        nome_base = os.path.splitext(nome_arquivo)[0]
        
        # Mostra os próximos passos para o usuário
        print(f"\nPara montar e executar:")
        print(f"  as --64 -o {nome_base}.o {nome_base}.s")
        print(f"  ld -o {nome_base} {nome_base}.o")
        print(f"  ./{nome_base}")
        
        # Sai com código de sucesso
        sys.exit(0)
    else:
        # Compilação falhou
        print("Compilação falhou!")
        sys.exit(1)

# Isso aqui garante que o main só roda quando executa o arquivo diretamente
if __name__ == "__main__":
    main()