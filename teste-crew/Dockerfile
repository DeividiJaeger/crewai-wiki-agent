FROM python:3.11-slim

WORKDIR /app

# Primeiro copiar apenas o arquivo de requisitos
COPY requirements.txt .

# Instalar dependências em uma única camada
RUN pip install -r requirements.txt

# Por último, copiar os arquivos que mudam com frequência
COPY main.py .
COPY .env .

# Executar o script
CMD ["python", "main.py"]
