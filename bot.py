import time
import asyncio
import nest_asyncio
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from bromo import Interation
import threading
import json
import telegram
from credentials import *

from telebot import send_message


class RoulleteBot(Interation):
    def __init__(self, roulette):

        chrome_options = Options()
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--log-level=3')
        service = ChromeService(executable_path='chromedriver.exe')
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.actions = ActionChains(self.driver)
        self.config = self.load_json('config.json')
        self.roulettes = self.load_json('roulettes.json')
        self.actions = ActionChains(self.driver)
        self.goto(self.config['url_principal'])
        self.roulette = roulette

        self.strategies = ''

        self.categories = {
            'column_one': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            'column_two': [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
            'column_three': [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36],
            'line_one': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
            'line_two': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
            'line_three': [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
        }

    def load_json(self, path):
        with open(path, 'r') as arquivo:
            return json.load(arquivo)

    def goto(self, url):
        self.driver.get(url)

    def login(self):
        self.click('//button[contains(@class, "sign-in")]')
        self.key('//input[@name="username"]', self.config['email'])
        time.sleep(1)
        self.key('//input[@name="password"]', self.config['senha'])
        self.key('//input[@name="password"]')
        time.sleep(3)

    async def goto_roulette(self, game=None):
        if game:
            self.roulette = game
        self.goto(self.roulettes['base_URL'] + self.roulettes[f'{self.roulette}'])
        await self.async_check_strategies([])

    async def async_check_strategies(self, sequence=[]):
        if not sequence:
            sequence.append(self.get_number())
            await asyncio.sleep(10)
            await self.async_check_strategies(sequence)
            return

        print(sequence)
        sequence_continue = False

        for category, numbers in self.categories.items():
            if all(number in numbers for number in sequence):
                if len(sequence) == self.config['sequencia_total']:
                    self.strategies = self.get_related_categories(category)
                    print(category, self.strategies)
                    await self.async_send_message(category, self.strategies)
                else:
                    sequence_continue = True

        await asyncio.sleep(10)

        if sequence_continue:
            sequence.append(self.get_number())
            await self.async_check_strategies(sequence)
        elif all(number == 0 for number in sequence):
            await self.async_check_strategies([])
        else:
            await self.async_check_strategies([sequence[-1]])

    def get_number(self):
        win_number = self.element('.board-cell .win-animation', method=By.CSS_SELECTOR, time=200)
        win_number = win_number.find_element(By.XPATH, '..')
        return int(win_number.text)

    def game_check(self):
        while True:
            pause_section_element = self.driver.find_elements(
                By.XPATH, '//button[contains(@class, "yes")]')
            if (len(pause_section_element) > 0):
                pause_section_element[0].click()
            time.sleep(2)

    def get_related_categories(self, strategies):
        categories = {
            'column_one': ['column_two', 'column_three'],
            'column_two': ['column_one', 'column_three'],
            'column_three': ['column_one', 'column_two'],
            'line_one': ['line_two', 'line_three'],
            'line_two': ['line_one', 'line_three'],
            'line_three': ['line_one', 'line_two']
        }

        category_full_names = {
            'column_one': '1ª Coluna',
            'column_two': '2ª Coluna',
            'column_three': '3ª Coluna',
            'line_one': '1ª Linha',
            'line_two': '2ª Linha',
            'line_three': '3ª Linha'
        }

        related_categories = [category_full_names.get(category, category)
                              for category in categories.get(strategies, [])]

        return f"{' e '.join(related_categories)}"

    def run(self):
        nest_asyncio.apply()  # Use nest_asyncio para permitir asyncio em threads
        asyncio.run(self.run_async())

    async def run_async(self):
        # Inicie as tarefas assíncronas em um loop de eventos
        loop = asyncio.get_event_loop()
        task1 = loop.run_in_executor(None, self.game_check)
        task2 = loop.run_in_executor(None, self.goto_roulette)

        # Aguarde a conclusão de ambas as tarefas
        await asyncio.gather(task1, task2)
    
    
    async def _send_message(self, message='O bot pergunta qual sentido da vida!'):
        self.bot = telegram.Bot(token=TOKEN)
        await self.bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="HTML")    
        
    def send_message(self, sala=None, strategy=None):        
        num = 10
        message = f"""
        {'✅'*num}

        🎰<strong>SALA:</strong> {sala}
        💵<strong>ENTRAR:</strong> {strategy}

        {'✅'*num}
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._send_message(message))





if __name__ == "__main__":
    test = RoulleteBot('a')
    # test.login()
    # threading.Thread(target=test.game_check).start()
    # threading.Thread(target=test.goto_roulette).start()
    test.run()
