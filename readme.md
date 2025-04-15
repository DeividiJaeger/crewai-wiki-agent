# 🔍 Pesquisador Web com CrewAI e DuckDuckGo

Um assistente de pesquisa que usa agentes de IA para buscar informações na web através do DuckDuckGo e sintetizar resultados de forma clara e objetiva.

## 📋 Requisitos
- Python 3.12
- Chave de API Groq

## 🛠️ Instalação
1. Clone o repositório
2. Crie e ative um ambiente virtual Python 3.12
3. Instale as dependências
4. Configure o arquivo .env

Crie um arquivo `.env` na raiz do projeto com sua chave de API Groq:
```
GROQ_API_KEY=sua_chave_api_aqui
```

## 🚀 Execução
### Interface Web (Streamlit)
Para iniciar a aplicação Streamlit:
```bash
streamlit run app.py
```

Após a execução, a interface web abrirá automaticamente no seu navegador padrão (geralmente em http://localhost:8501).

### API REST (FastAPI)
Para iniciar o servidor API:
```bash
python -m api.start_api
```

A API estará disponível em http://localhost:8000 e a documentação automática em http://localhost:8000/docs.

## 📡 Endpoints da API
- **POST /pesquisar**: Inicia uma pesquisa em background
- **GET /status/{task_id}**: Verifica o status de uma pesquisa
- **GET /resultado/{task_id}**: Obtém o resultado de uma pesquisa concluída
- **DELETE /resultado/{task_id}**: Remove um resultado do servidor

### Exemplo de uso da API com cURL
```bash
# Iniciar uma pesquisa
curl -X POST http://localhost:8000/pesquisar \
  -H "Content-Type: application/json" \
  -d '{"tema": "inteligência artificial"}'

# Verificar status (substitua {task_id} pelo ID retornado)
curl http://localhost:8000/status/{task_id}

# Obter resultado
curl http://localhost:8000/resultado/{task_id}
```

## 🧩 Estrutura do Projeto
O projeto está organizado nas seguintes pastas:
- `api/`: Contém todos os arquivos relacionados à API REST
- `tests/`: Contém arquivos de teste para a API e outras funcionalidades
- `tools/`: Ferramentas utilizadas pelos agentes
- `config/`: Arquivos de configuração YAML para agentes e tarefas

## 💡 Como Funciona
O projeto usa o framework CrewAI para coordenar dois agentes de IA:

1. **Pesquisador Web**: Busca informações usando o DuckDuckGo
2. **Sintetizador**: Resume os resultados em um formato conciso

O processo é executado sequencialmente - primeiro o Pesquisador busca, depois o Sintetizador processa os resultados.

## ⚠️ Solução de Problemas
- **Erro de Chave API**: Verifique se seu arquivo .env está configurado corretamente
- **Tempo Limite nas Buscas**: Pesquisas complexas podem levar mais tempo
- **Erro de Conexão**: Verifique sua conexão com a internet
- **Erro de Dependência**: Tente reinstalar com `pip install -r requirements.txt --force-reinstall`

## 📝 Uso
1. Acesse a interface web ou use a API REST
2. Insira uma pergunta ou tópico de pesquisa
3. Aguarde o processamento (pode levar alguns segundos)
4. Visualize os resultados sintetizados

## ✨ Personalização
Personalize agentes e tarefas editando os arquivos YAML na pasta config:
- `agents.yaml`: Modifique funções, objetivos e experiências dos agentes
- `tasks.yaml`: Ajuste descrições de tarefas e resultados esperados

## Modelo LLM
Este projeto usa o Llama 3.1 8B Instant através da API da Groq. Para usar outro modelo ou provedor, modifique a configuração LLM em `crew.py`.

## Testes
Para executar os testes automatizados:

Para executar os testes manuais da API (a API deve estar em execução):
```bash
python -m tests.test_api_manual --teste completo
```
