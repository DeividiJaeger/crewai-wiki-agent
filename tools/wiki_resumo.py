import requests
from crewai.tools import tool

@tool("Wikipedia Resumo Tool")
def wikipedia_resumo(term: str, max_chars: int = 2000) -> str:
    """Busca um resumo da Wikipédia para o termo fornecido.
    
    Args:
        term: O termo a ser pesquisado na Wikipedia
        max_chars: Número máximo de caracteres a retornar (padrão: 2000)
    
    Returns:
        Resumo do artigo limitado ao tamanho especificado
    """
    url = f"https://pt.wikipedia.org/w/api.php?action=query&prop=extracts&exlimit=1&explaintext=1&titles={term}&format=json&utf8=1&redirects=1&exintro=1"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        
        if pages:
            # Obtém o primeiro ID de página (ignorando o número específico)
            page_id = next(iter(pages))
            extract = pages[page_id].get("extract", "")
            
            if extract:
                # Limita o tamanho do extrato para economizar tokens
                if len(extract) > max_chars:
                    extract = extract[:max_chars] + "..."
                return extract
            return "Nenhum conteúdo encontrado na Wikipedia para este termo."
    return f"Erro ao buscar o termo '{term}' na Wikipedia."
