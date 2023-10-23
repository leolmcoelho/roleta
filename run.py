import sys
from bot2 import RoulleteBot
print(sys.argv[1])
# Crie uma instância do bot com base no argumento fornecido
r = RoulleteBot(sys.argv[1])
r.run()
