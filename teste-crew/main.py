import os
import sys
import subprocess

# Desabilitar telemetria OpenTelemetry que está causando erros de conexão
os.environ["OTEL_SDK_DISABLED"] = "true"

# Verificar e instalar dependências necessárias
try:
    import typing_extensions
    import dotenv
except ImportError:
    print("Instalando dependências necessárias...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "typing_extensions", "python-dotenv"])
    import dotenv

# Carregar variáveis de ambiente do arquivo .env
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, Task, Crew, LLM
# Configurar a chave da API do Groq
api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    raise ValueError("Por favor, defina a variável de ambiente GROQ_API_KEY no arquivo .env")

# Configurar o LLM para o CrewAI
llm = LLM(
    model="llama3-70b-8192",  # Especifique um modelo do Groq
    api_key=api_key,
    api_base="https://api.groq.com/openai/v1",
    temperature=0.5
)

# Definir o agente com o modelo específico do Groq
agente = Agent(
    role='Assistente',
    goal='Responder perguntas do usuário.',
    backstory='Um assistente virtual que utiliza o modelo de linguagem do Groq.',
    verbose=True,
    allow_delegation=False,
    llm=llm  
)

# Definir a tarefa
tarefa = Task(
    description='Responder à pergunta: "liste as 5 ações com mais potencial de valorização no mercado brasileiro de ações',
    agent=agente,
    expected_output="Uma resposta clara e precisa para a pergunta do usuário."
)

# Criar a equipe e executar a tarefa
equipe = Crew(
    agents=[agente],
    tasks=[tarefa],
    verbose=True  
)

resultado = equipe.kickoff()
print(resultado)
