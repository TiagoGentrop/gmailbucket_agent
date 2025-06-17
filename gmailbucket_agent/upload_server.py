# Importa o módulo 'os' para interagir com o sistema operacional, especialmente para ler variáveis de ambiente.
import os
# Importa o 'uvicorn', que é o servidor ASGI (Asynchronous Server Gateway Interface) que usaremos para rodar a aplicação.
import uvicorn
# Importa as classes necessárias do FastAPI para criar a aplicação e manipular uploads de arquivos.
from fastapi import FastAPI, File, UploadFile
# Importa a classe 'HTMLResponse' para retornar conteúdo HTML diretamente.
from fastapi.responses import HTMLResponse
# Importa a biblioteca cliente do Google Cloud Storage para fazer o upload dos arquivos.
from google.cloud import storage
# Importa a função 'load_dotenv' da biblioteca python-dotenv para carregar variáveis de um arquivo .env.
from dotenv import load_dotenv

# Executa a função para carregar as variáveis definidas no arquivo .env para o ambiente atual.
load_dotenv()

# Cria uma instância da aplicação FastAPI, que será nosso servidor web.
app = FastAPI()

# Define um endpoint para a raiz ("/") que responde a requisições GET e retorna um conteúdo HTML.
@app.get("/", response_class=HTMLResponse)
async def get_upload_page():
    """Esta função serve a página HTML de upload."""
    # Abre o arquivo "upload.html" em modo de leitura com codificação UTF-8.
    with open("upload.html", "r", encoding="utf-8") as f:
        # Lê o conteúdo do arquivo e o retorna como resposta.
        return f.read()

# Define um endpoint para "/upload" que responde a requisições POST.
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Esta função recebe o arquivo, faz o upload para o GCS
    e retorna o nome do arquivo.
    """
    # Busca o valor da variável de ambiente 'GCS_ATTACHMENT_PATH', que deve conter o caminho no Google Cloud Storage.
    gcs_path = os.getenv("GCS_ATTACHMENT_PATH")
    # Verifica se a variável de ambiente não foi configurada.
    if not gcs_path:
        error_msg = "Erro de Configuração: A variável GCS_ATTACHMENT_PATH está faltando no seu .env."
        # Imprime a mensagem de erro no console do servidor para depuração.
        print(error_msg)
        # Retorna uma resposta JSON indicando falha.
        return {"success": False, "error": error_msg}

    # Bloco try/except para capturar possíveis erros durante o processo de upload.
    try:
        # --- INÍCIO DA LÓGICA ROBUSTA ---
        # Remove o prefixo 'gs://' se ele existir, para não quebrar o código
        # Cria uma cópia da variável para processamento, mantendo a original intacta.
        path_to_process = gcs_path
        # Verifica se o caminho começa com "gs://".
        if path_to_process.startswith("gs://"):
            # Remove os 5 primeiros caracteres ("gs://") para obter um caminho limpo.
            path_to_process = path_to_process[5:] 
        # --- FIM DA LÓGICA ROBUSTA ---

        # Agora, o resto do código funciona com um caminho limpo
        # Verifica se o caminho contém uma barra, que é necessária para separar o bucket da pasta.
        if '/' not in path_to_process:
            # Lança um erro se o formato for inválido (ex: apenas o nome do bucket).
            raise ValueError("O caminho no GCS_ATTACHMENT_PATH deve conter o nome do bucket e pelo menos uma pasta (ex: 'meu-bucket/anexos').")

        # Inicializa o cliente do Google Cloud Storage que permitirá a comunicação com a API do GCS.
        storage_client = storage.Client()
        
        # Divide o caminho no primeiro "/" para separar o nome do bucket do caminho da pasta.
        bucket_name, folder_path = path_to_process.split('/', 1)
        # Obtém uma referência ao objeto do bucket usando o nome extraído.
        bucket = storage_client.bucket(bucket_name)
        
        # Monta o nome final do arquivo no GCS, combinando a pasta e o nome do arquivo original.
        # .strip('/') remove barras extras do início ou fim do caminho da pasta.
        blob_name = f"{folder_path.strip('/')}/{file.filename}"
        # Cria um objeto "blob" que representa o arquivo a ser enviado para o bucket.
        blob = bucket.blob(blob_name)
        
        # Lê o conteúdo do arquivo enviado na requisição de forma assíncrona.
        content = await file.read()
        # Faz o upload do conteúdo (em bytes) para o blob no GCS, preservando o 'content_type' original.
        blob.upload_from_string(content, content_type=file.content_type)
        
        # Imprime uma mensagem de sucesso no console do servidor.
        print(f"Arquivo '{file.filename}' enviado com sucesso para 'gs://{bucket_name}/{blob_name}'.")
        
        # Retorna uma resposta JSON indicando sucesso e o nome do arquivo.
        return {"success": True, "filename": file.filename}

    # Captura qualquer exceção que possa ocorrer durante o bloco 'try'.
    except Exception as e:
        # Imprime a exceção no console para facilitar a depuração.
        print(f"Erro no upload: {e}")
        # Retorna uma resposta JSON de falha com a mensagem de erro.
        return {"success": False, "error": str(e)}

# Este bloco de código é o ponto de entrada principal e só executa se o script for chamado diretamente.
if __name__ == "__main__":
    # Inicia o servidor Uvicorn com a aplicação FastAPI.
    # host="0.0.0.0" torna o servidor acessível na rede local.
    # port=8001 define a porta em que o servidor ficará escutando por requisições.
    uvicorn.run(app, host="0.0.0.0", port=8001)