Comandos usados no terminal: 
Teste corrigido- 
echo "42" > teste1.ci

# Compilar
python3 compilador_ci.py teste1.ci

# Montar e linkar
as --64 -o teste1.o teste1.s
ld -o teste1 teste1.o

# Executar
./teste1


Para testar os casos de erro- 
echo "abc" > teste2.ci
python3 compilador_ci.py teste2.ci