from crew import PesquisaCrew
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def run_pesquisador(tema: str):
    # Verifica se a chave API está configurada
    if not os.getenv("GROQ_API_KEY"):
        return "Erro: Chave API do Groq não configurada. Por favor, configure no arquivo .env"
    
    # inicializo a crew
    crew_instance = PesquisaCrew()
    
    # rodo a ia com o processo sequencial - o pesquisador vai executar primeiro, depois o sintetizador
    result = crew_instance.crew().kickoff(inputs={"tema": tema})
    
    # retorno o resultado
    return result