from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun
from crewai.tools import tool
import os
from dotenv import load_dotenv
from models import PesquisaOutput, PesquisaResultado

# Carregar variáveis de ambiente
load_dotenv()

# Configurar LLM com a API key do Groq
llm = LLM(model="groq/meta-llama/llama-4-scout-17b-16e-instruct", temperature=0.5, api_key=os.getenv("GROQ_API_KEY"))

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
        
    def format_output(self, result) -> PesquisaOutput:
        """
        Formata o resultado da Crew usando o modelo Pydantic.
        
        Args:
            result: O resultado bruto da execução da Crew (pode ser string ou objeto CrewOutput)
            
        Returns:
            Um objeto PesquisaOutput formatado
        """
        try:
            # Verifica se o resultado é uma string ou um objeto
            resultado_texto = ""
            if hasattr(result, "raw_output"):
                # CrewOutput tem um atributo raw_output
                resultado_texto = str(result.raw_output)
            elif hasattr(result, "__str__"):
                # Se não for CrewOutput mas tiver método __str__
                resultado_texto = str(result)
            else:
                # Caso seja outro tipo de objeto
                resultado_texto = f"Resultados da pesquisa: {repr(result)}"
            
            # Agora processamos o texto
            linhas = resultado_texto.split('\n')
            tema = ""
            resumo = ""
            resultados = []
            
            # Identificamos o tema e o resumo
            for i, linha in enumerate(linhas):
                linha = linha.strip()
                if not linha:
                    continue
                    
                if i == 0 and ":" in linha:
                    # Primeira linha geralmente contém o tema
                    tema = linha.split(":", 1)[1].strip()
                elif "resumo" in linha.lower() or i == len(linhas) - 1:
                    # Última linha ou linha marcada como resumo
                    resumo = linha.strip()
                elif linha and not linha.startswith("-"):
                    # Outras linhas não vazias são provavelmente tópicos
                    descricao = linha
                    resultados.append(PesquisaResultado(topico=f"Tópico {len(resultados)+1}", descricao=descricao))
            
            # Se não conseguimos identificar o tema, usamos o texto da pesquisa
            if not tema:
                tema = "Resultados da pesquisa"
            
            # Se não conseguimos identificar o resumo, usamos o último resultado ou o texto completo
            if not resumo and resultados:
                resumo = resultados[-1].descricao
            elif not resumo:
                resumo = resultado_texto[:200] + "..." if len(resultado_texto) > 200 else resultado_texto
                
            return PesquisaOutput(
                tema=tema,
                resultados=resultados if resultados else [PesquisaResultado(topico="Resultado geral", descricao=resultado_texto)],
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