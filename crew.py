from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool
import os
from dotenv import load_dotenv
from models import PesquisaOutput, PesquisaResultado
from tools.wiki_resumo import wikipedia_resumo
from tools.web_search_ddg import search_web
from tools.text_processor import extract_key_points

# Carregar variáveis de ambiente
load_dotenv()

# Configurar LLM com a API key do Groq - reduzindo temperature para diminuir verbosidade
llm = LLM(
    model="groq/meta-llama/llama-4-scout-17b-16e-instruct", 
    temperature=0.1,  # Temperatura mais baixa para respostas mais diretas
    api_key=os.getenv("GROQ_API_KEY")
)

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
    
    @agent 
    def wikipedia_pesquisador(self) -> Agent:
        return Agent(
            config=self.agents_config["wikipedia_pesquisador"],
            verbose=True,  # Reduzir verbosidade para economizar tokens
            tools=[wikipedia_resumo, extract_key_points],
            llm=llm,
        )
        
    @agent
    def redator_artigo(self) -> Agent:
        return Agent(
            config=self.agents_config["redator_artigo"],
            verbose=True,  # Reduzir verbosidade para economizar tokens
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
    
    @task
    def pesquisa_wikipedia_task(self) -> Task:
        return Task(
            config=self.tasks_config["pesquisa_wikipedia_task"],
        )

    @task
    def escrever_artigo_task(self) -> Task:
        return Task(
            config=self.tasks_config["escrever_artigo_task"],
        )

    @crew
    def crew(self) -> Crew:
        # Podemos escolher o fluxo desejado
        return self.wikipedia_artigo_crew()
    
    def pesquisa_ddg_crew(self) -> Crew:
        """Fluxo de pesquisa usando DuckDuckGo com posterior sintetização"""
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
    
    def wikipedia_artigo_crew(self) -> Crew:
        """Fluxo de pesquisa na Wikipedia com criação de artigo"""
        # Criamos as tarefas
        wiki_task = self.pesquisa_wikipedia_task()
        artigo_task = self.escrever_artigo_task()
        
        # Configuramos o fluxo de trabalho para processar sequencialmente
        return Crew(
            agents=[self.wikipedia_pesquisador(), self.redator_artigo()],
            tasks=[wiki_task, artigo_task],
            process=Process.sequential,
            verbose=False,  # Reduzir verbosidade para economizar tokens
        )
        
    def format_output(self, result) -> PesquisaOutput:
        """
        Formata o resultado da Crew usando o modelo Pydantic.
        """
        try:
            # Simplificando a extração do resultado para reduzir processamento
            if hasattr(result, "raw_output"):
                resultado_texto = str(result.raw_output)
            else:
                resultado_texto = str(result)
            
            # Simplificando a estrutura do resultado
            tema = "Artigo sobre o tema solicitado"
            resumo = resultado_texto
            
            # Removendo a criação de múltiplos resultados para economizar tokens
            return PesquisaOutput(
                tema=tema,
                resultados=[PesquisaResultado(topico="Artigo", descricao="Artigo de 300 palavras gerado")],
                resumo=resumo
            )
        except Exception as e:
            # Em caso de erro, retorna um output mínimo
            error_msg = str(e)
            result_str = str(result) if result else "Sem resultado"
            return PesquisaOutput(
                tema="Erro ao processar",
                resultados=[PesquisaResultado(topico="Erro", descricao=error_msg)],
                resumo=f"Ocorreu um erro ao formatar o resultado: {error_msg}. Resultado original: {result_str[:200]}"
            )