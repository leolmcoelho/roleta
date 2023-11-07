import time
import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
import traceback
from bromo import Interation
import threading
import json
import sys
import platform
import logging


class RoulleteBot(Interation):

    verify = False
    history_sequence = []
    category = ''

    def __init__(self, roulette):

        self.roulette = roulette
        # self.driver = webdriver.Firefox()
        logging.basicConfig(
            filename=f'tmp/{roulette}/chrome.log', level=logging.WARNING,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.make_log()
        chrome_options = Options()

        if platform.system() == "Windows":
            # Se for Windows, use o executável 'chromedriver.exe'
            chrome_driver_path = 'chromedriver.exe'
        else:
            chrome_options.binary_location = '/usr/bin/google-chrome'  # Caminho para o Google Chrome
            # Se for outro sistema operacional, defina o caminho apropriado
            chrome_driver_path = "/root/app/chromedriver"
            chrome_options.add_argument('--headless')

        chrome_options.add_argument('--log-level=WARN')
        chrome_options.add_argument("--silent")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        service = ChromeService(executable_path=chrome_driver_path)
        service.port = self.roulettes[roulette]['port']

        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.logger.info("WebDriver Iniciado")
        self.actions = ActionChains(self.driver)

        self.actions = ActionChains(self.driver)
        self.goto(self.config['url_principal'])
        self.strategys = ''

        self.categories = {
            'column_one': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            'column_two': [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
            'column_three': [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36],
            'line_one': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
            'line_two': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
            'line_three': [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
        }

        self.logger.info('A execução do Bot começou')

    def load_json(self, path):
        with open(path, 'r') as arquivo:
            return json.load(arquivo)

    def goto(self, url):
        self.driver.get(url)

    def make_log(self):
        logger = logging.getLogger(self.roulette)
        logger.setLevel(logging.DEBUG)

        self.config = self.load_json('config.json')
        self.roulettes = self.load_json('roulettes.json')
        file_handler = logging.FileHandler(f'tmp/{self.roulette}/app.log')
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        self.logger = logger

    def login(self):
        self.click('//button[contains(@class, "sign-in")]')
        self.key('//input[@name="username"]', self.config['email'])
        time.sleep(1)
        self.key('//input[@name="password"]', self.config['senha'])
        self.key('//input[@name="password"]')
        time.sleep(3)

    def goto_roulette(self, game=None):
        # self.goto_roulettes()
        if game:
            self.roulette = game
        self.goto(self.roulettes['base_URL'] + self.roulettes[f'{self.roulette}']['link'])
        self.check_strategies([])

    

    def check_strategies(self, sequence=[]):
        # print(self.history_sequence)
        if not sequence:
            number = self.get_number()
            sequence.append(number)
            self.check_strategies(sequence)
            return

        self.logger.info(sequence)
        sequence_continue = False

        if self.verify:
            txt = '❌'
            
            ultimo_numero = self.history_sequence[-1]
            if ultimo_numero not in self.categories[self.category]:
                txt = '✅'
            data = {
                "text": f'{txt}{ultimo_numero}',
                'read': True
            }                      
           
            json_file_path = f'tmp/{self.roulette}/gale.json'

            with open(json_file_path, 'w', encoding='utf-8') as arquivo:
                json.dump(data, arquivo, ensure_ascii=False)

           
            self.history_sequence = []
            self.verify = False

        for category, numbers in self.categories.items():

            if all(number in numbers for number in sequence):
                number = sequence[-1]

                if len(sequence) == self.config['sequencia_total']:
                    self.strategies = self.get_related_categories(category)
                    self.logger.debug(f'{category}, {self.strategies}')
                    data = {
                        'send_message': True,
                        'roulette': self.roulette,
                        'aposta': self.strategies,
                        'number': number,
                        'sequence': sequence,
                        'category': category
                    }
                    self.category = category
                    self.verify = True
                    print('transfornmou o verify em true')
                    print('A sequencia é', sequence)
                    self.set_data(data)
                    self.history_sequence = sequence

                else:
                    sequence_continue = True

        time.sleep(10)
        number = self.get_number()
        print('numero atual pego', number)
        if sequence_continue:
            sequence.append(number)
            self.check_strategies(sequence)
        elif all(number == 0 for number in sequence):
            self.check_strategies([])
        else:

            self.history_sequence.append(number)
            self.check_strategies([sequence[-1]])

            # self.history_sequence =self.history_sequence + sequence

    def get_number(self, max_attempts=5):
        number = None
        attempts = 0

        _time = 2

        while attempts < max_attempts:
            try:
                # Localize o elemento com a classe '.board-cell .win-animation' usando CSS_SELECTOR
                win_number = self.element('.board-cell .win-animation',
                                          method=By.CSS_SELECTOR, time=200)
                win_number = win_number.find_element(By.XPATH, '..')
                number = int(win_number.text)

                # Registre o número em um arquivo de texto
                with open(r'tmp/numeros.txt', 'a') as arquivo:
                    arquivo.write(str(number) + '\n')

                return number  # Retorna o número obtido com sucesso

            except NoSuchElementException as e:
                # Lidar com o caso em que o elemento não é encontrado
                self.logger.info(f'Elemento não encontrado: {e}')
                attempts += 1
                time.sleep(_time)  # Aguarda um pouco antes de tentar novamente

            except NoSuchWindowException as e:
                # Lidar com o caso em que o elemento não é encontrado
                self.logger.info(f'Elemento não encontrado: {e}')
                attempts += 1
                exit()
                # Aguarda um pouco antes de tentar novamente

            except ValueError as e:
                # Lidar com o caso em que o texto do elemento não pode ser convertido em um número
                self.logger.info(f'Valor não pode ser convertido em número: {e}')
                attempts += 1
                time.sleep(_time)  # Aguarda um pouco antes de tentar novamente

            except Exception as e:
                # Lidar com outras exceções
                self.logger.error(f'Exceção não tratada: {e}')
                attempts += 1
                time.sleep(_time)  # Aguarda um pouco antes de tentar novamente

        return number

    def game_check(self):
        while True:
            pause_section_element = self.driver.find_elements(
                By.XPATH, '//button[contains(@class, "yes")]')
            if (len(pause_section_element) > 0):
                pause_section_element[0].click()
            time.sleep(2)

    def set_data(self, data):
        if not os.path.exists('tmp'):
            os.makedirs('tmp')
        with open(f'tmp/{self.roulette}/roleta.json', 'w') as f:
            f.write(json.dumps(data))

    def get_related_categories(self, strategys):

        categories = {
            'column_one': ['column_two', 'column_three'],
            'column_two': ['column_one', 'column_three'],
            'column_three': ['column_one', 'column_two'],
            'line_one': ['line_two', 'line_three'],
            'line_two': ['line_one', 'line_three'],
            'line_three': ['line_one', 'line_two']
        }

        category_full_names = {
            'column_one': '1ª Duzia',
            'column_two': '2ª Duzia',
            'column_three': '3ª Duzia',
            'line_one': '1ª Coluna',
            'line_two': '2ª Coluna',
            'line_three': '3ª Coluna'
        }

        related_categories = [category_full_names.get(category, category)
                              for category in categories.get(strategys, [])]

        return f"{' e '.join(related_categories)}"

    def run(self):

        threading.Thread(target=self.game_check).start()
        threading.Thread(target=self.goto_roulette).start()


    def run_teste(self):
        pass
        

if __name__ == "__main__":
    test = RoulleteBot('a')
    # test.login()
    # threading.Thread(target=test.game_check).start()
    # threading.Thread(target=test.goto_roulette).start()
    test.run()
