import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configurar as opções do navegador
chrome_options = Options()
# chrome_options.add_argument('--headless')  # Adicione as opções desejadas, como 'headless'

# Inicializar o driver do Chrome com as opções
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=chrome_options
)


# Realizar alguma ação, como clicar em um elemento
element = driver.find_element_by_name('q')
element.send_keys('Exemplo de pesquisa')
element.submit()

# Aguardar um tempo (por exemplo, 5 segundos)
time.sleep(5)

# Fechar o navegador
driver.quit()
