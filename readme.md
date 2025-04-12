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
Para iniciar a aplicação Streamlit:
```bash
streamlit run app.py
```

Após a execução, a interface web abrirá automaticamente no seu navegador padrão (geralmente em http://localhost:8501).

## 🧩 Estrutura do Projeto
O projeto organiza agentes, tarefas e lógica da aplicação em um design modular.

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
1. Acesse a interface web
2. Insira uma pergunta ou tópico de pesquisa
3. Clique em "Pesquisar"
4. Aguarde o processamento (pode levar alguns segundos)
5. Visualize os resultados sintetizados

## ✨ Personalização
Personalize agentes e tarefas editando os arquivos YAML na pasta config:
- `agents.yaml`: Modifique funções, objetivos e experiências dos agentes
- `tasks.yaml`: Ajuste descrições de tarefas e resultados esperados

## Modelo LLM
Este projeto usa o Llama 3.1 8B Instant através da API da Groq. Para usar outro modelo ou provedor, modifique a configuração LLM em `crew.py`.