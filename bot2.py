import time, os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

from bromo import Interation
import threading
import json
import platform


class RoulleteBot(Interation):
    def __init__(self, roulette):
        # self.driver = webdriver.Firefox()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--log-level=3')
        if platform.system() == "Windows":
            # Se for Windows, use o executável 'chromedriver.exe'
            chrome_driver_path = 'chromedriver.exe'
        else:
            # Se for outro sistema operacional, defina o caminho apropriado
            chrome_driver_path = "/usr/local/bin/chromedriver"
            
        service = ChromeService(executable_path=chrome_driver_path)
        self.driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=chrome_options
        )
        #self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        self.actions = ActionChains(self.driver)
        self.config = self.load_json('config.json')
        self.roulettes = self.load_json('roulettes.json')
        self.actions = ActionChains(self.driver)
        self.goto(self.config['url_principal'])
        self.roulette = roulette

        self.strategys = ''

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

    def goto_roulette(self, game=None):
        # self.goto_roulettes()
        if game:
            self.roulette = game
        self.goto(self.roulettes['base_URL'] + self.roulettes[f'{self.roulette}'])
        self.check_strategies([])

    def check_strategies(self, sequence=[]):
        if not sequence:
            sequence.append(self.get_number())
           
            self.check_strategies(sequence)
            return

        print(sequence)
        sequence_continue = False

        for category, numbers in self.categories.items():
            if all(number in numbers for number in sequence):
                if len(sequence) == self.config['sequencia_total'] or True:
                    self.strategies = self.get_related_categories(category)
                    print(category, self.strategies)
                    data = {
                        'send_message': True,
                        'roulette': self.roulette,
                        'aposta': self.strategies,
                    }
                    self.set_data(data)
                else:
                    sequence_continue = True

        time.sleep(10)

        if sequence_continue:
            sequence.append(self.get_number())
            self.check_strategies(sequence)
        elif all(number == 0 for number in sequence):
            self.check_strategies([])
        else:
            self.check_strategies([sequence[-1]])

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
            
    def set_data(self, data):
        if not os.path.exists('tmp'):
            os.makedirs('tmp')
        with open(f'tmp\{self.roulette}.json', 'w') as f:
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
            'column_one': '1ª Coluna',
            'column_two': '2ª Coluna',
            'column_three': '3ª Coluna',
            'line_one': '1ª Linha',
            'line_two': '2ª Linha',
            'line_three': '3ª Linha'
        }

        related_categories = [category_full_names.get(category, category)
                              for category in categories.get(strategys, [])]

        return f"{' e '.join(related_categories)}"

    def run(self):
        

        threading.Thread(target=self.game_check).start()
        threading.Thread(target=self.goto_roulette).start()


if __name__ == "__main__":
    test = RoulleteBot('a')
    # test.login()
    # threading.Thread(target=test.game_check).start()
    # threading.Thread(target=test.goto_roulette).start()
    test.run()
