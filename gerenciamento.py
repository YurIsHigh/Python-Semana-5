# SEM with:
f = open("dados.txt", "r")
try:
    conteudo = f.read()
finally:
    f.close()

# COM with:
with open("dados.txt", "r", encoding="utf-8") as f:
    conteudo = f.read() # arquivo fechado automaticamente