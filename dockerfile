# Use a imagem base do Python
FROM python:3.10-slim

# Instale as dependências necessárias
RUN pip install selenium

# Instale o Chrome e o WebDriver do Chrome
RUN apt-get update && apt-get install -y wget unzip
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update
RUN apt-get install -y google-chrome-stable
RUN wget https://chromedriver.storage.googleapis.com/$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip -d /usr/bin
RUN rm chromedriver_linux64.zip

# Copie sua aplicação Python para o contêiner
COPY . /app

# Configure um diretório de trabalho
WORKDIR /app

# Comando padrão a ser executado quando o contêiner for iniciado
CMD ["python", "run.py", "a"]
