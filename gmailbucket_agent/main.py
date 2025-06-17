# Importa o módulo 'os' para interagir com o sistema operacional, como ler variáveis de ambiente.
import os
# Importa o 'uvicorn', que é o servidor ASGI (Asynchronous Server Gateway Interface) usado para rodar nossa aplicação FastAPI.
import uvicorn
# Importa classes essenciais do FastAPI:
# - FastAPI: A classe principal para criar a aplicação web.
# - File, UploadFile: Usadas para declarar e manipular o upload de arquivos.
from fastapi import FastAPI, File, UploadFile
# Importa 'HTMLResponse' para poder retornar respostas no formato HTML.
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
# Importa 'BaseModel' do Pydantic para criar modelos de dados que garantem a validação dos dados de requisições.
from pydantic import BaseModel
# Importa a função 'load_dotenv' para carregar variáveis de ambiente de um arquivo .env.
from dotenv import load_dotenv

# --- Importações do nosso agente e ferramentas ---

# Importa a biblioteca cliente do Google Cloud Storage para interagir com os buckets de armazenamento.
from google.cloud import storage
# Importa a classe 'Runner' do kit de desenvolvimento de agentes (ADK) do Google.
# O 'Runner' é responsável por executar o agente e gerenciar o ciclo de vida da conversa.
from google.adk.runners import Runner
# Importa um serviço de sessão que armazena o histórico da conversa em memória.
from google.adk.sessions import InMemorySessionService
# Importa a instância 'root_agent' que foi definida no nosso arquivo 'agent.py'.
from .agent import root_agent

# Executa a função para carregar as variáveis de ambiente do arquivo .env.
load_dotenv()

# --- Inicialização da Aplicação ---

# Cria a instância principal da aplicação FastAPI.
app = FastAPI()
# --- LÓGICA DE CAMINHO ABSOLUTO (A SOLUÇÃO DEFINITIVA) ---

# NOVO: Pega o caminho absoluto do diretório onde main.py está (a pasta 'agent_gmail')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# NOVO: Junta o caminho base com o nome da pasta 'templates'
STATIC_DIR = os.path.join(BASE_DIR, "templates")

# NOVO: Usa a variável STATIC_DIR que contém o caminho completo e sem ambiguidades
app.mount("/templates", StaticFiles(directory=STATIC_DIR), name="templates")
# Cria uma instância do 'Runner' para o nosso agente.
# Esta instância irá gerenciar as interações com o agente.
program = Runner(
                # Associa o agente que criamos ('root_agent') ao Runner.
                agent=root_agent,
                # Define um nome para a aplicação, útil para logging e identificação.
                app_name="agent_gmail",
                # Define o serviço de sessão. 'InMemorySessionService' mantém o histórico da conversa na memória RAM do servidor.
                session_service=InMemorySessionService(),
               )

# Pega o caminho do bucket e pasta no Google Cloud Storage (GCS) a partir da variável de ambiente.
GCS_ATTACHMENT_PATH = os.getenv("GCS_ATTACHMENT_PATH")

# --- Endpoints (Rotas) da nossa API ---

# Define uma rota para o método GET na raiz do site ("/"). A resposta será do tipo HTML.
@app.get("/", response_class=HTMLResponse)
async def get_chat_page():
    """Esta função serve a página HTML principal do chat."""
    try:
        # Pega o diretório do script atual.
        script_dir = os.path.dirname(__file__)
        # Constrói o caminho completo para o arquivo HTML do chat.
        chat_html_path = os.path.join(script_dir, "templates", "chat.html")
        # Abre e lê o arquivo HTML.
        with open(chat_html_path, "r", encoding="utf-8") as f:
            # Retorna o conteúdo do arquivo como uma resposta HTML.
            return f.read()
    # Caso o arquivo não seja encontrado, retorna um erro 404.
    except FileNotFoundError:
        return HTMLResponse("<h1>Erro: Arquivo templates/chat.html não encontrado.</h1>", status_code=404)

# Define uma rota para o método POST no endpoint "/upload".
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Este endpoint lida com o upload de um arquivo para o Google Cloud Storage (GCS)."""
    # Verifica se o caminho do GCS foi configurado no arquivo .env.
    if not GCS_ATTACHMENT_PATH:
        return {"success": False, "error": "GCS_ATTACHMENT_PATH não configurado no .env"}
        
    try:
        # Inicializa o cliente do Google Cloud Storage.
        storage_client = storage.Client()
        # Define o caminho do GCS a ser processado.
        path_to_process = GCS_ATTACHMENT_PATH
        # Remove o prefixo "gs://" se ele existir, pois a biblioteca não o utiliza nesta parte.
        if path_to_process.startswith("gs://"):
            path_to_process = path_to_process[5:]
        
        # Separa o nome do bucket do caminho da pasta dentro dele.
        bucket_name, folder_path = path_to_process.split('/', 1)
        # Acessa o bucket específico.
        bucket = storage_client.bucket(bucket_name)
        # Cria o nome completo do objeto (blob) no bucket, incluindo a pasta.
        blob_name = f"{folder_path.strip('/')}/{file.filename}"
        # Cria uma referência para o blob (o futuro arquivo no bucket).
        blob = bucket.blob(blob_name)
        
        # Lê o conteúdo do arquivo enviado de forma assíncrona.
        content = await file.read()
        # Faz o upload do conteúdo para o GCS, especificando o tipo de conteúdo (ex: 'image/jpeg').
        blob.upload_from_string(content, content_type=file.content_type)
        
        # Retorna uma resposta de sucesso com o nome do arquivo.
        return {"success": True, "filename": file.filename}
    # Captura qualquer exceção que ocorra durante o processo de upload.
    except Exception as e:
        return {"success": False, "error": str(e)}

# Define a estrutura de dados esperada para a requisição do chat usando Pydantic.
# A requisição deve conter um campo "message" que é uma string.
class ChatRequest(BaseModel):
    message: str

# Define uma rota para o método POST no endpoint "/chat".
@app.post("/chat")
async def handle_chat(chat_request: ChatRequest):
    """Este endpoint recebe a mensagem do usuário e a envia para o agente."""
    try:
        # Chama o método 'chat' do nosso 'program' (Runner), passando a mensagem do usuário.
        # O Runner gerencia a conversa com o agente e retorna a resposta.
        response = await program.chat(chat_request.message)
        # Retorna uma resposta de sucesso com a resposta do agente.
        return {"success": True, "response": response}
    # Captura qualquer exceção que ocorra durante a interação com o agente.
    except Exception as e:
        return {"success": False, "error": str(e)}

# Este bloco de código só será executado se o script for chamado diretamente (ex: python main.py).
if __name__ == "__main__":
    # Inicia o servidor Uvicorn para rodar a aplicação 'app'.
    # host="0.0.0.0" faz o servidor ficar visível na rede local.
    # port=8001 define a porta em que o servidor irá rodar.
    uvicorn.run(app, host="0.0.0.0", port=8001)