import requests
import time
import sys
import argparse

"""
Script para teste manual da API.
Este script testa todos os endpoints da API quando ela estiver em execução.

Uso:
    python tests/test_api_manual.py --url http://localhost:8000 --teste completo
    python tests/test_api_manual.py --url http://localhost:8000 --teste basico
"""

def teste_basico(base_url):
    """Testes básicos da API - endpoints / e /health"""
    print("\n==== TESTE BÁSICO ====")
    
    # Teste do endpoint raiz
    print("\n-> Testando endpoint raiz...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print(f"✅ Sucesso! Resposta: {response.json()}")
        else:
            print(f"❌ Erro! Status: {response.status_code}, Resposta: {response.text}")
    except Exception as e:
        print(f"❌ Exceção: {str(e)}")
    
    # Teste do endpoint de saúde
    print("\n-> Testando endpoint de saúde...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print(f"✅ Sucesso! Resposta: {response.json()}")
        else:
            print(f"❌ Erro! Status: {response.status_code}, Resposta: {response.text}")
    except Exception as e:
        print(f"❌ Exceção: {str(e)}")

def teste_completo(base_url):
    """Teste completo da API - fluxo de pesquisa, status e resultado"""
    print("\n==== TESTE COMPLETO ====")
    
    # Teste básico primeiro
    teste_basico(base_url)
    
    # Teste do endpoint de pesquisa
    print("\n-> Testando endpoint de pesquisa...")
    try:
        tema = "agente inteligente"
        response = requests.post(f"{base_url}/pesquisar", json={"tema": tema})
        
        if response.status_code == 200:
            task_id = response.json()["id"]
            print(f"✅ Sucesso! Tarefa criada com ID: {task_id}")
            
            # Teste do endpoint de status
            print("\n-> Testando endpoint de status...")
            status = "pendente"
            max_checks = 10
            checks = 0
            
            while status in ["pendente", "processando"] and checks < max_checks:
                status_response = requests.get(f"{base_url}/status/{task_id}")
                
                if status_response.status_code == 200:
                    status = status_response.json()["status"]
                    print(f"  Status atual: {status}")
                    
                    if status == "concluído":
                        print("✅ Processamento concluído com sucesso!")
                        break
                    elif status.startswith("erro"):
                        print(f"❌ Erro no processamento: {status}")
                        break
                else:
                    print(f"❌ Erro ao verificar status: {status_response.status_code}")
                    break
                
                checks += 1
                print(f"  Aguardando 5 segundos... ({checks}/{max_checks})")
                time.sleep(5)
            
            if checks >= max_checks and status not in ["concluído"]:
                print("⚠️ Tempo limite excedido ao aguardar processamento")
            
            # Teste do endpoint de resultado (apenas se concluído)
            if status == "concluído":
                print("\n-> Testando endpoint de resultado...")
                resultado_response = requests.get(f"{base_url}/resultado/{task_id}")
                
                if resultado_response.status_code == 200:
                    resultado = resultado_response.json()
                    print("✅ Resultado obtido com sucesso!")
                    print(f"\nTema: {resultado['tema']}")
                    print("\nResultados:")
                    for res in resultado["resultados"]:
                        print(f"- {res['topico']}: {res['descricao']}")
                    print(f"\nResumo: {resultado['resumo'][:100]}...")
                    
                    # Teste do endpoint de remoção
                    print("\n-> Testando endpoint de remoção...")
                    remover_response = requests.delete(f"{base_url}/resultado/{task_id}")
                    
                    if remover_response.status_code == 200:
                        print("✅ Resultado removido com sucesso!")
                    else:
                        print(f"❌ Erro ao remover resultado: {remover_response.status_code}")
                else:
                    print(f"❌ Erro ao obter resultado: {resultado_response.status_code}")
        else:
            print(f"❌ Erro ao iniciar pesquisa: {response.status_code}, Resposta: {response.text}")
    except Exception as e:
        print(f"❌ Exceção: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Testa os endpoints da API")
    parser.add_argument("--url", default="http://localhost:8000", help="URL base da API")
    parser.add_argument("--teste", default="basico", choices=["basico", "completo"], 
                       help="Tipo de teste a ser executado")
    
    args = parser.parse_args()
    
    print(f"Testando API em {args.url}")
    
    if args.teste == "basico":
        teste_basico(args.url)
    else:
        teste_completo(args.url)
    
    print("\nTestes concluídos.")
