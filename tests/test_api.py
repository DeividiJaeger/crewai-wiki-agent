import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from api.api import app
import json
from pydantic import BaseModel
from models import PesquisaOutput, PesquisaResultado

# Cliente de teste para a aplicação FastAPI
client = TestClient(app)

class TestAPI(unittest.TestCase):
    """
    Testes para verificar o funcionamento dos endpoints da API.
    """
    
    def test_root_endpoint(self):
        """Teste do endpoint raiz"""
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "online")
    
    def test_health_endpoint(self):
        """Teste do endpoint de saúde"""
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.json())
        self.assertIn("groq_api", response.json())
    
    @patch('api.api.run_pesquisador')
    def test_pesquisar_endpoint(self, mock_run_pesquisador):
        """Teste do endpoint de pesquisa"""
        # Configurar o mock para simular a resposta da função run_pesquisador
        mock_resultado = PesquisaOutput(
            tema="Teste",
            resultados=[PesquisaResultado(topico="Tópico teste", descricao="Descrição teste")],
            resumo="Resumo teste"
        )
        mock_run_pesquisador.return_value = mock_resultado
        
        # Fazer a solicitação de pesquisa
        response = client.post("/pesquisar", json={"tema": "Teste de API"})
        
        # Verificar se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())
        self.assertEqual(response.json()["status"], "pendente")
    
    def test_pesquisar_sem_tema(self):
        """Teste do endpoint de pesquisa sem fornecer um tema"""
        response = client.post("/pesquisar", json={"tema": ""})
        self.assertEqual(response.status_code, 400)
    
    @patch('api.api.tarefas_em_andamento')
    def test_status_tarefa_nao_encontrada(self, mock_tarefas):
        """Teste do endpoint de status com ID inexistente"""
        # Simular dicionário vazio de tarefas
        mock_tarefas.__contains__.return_value = False
        
        response = client.get("/status/tarefa_inexistente")
        self.assertEqual(response.status_code, 404)
    
    @patch('api.api.tarefas_em_andamento')
    @patch('api.api.resultados_pesquisas')
    def test_fluxo_completo(self, mock_resultados, mock_tarefas):
        """Teste do fluxo completo de pesquisa, verificação de status e obtenção do resultado"""
        # Configurar os mocks para simular tarefas e resultados
        task_id = "task_teste"
        
        # Simular tarefa concluída
        mock_tarefas.__contains__.return_value = True
        mock_tarefas.__getitem__.return_value = {"status": "concluído", "tema": "Teste"}
        
        # Simular resultado disponível
        mock_resultados.__contains__.return_value = True
        mock_resultados.__getitem__.return_value = PesquisaOutput(
            tema="Teste",
            resultados=[PesquisaResultado(topico="Tópico teste", descricao="Descrição teste")],
            resumo="Resumo teste"
        )
        
        # Verificar status
        response_status = client.get(f"/status/{task_id}")
        self.assertEqual(response_status.status_code, 200)
        self.assertEqual(response_status.json()["status"], "concluído")
        
        # Obter resultado
        response_resultado = client.get(f"/resultado/{task_id}")
        self.assertEqual(response_resultado.status_code, 200)
        self.assertEqual(response_resultado.json()["tema"], "Teste")
        self.assertEqual(len(response_resultado.json()["resultados"]), 1)
        self.assertEqual(response_resultado.json()["resultados"][0]["topico"], "Tópico teste")

# Permite executar os testes diretamente
if __name__ == "__main__":
    unittest.main()
