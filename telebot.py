import telegram
import logging
import asyncio
import json
import os
import time
import traceback
# Certifique-se de ter as variáveis TOKEN e CHAT_ID em credentials.py
from credentials import TOKEN, CHAT_ID

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Crie o bot


def send_message(sala=None, strategy=None):
    bot = telegram.Bot(token=TOKEN)

    async def _send_message(message='O bot pergunta qual sentido da vida!'):
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="HTML")
    num = 10
    message = f"""
    {'✅'*num}

🎰<strong>SALA:</strong> Roleta {sala.upper()}
💵<strong>ENTRAR:</strong> {strategy}

{'✅'*num}
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_send_message(message))


def read_data(roleta):
    with open(f'tmp\{roleta}', 'r') as f:  # Use 'r' para leitura
        data = json.load(f)  # Carregue o conteúdo do arquivo JSON
    return data


def set_send_message_false(roleta):
    # Lê o JSON atual do arquivo
    data = read_data(roleta)
    data['send_message'] = False
    with open(f'tmp\{roleta}', 'w') as f:
        json.dump(data, f, indent=4)


def run():
    while True:
        try:
            diretorio = 'tmp'
            arquivos = os.listdir(diretorio)
            # print(arquivos)
            # break
            for arquivo in arquivos:
                # O caminho completo para o arquivo é a junção do diretório com o nome do arquivo
                caminho_completo = os.path.join(diretorio, arquivo)
                if os.path.isfile(caminho_completo) and arquivo.endswith(".json"):

                    data = read_data(arquivo)
                    if data['send_message']:
                        print(data)
                        roulette = data['roulette']
                        aposta = data['aposta']

                        send_message(roulette, aposta)
                        set_send_message_false(arquivo)
                        # break
                time.sleep(1)
            #break
        except:
            logging.error('Failed to send message')
            traceback.print_exc()
            break


if __name__ == '__main__':
    #
    # send_message('A', '1° linha e 2° LInha ')
    # print(read_data())
    run()
