from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import time
from typing import Dict, Optional
import os

from main import run_pesquisador  # Importando a função principal
from models import PesquisaOutput  # Importando os modelos

# Criação da aplicação FastAPI
app = FastAPI(
    title="Agente Wiki API",
    description="API para pesquisar e gerar artigos usando agentes de IA",
    version="1.0.0"
)

# Configuração CORS para permitir requisições de outros domínios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, defina origens específicas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Classes de modelo para as requisições
class PesquisaRequest(BaseModel):
    tema: str
    
class PesquisaStatusResponse(BaseModel):
    id: str
    status: str
    eta: Optional[int] = None

# Armazenamento em memória para tarefas em background
# Em um ambiente de produção, use Redis ou um banco de dados
tarefas_em_andamento: Dict[str, Dict] = {}
resultados_pesquisas: Dict[str, PesquisaOutput] = {}

# Função para executar pesquisa em background
def executar_pesquisa_background(task_id: str, tema: str):
    try:
        # Atualiza status para em processamento
        tarefas_em_andamento[task_id]["status"] = "processando"
        
        # Executa a pesquisa
        resultado = run_pesquisador(tema)
        
        # Armazena o resultado
        resultados_pesquisas[task_id] = resultado
        
        # Atualiza status para completo
        tarefas_em_andamento[task_id]["status"] = "concluído"
    except Exception as e:
        # Em caso de erro, atualiza o status
        tarefas_em_andamento[task_id]["status"] = f"erro: {str(e)}"

@app.post("/pesquisar", response_model=PesquisaStatusResponse)
async def iniciar_pesquisa(request: PesquisaRequest, background_tasks: BackgroundTasks):
    """
    Inicia uma pesquisa em background sobre o tema fornecido.
    Retorna um ID para consultar o status e resultado posteriormente.
    """
    if not request.tema:
        raise HTTPException(status_code=400, detail="Tema não pode estar em branco")
    
    # Gera um ID único para a tarefa (em produção, use UUID)
    task_id = f"task_{int(time.time())}"
    
    # Registra a tarefa como pendente
    tarefas_em_andamento[task_id] = {
        "status": "pendente", 
        "tema": request.tema,
        "tempo_inicio": time.time()
    }
    
    # Inicia a tarefa em background
    background_tasks.add_task(executar_pesquisa_background, task_id, request.tema)
    
    return PesquisaStatusResponse(
        id=task_id,
        status="pendente",
        eta=60  # Estimativa de 60 segundos para conclusão
    )

@app.get("/status/{task_id}", response_model=PesquisaStatusResponse)
async def verificar_status(task_id: str):
    """
    Verifica o status de uma pesquisa em andamento.
    """
    if task_id not in tarefas_em_andamento:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    status = tarefas_em_andamento[task_id]["status"]
    
    # Calcula ETA se ainda estiver processando
    eta = None
    if status == "processando":
        tempo_decorrido = time.time() - tarefas_em_andamento[task_id]["tempo_inicio"]
        if tempo_decorrido < 60:
            eta = 60 - int(tempo_decorrido)
    
    return PesquisaStatusResponse(
        id=task_id,
        status=status,
        eta=eta
    )

@app.get("/resultado/{task_id}", response_model=PesquisaOutput)
async def obter_resultado(task_id: str):
    """
    Obtém o resultado de uma pesquisa concluída.
    """
    if task_id not in tarefas_em_andamento:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    if tarefas_em_andamento[task_id]["status"] != "concluído":
        raise HTTPException(status_code=400, detail="Pesquisa ainda não concluída")
    
    if task_id not in resultados_pesquisas:
        raise HTTPException(status_code=404, detail="Resultado não encontrado")
    
    return resultados_pesquisas[task_id]

@app.delete("/resultado/{task_id}")
async def remover_resultado(task_id: str):
    """
    Remove um resultado de pesquisa do servidor para liberar memória.
    """
    if task_id not in tarefas_em_andamento:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    # Remove os dados da memória
    if task_id in resultados_pesquisas:
        del resultados_pesquisas[task_id]
    
    del tarefas_em_andamento[task_id]
    
    return {"message": "Dados removidos com sucesso"}

# Endpoint raiz para verificar se a API está funcionando
@app.get("/")
async def root():
    """
    Endpoint para verificar se a API está funcionando.
    """
    return {"status": "online", "message": "API de Agentes de Pesquisa está operacional"}

# Verificação de saúde da API
@app.get("/health")
async def health_check():
    """
    Endpoint para verificação de saúde da API.
    """
    # Verifica se a chave GROQ está configurada
    groq_key_status = "configurada" if os.getenv("GROQ_API_KEY") else "não configurada"
    
    return {
        "status": "healthy",
        "groq_api": groq_key_status,
        "tarefas_ativas": len(tarefas_em_andamento),
        "resultados_armazenados": len(resultados_pesquisas)
    }

# Bloco para executar diretamente o servidor se este arquivo for executado
if __name__ == "__main__":
    # Iniciar o servidor Uvicorn quando o script for executado diretamente
    # O parâmetro reload=True permite recarregar automaticamente o servidor quando os arquivos são alterados
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
