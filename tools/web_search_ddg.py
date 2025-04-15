import requests
from crewai.tools import tool
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun

# Criando uma ferramenta compatível com CrewAI
@tool("web_search")
def search_web(query: str) -> str:
    """Busca informações na web usando DuckDuckGo.
    
    Args:
        query: O termo de busca que você deseja pesquisar.
        
    Returns:
        Resultados da pesquisa como uma string.
    """
    search = DuckDuckGoSearchRun()
    return search.run(query)
