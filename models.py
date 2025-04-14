from pydantic import BaseModel, Field
from typing import List, Optional

class PesquisaResultado(BaseModel):
    topico: str = Field(description="Tópico principal da pesquisa")
    descricao: str = Field(description="Descrição detalhada sobre o tópico")

class PesquisaOutput(BaseModel):
    tema: str = Field(description="Tema original da pesquisa")
    resultados: List[PesquisaResultado] = Field(description="Lista de resultados da pesquisa")
    resumo: str = Field(description="Resumo sintetizado dos resultados")
