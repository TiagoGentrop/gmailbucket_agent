# Importa a biblioteca principal do Vertex AI, que permite a interação com os modelos de IA do Google Cloud.
import vertexai

# Importa o módulo 'sys' para interagir com o sistema, embora não seja utilizado neste trecho de código.
import sys

# Importa o módulo 'os' para interagir com o sistema operacional, 
# usado aqui para acessar variáveis de ambiente.
import os

# Da biblioteca 'dotenv', importa a função 'load_dotenv'.
# Esta função é usada para carregar variáveis de ambiente a partir de um arquivo .env.
# Isso é útil para manter informações sensíveis (como chaves de API e IDs de projeto) fora do código-fonte.
from dotenv import load_dotenv

# Executa a função para carregar as variáveis de ambiente do arquivo .env para o ambiente do sistema.
load_dotenv()

# Da biblioteca 'google.adk.agents', importa a classe 'Agent'.
# Esta classe é a base para a criação de agentes de IA, definindo seu comportamento, ferramentas e modelo.
from google.adk.agents import Agent

# Realiza uma importação relativa do arquivo 'prompt.py' (localizado no mesmo diretório).
# Importa a variável 'ROOT_AGENT_INSTRUCTION', que provavelmente contém o texto da instrução principal para o agente.
from .prompt import ROOT_AGENT_INSTRUCTION

# Realiza uma importação relativa do arquivo 'tools.py'.
# Importa a função 'enviar_email', que será uma das ferramentas que o agente pode utilizar.
# A função 'baixar_drive_para_gcs' também é importada, mas não está sendo usada na definição deste agente específico.
from .tools import enviar_email

# Inicializa o SDK do Vertex AI com as configurações do projeto.
# Esta etapa é crucial para autenticar e conectar sua aplicação aos serviços do Google Cloud.
vertexai.init(
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
)

# Cria uma instância da classe 'Agent' para definir o agente principal.
root_agent = Agent(
    model="gemini-2.0-flash",
    name='AGENT_GMAIL',
    description="Um agente para ajudar a enviar emails.",
    instruction=ROOT_AGENT_INSTRUCTION,
    tools=[
        enviar_email
    ],
)

