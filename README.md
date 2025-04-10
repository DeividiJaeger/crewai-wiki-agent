# Teste CrewAI com Groq

Este projeto demonstra a integração do CrewAI com o modelo de linguagem Groq para responder perguntas de forma automatizada.

## Visão Geral

O projeto usa o framework CrewAI para criar um agente inteligente que responde perguntas usando o modelo de linguagem da Groq. Tudo é empacotado em um container Docker para facilitar a execução em qualquer ambiente.

## Pré-requisitos

- Docker instalado em sua máquina
- Uma chave de API do Groq (obtenha em [https://console.groq.com/keys](https://console.groq.com/keys))

## Estrutura do Projeto

```
teste-crew/
├── .env                  # Arquivo com as variáveis de ambiente
├── Dockerfile            # Configuração do Docker
├── main.py               # Código principal do projeto
├── README.md             # Este arquivo
└── requirements.txt      # Dependências Python
```

## Como Executar o Projeto

### 1. Configure a chave da API do Groq

Verifique se o arquivo `.env` contém sua chave de API do Groq:

```
GROQ_API_KEY=sua_chave_api_aqui
```

### 2. Construa a Imagem Docker

Execute o seguinte comando na pasta raiz do projeto:

```bash
docker build -t teste-crew .
```

Este comando cria uma imagem Docker chamada `teste-crew` a partir das instruções no Dockerfile.

### 3. Execute o Container

```bash
docker run teste-crew
```

Este comando inicia o container e executa o código que faz a consulta ao modelo de linguagem da Groq.

## Executando sem Reconstruir

Após fazer alterações apenas no código Python (sem alterar dependências):

```bash
# Constrói novamente a imagem, aproveitando as camadas em cache
docker build -t teste-crew .

# Executa o container
docker run teste-crew
```

O Docker é inteligente e usará cache para as camadas que não mudaram, economizando tempo na reconstrução.

## Forçando uma Reconstrução Completa

Se você precisar reconstruir tudo do zero (por exemplo, após adicionar novas dependências):

```bash
docker build --no-cache -t teste-crew .
```

## Verificando Logs e Depuração

Para ver os logs em tempo real durante a execução:

```bash
docker run -it teste-crew
```

## Explicação dos Componentes

### CrewAI

O CrewAI é um framework para criar agentes de IA que podem trabalhar juntos. Neste projeto, usamos:

- **Agent**: Define o papel, objetivo e a história de fundo do assistente
- **Task**: Define a tarefa que o agente deve executar
- **Crew**: Organiza um ou mais agentes para executar tarefas

### Groq

Groq é uma plataforma que fornece acesso a modelos de linguagem de alta performance. Usamos o modelo "llama3-70b-8192" para responder às perguntas.

## Solução de Problemas

### Erro de Importação ou Dependência

Se encontrar erros relacionados à importação de bibliotecas:

```bash
# Verifique se o requirements.txt está correto e reconstrua a imagem
docker build --no-cache -t teste-crew .
```

### Erro na Chave da API

Se o erro estiver relacionado à autenticação com o Groq:

1. Verifique se sua chave API está correta no arquivo `.env`
2. Reconstrua a imagem: `docker build -t teste-crew .`
3. Execute novamente: `docker run teste-crew`

### Container Finaliza sem Resposta

Se o container terminar sem dar uma resposta:

```bash
# Execute com modo interativo para ver mensagens de erro
docker run -it teste-crew
```
