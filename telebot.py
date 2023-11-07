import telegram
import logging
import asyncio
import json
import os
import time
import traceback
# Certifique-se de ter as variáveis TOKEN e CHAT_ID em credentials.py
from credentials import TOKEN, CHAT_ID


# Crie o bot

logging.basicConfig(filename=f'tmp/bot/telegram.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def send_message(sala=None, strategy=None, numero = None, message = False):
    bot = telegram.Bot(token=TOKEN)

    async def _send_message(message='O bot pergunta qual sentido da vida!'):
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="HTML")
    num = 10
    if message == False:
        message = f"""
    {'❗❗ ENTRADA CONFIRMADA ❗❗'}

🎰<strong>SALA:</strong> ROLETA {sala.upper()}
💵<strong>ENTRAR:</strong> {strategy}
⭕️ Até uma proteção - Cobrir o zero.

👉 Entrar depois do número: {numero}

🤔 Ainda não sabe operar? <a href="https://playpix.com/affiliates/?btag=1483296_l225837">[ Aperte aqui ]</a>
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_send_message(message))


def send_gale(sala=None, strategy=None, numero = None):
    bot = telegram.Bot(token=TOKEN)

    async def _send_message(message='O bot pergunta qual sentido da vida!'):
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="HTML")
    num = 10
    message = f"""
    {'❗❗ ENTRADA CONFIRMADA ❗❗'}

🎰<strong>SALA:</strong> ROLETA {sala.upper()}
💵<strong>ENTRAR:</strong> {strategy}
⭕️ Até uma proteção - Cobrir o zero.

👉 Entrar depois do número: {numero}

🤔 Ainda não sabe operar? <a href="https://playpix.com/affiliates/?btag=1483296_l225837">[ Aperte aqui ]</a>
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_send_message(message))

def read_data(roleta, path = 'roleta'):
    with open(f'tmp/{roleta}/{path}.json', 'r', encoding='utf-8') as f:  # Use 'r' para leitura
        data = json.load(f)  # Carregue o conteúdo do arquivo JSON
    return data


def set_send_message_false(roleta, path='roleta'):
    # Lê o JSON atual do arquivo
    data = read_data(roleta)
    data['send_message'] = False

    with open(f'tmp/{roleta}/{path}.json', 'w') as f:
        json.dump(data, f, indent=4)
        
def set_gale_false(roleta, path='gale'):
    # Lê o JSON atual do arquivo
    data = read_data(roleta, path)
    data['read'] = False

    with open(f'tmp/{roleta}/{path}.json', 'w') as f:
        json.dump(data, f, indent=4)
    return True

def send_check_message(number):
    bot = telegram.Bot(token=TOKEN)

    async def _send_message(message='O bot pergunta qual sentido da vida!'):
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="HTML")
    num = 10
    message = f"{number}✅"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_send_message(message))


        

def run():
    while True:
        try:
            diretorio = 'tmp'
            arquivos = os.listdir(diretorio)
            # print(arquivos)
            # break
            for arquivo in arquivos:
                # O caminho completo para o arquivo é a junção do diretório com o nome do arquivo
                caminho_completo = os.path.join(diretorio, arquivo, 'roleta.json')
                caminho_verify = os.path.join(diretorio, arquivo, 'verify.json')
                #print(arquivo)
                
                if os.path.isfile(caminho_completo) and caminho_completo.endswith(".json"):
                    #print(arquivo)
                    data = read_data(arquivo)
                   
                    #print(data)
                    if data['send_message']:
                        logging.debug(data)
                        roulette = data['roulette']
                        aposta = data['aposta']
                        number = data['number']

                        send_message(roulette, aposta, number)
                        set_send_message_false(arquivo)
                        # break
                    try:
                        gale = read_data(arquivo, 'gale')
                        if gale['read']:
                            logging.debug(gale)
                            send_message(message=gale['text'])
                            set_gale_false(arquivo)
                    except Exception as e:
                        logging.error(e)
                        
                        
                        
                    
                 
                if os.path.isfile(caminho_verify) and caminho_verify.endswith(".json"):
                    data_verify = read_data(arquivo, 'verify')
                    if data_verify['verify']:
                        logging.debug(data_verify)
                        number = data_verify['number']
                        
                        
                time.sleep(1)
            # break
        except:
            logging.error('Failed to send message')
            traceback.print_exc()
            break


if __name__ == '__main__':
    #
    #send_message('A', '1° linha e 2° LInha ')
    # print(read_data())
    run()
