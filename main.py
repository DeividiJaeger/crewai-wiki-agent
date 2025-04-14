from crew import PesquisaCrew
import os
import traceback
from dotenv import load_dotenv
from models import PesquisaOutput, PesquisaResultado

# Carregar variáveis de ambiente
load_dotenv()

def run_pesquisador(tema: str):
    # Verifica se a chave API está configurada
    if not os.getenv("GROQ_API_KEY"):
        return PesquisaOutput(
            tema="Erro de configuração",
            resultados=[PesquisaResultado(topico="Erro", descricao="Chave API do Groq não configurada")],
            resumo="Erro: Chave API do Groq não configurada. Por favor, configure no arquivo .env"
        )
    
    try:
        # inicializo a crew
        crew_instance = PesquisaCrew()
        
        # rodo a ia com o processo sequencial - o pesquisador vai executar primeiro, depois o sintetizador
        crew_obj = crew_instance.crew()
        result = crew_obj.kickoff(inputs={"tema": tema})
        
        # formato o resultado usando Pydantic
        output = crew_instance.format_output(result)
        
        # retorno o objeto Pydantic
        return output
    
    except Exception as e:
        # Em caso de erro, retorna um output mínimo com o traceback completo para debugging
        error_detail = f"{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        return PesquisaOutput(
            tema="Erro na execução",
            resultados=[PesquisaResultado(topico="Erro", descricao=str(e))],
            resumo=f"Ocorreu um erro ao processar sua solicitação: {error_detail[:300]}..."
        )