import sys
import os

def ler_arquivo(nome_arquivo):
    """Lê o arquivo fonte .ci"""
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read().strip()
            return conteudo
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
        sys.exit(2)
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        sys.exit(2)

def analisar_sintaxe(conteudo):
    """Verifica se o conteúdo é uma constante inteira válida"""
    if not conteudo:
        return None, "Erro: Arquivo vazio"
    
    # Verifica se contém apenas dígitos (0-9)
    if not conteudo.isdigit():
        return None, f"Erro de sintaxe: '{conteudo}' não é uma constante inteira válida"
    
    return conteudo, None

def gerar_codigo_assembly(constante):
    """Gera o código assembly usando o modelo exato do modelo.s"""
    # Lê o conteúdo do modelo.s
    try:
        with open('modelo.s', 'r', encoding='utf-8') as arquivo_modelo:
            modelo = arquivo_modelo.read()
    except FileNotFoundError:
        print("Erro: Arquivo 'modelo.s' não encontrado no diretório atual.")
        sys.exit(2)
    
    # Gera a instrução mov
    instrucao_mov = f"    mov ${constante}, %rax"
    
    # Substitui o marcador no modelo pela instrução gerada
    codigo_assembly = modelo.replace("  ## saida do compilador deve ser inserida aqui", instrucao_mov)
    
    return codigo_assembly

def compilar(nome_arquivo_entrada):
    """Função principal que coordena a compilação"""
    # Passo 1: Ler o arquivo
    conteudo = ler_arquivo(nome_arquivo_entrada)
    
    # Passo 2: Verificar sintaxe
    constante, erro = analisar_sintaxe(conteudo)
    
    if erro:
        print(erro)
        return None
    
    # Passo 3: Gerar código assembly
    codigo_assembly = gerar_codigo_assembly(constante)
    
    # Cria nome do arquivo de saída
    nome_saida = os.path.splitext(nome_arquivo_entrada)[0] + '.s'
    
    try:
        # Passo 4: Escrever arquivo de saída
        with open(nome_saida, 'w', encoding='utf-8') as arquivo:
            arquivo.write(codigo_assembly)
        print(f"Arquivo assembly gerado: {nome_saida}")
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