import uvicorn

if __name__ == "__main__":
    """
    Script para iniciar o servidor FastAPI usando Uvicorn.
    
    Este script serve como um ponto de entrada simplificado para iniciar a API.
    Ele configura o servidor Uvicorn para servir nossa aplicação FastAPI.
    """
    # Parâmetros:
    # - "api.api:app": Módulo:Instância (aponta para a variável app em api.py)
    # - host="0.0.0.0": Permite acesso de qualquer IP (não apenas localhost)
    # - port=8000: Porta padrão para FastAPI
    # - reload=True: Recarrega o servidor quando os arquivos são alterados (útil para desenvolvimento)
    uvicorn.run(
        "api.api:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )
