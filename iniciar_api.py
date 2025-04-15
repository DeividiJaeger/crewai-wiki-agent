import os
import sys

# Adiciona o diretório atual ao PYTHONPATH para encontrar os módulos
sys.path.append(os.path.abspath('.'))

# Importa o script de inicialização da API
from api.start_api import main

if __name__ == "__main__":
    """
    Ponto de entrada principal para iniciar a API a partir da raiz do projeto.
    Este script redireciona para o script de inicialização na pasta da API.
    """
    # Executa diretamente o script start_api.py
    exec(open("api/start_api.py").read())
