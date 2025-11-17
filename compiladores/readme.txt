Comandos usados no terminal: 
Teste corrigido- # 1. Criar arquivo de teste
echo "42" > teste.ci

# 2. Compilar
python3 compilador_ci.py teste.ci

# 3. Montar e linkar
as --64 -o teste.o teste.s
ld -o teste teste.o

# 4. Executar
./teste


Para testar os casos de erro- #Teste com erro de sintaxe
echo "4a2" > erro.ci
python3 compilador_ci.py erro.ci


# Teste com arquivo inexistente
python3 compilador_ci.py nao_existe.ci
