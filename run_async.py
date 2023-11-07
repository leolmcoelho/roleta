import os
import time

roletas = ["popok",
           "ftv",
           "a",
           "b",
           "c",
           "d",
           "f",
           "bot"
           
           ]

# Verifica se o diretório não existe e, se não existir, cria-o
def start_roletas():
    for roleta in roletas:
        print("Iniciando o Bot ", roleta)
        diretorio =  f'tmp/{roleta}'
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
        cmd = f'python3 run.py {roleta} &'
        
        if roleta == 'bot':
            cmd = f'python3 telebot.py &'
            #print(cmd)
        os.system(cmd)
        time.sleep(5)

def kill_roletas():
    os.system('pkill python3')
    os.system('pkill chrome')


while True:
    start_roletas()  # Inicia as roletas
    time.sleep(6*60*60)  # Aguarda 6 horas (6 horas * 60 minutos * 60 segundos)
    kill_roletas()