from crewai.tools import tool

@tool("Text Processor")
def extract_key_points(text: str, num_points: int = 5) -> str:
    """Extrai os pontos principais de um texto longo.
    
    Args:
        text: Texto a ser processado
        num_points: Número de pontos principais a extrair
        
    Returns:
        Lista dos pontos principais extraídos do texto
    """
    # Divide o texto em parágrafos
    paragraphs = [p for p in text.split('\n') if p.strip()]
    
    # Se houver poucos parágrafos, retorna os primeiros
    if len(paragraphs) <= num_points:
        return '\n\n'.join(paragraphs)
    
    # Caso contrário, seleciona o primeiro parágrafo (introdução) e alguns do meio
    important_paragraphs = [paragraphs[0]]
    
    # Seleciona parágrafos distribuídos pelo texto
    step = max(1, (len(paragraphs) - 2) // (num_points - 2))
    for i in range(1, len(paragraphs) - 1, step):
        if len(important_paragraphs) < num_points - 1:
            important_paragraphs.append(paragraphs[i])
    
    # Adiciona o último parágrafo (conclusão)
    if paragraphs[-1] not in important_paragraphs:
        important_paragraphs.append(paragraphs[-1])
    
    return '\n\n'.join(important_paragraphs)
