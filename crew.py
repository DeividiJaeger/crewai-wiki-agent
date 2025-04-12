from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun
from crewai.tools import tool
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar LLM com a API key do Groq
llm = LLM(model="groq/llama-3.1-8b-instant", temperature=0, api_key=os.getenv("GROQ_API_KEY"))

# Criando uma ferramenta compatível com CrewAI
@tool("web_search")
def search_web(query: str) -> str:
    """Busca informações na web usando DuckDuckGo.
    
    Args:
        query: O termo de busca que você deseja pesquisar.
        
    Returns:
        Resultados da pesquisa como uma string.
    """
    search = DuckDuckGoSearchRun()
    return search.run(query)

@CrewBase
class PesquisaCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def pesquisador(self) -> Agent:
        return Agent(
            config=self.agents_config["pesquisador"],
            verbose=True,
            tools=[search_web],
            llm=llm,
        )
    
    @agent
    def sintetizador(self) -> Agent:
        return Agent(
            config=self.agents_config["sintetizador"],
            verbose=True,
            tools=[],
            llm=llm,
        )
    
    @task
    def realizar_pesquisa(self) -> Task:
        return Task(
            config=self.tasks_config["realizar_pesquisa"],
        )
    
    @task
    def sintetizar_informacoes(self) -> Task:
        return Task(
            config=self.tasks_config["sintetizar_informacoes"],
        )

    @crew
    def crew(self) -> Crew:
        # Criamos as tarefas
        pesquisa_task = self.realizar_pesquisa()
        sintese_task = self.sintetizar_informacoes()

        # Configuramos o fluxo de trabalho para processar sequencialmente
        return Crew(
            agents=[self.pesquisador(), self.sintetizador()],
            tasks=[pesquisa_task, sintese_task],
            process=Process.sequential,
            verbose=True,
        )