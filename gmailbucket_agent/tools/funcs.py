# -*- coding: utf-8 -*-

# --- Importações Padrão e de Terceiros ---
# Importa o módulo 'os' para interagir com o sistema operacional, como ler variáveis de ambiente e manipular caminhos.
import os
# Importa 'base64' para codificar a mensagem de email em um formato seguro para a web, exigido pela API do Gmail.
import base64
# Importa 're' para usar expressões regulares (regex) na validação de formatos de e-mail.
import re
# Importa 'mimetypes' para adivinhar o tipo de mídia (MIME type) de um arquivo de anexo (ex: 'application/pdf').
import mimetypes
# Importa 'Optional' do módulo 'typing' para indicar que um argumento de função pode ser opcional.
from typing import Optional
# Importa 'load_dotenv' para carregar variáveis de ambiente de um arquivo .env.
from dotenv import load_dotenv
# Importa 'requests' para fazer requisições HTTP, usado para baixar arquivos do Google Drive.
import requests
# Importa funções para analisar URLs, usado para extrair o ID de um link do Google Drive.
from urllib.parse import urlparse, parse_qs

# Executa a função para carregar as variáveis do arquivo .env no ambiente do sistema.
load_dotenv()

# --- Importações do Google ---
# Importa a biblioteca cliente do Google Cloud Storage para interagir com buckets.
from google.cloud import storage
# Importa classes para lidar com a autenticação e autorização do Google.
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
# Importa o construtor de serviços da API do Google e o manipulador de erros HTTP.
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- Importações de Email ---
# Importa classes do módulo 'email' para construir a estrutura da mensagem de email.
from email.mime.multipart import MIMEMultipart # Para emails com múltiplas partes (texto e anexos).
from email.mime.text import MIMEText           # Para a parte de texto do email.
from email.mime.base import MIMEBase           # A classe base para criar partes de anexo.
from email import encoders                     # Para codificar os anexos em Base64.


# Carrega o caminho padrão para anexos no GCS a partir das variáveis de ambiente.
GCS_ATTACHMENT_PATH = os.getenv("GCS_ATTACHMENT_PATH")

# Define os escopos de permissão. Aqui, estamos pedindo permissão apenas para ENVIAR emails em nome do usuário.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def enviar_email(destinatarios: list[str], assunto: str, corpo_mensagem: str, nome_do_arquivo_anexo: Optional[str] = None) -> str:
    """
    Envia um email, com suporte opcional a um anexo do Google Cloud Storage.
    A função é inteligente e aceita um nome de arquivo simples ou um caminho completo do GCS.

    Args:
        destinatarios (list[str]): Uma lista de e-mails dos destinatários.
        assunto (str): O assunto do email.
        corpo_mensagem (str): O conteúdo de texto do email.
        nome_do_arquivo_anexo (Optional[str]): O nome do arquivo (ex: "relatorio.pdf") ou o caminho completo
                                             no GCS (ex: "meu-bucket/pasta/arquivo.pdf"). Padrão é None.

    Returns:
        str: Uma mensagem de sucesso ou de erro.
    """
    # 1. Validação dos emails dos destinatários
    if not destinatarios:
        return "Erro: A lista de destinatários não pode ser vazia."
    # Expressão regular para validar o formato de um endereço de e-mail.
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    for email in destinatarios:
        # Verifica se cada e-mail na lista corresponde ao formato esperado.
        if not re.fullmatch(email_regex, email.strip()):
            return f"Erro: O endereço '{email}' na lista de destinatários não é um formato de e-mail válido."

    # 2. Lógica de autenticação do Google (com cache de token)
    creds = None
    # Constrói os caminhos para os arquivos de credenciais e token.
    script_dir = os.path.dirname(__file__)
    project_root = os.path.join(script_dir, '..') # Navega para o diretório pai (raiz do projeto)
    CREDENTIALS_PATH = os.path.join(project_root, 'credentials.json')
    TOKEN_PATH = os.path.join(project_root, 'token.json')
    
    # Se o arquivo token.json existe, carrega as credenciais salvas dele.
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    # Se não há credenciais ou elas são inválidas (expiradas).
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Se as credenciais expiraram mas podem ser atualizadas, atualiza-as.
            creds.refresh(Request())
        else:
            # Caso contrário, inicia o fluxo de autorização do zero.
            # O usuário precisará autorizar o acesso no navegador.
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Salva as novas credenciais (ou as atualizadas) no arquivo token.json para usos futuros.
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    try:
        # 3. Construção da mensagem de email
        # Cria o objeto de serviço para interagir com a API do Gmail.
        service = build("gmail", "v1", credentials=creds)
        message = None

        # Se um nome de arquivo de anexo foi fornecido...
        if nome_do_arquivo_anexo:
            # ... a mensagem precisa ser do tipo "multipart" para conter texto e anexo.
            message = MIMEMultipart()
            # Anexa o corpo do email como a primeira parte (texto).
            message.attach(MIMEText(corpo_mensagem, "plain"))

            # Lógica robusta para encontrar o arquivo no GCS
            caminho_base_gcs = os.getenv("GCS_ATTACHMENT_PATH", "").strip('/')
            
            # Verifica se o parâmetro recebido já é um caminho completo de GCS (contém bucket e objeto).
            if "/" in nome_do_arquivo_anexo and caminho_base_gcs and nome_do_arquivo_anexo.startswith(caminho_base_gcs.split('/')[0]):
                caminho_completo_do_blob = nome_do_arquivo_anexo
            else:
                # Se for apenas o nome do arquivo, monta o caminho completo usando a variável de ambiente.
                if not caminho_base_gcs:
                    return "Erro de configuração: A variável 'GCS_ATTACHMENT_PATH' não foi encontrada no arquivo .env."
                caminho_completo_do_blob = f"{caminho_base_gcs}/{nome_do_arquivo_anexo}"
            
            # Separa o nome do bucket e o caminho do objeto (blob).
            bucket_name, blob_name = caminho_completo_do_blob.split('/', 1)
            
            # Conecta-se ao Google Cloud Storage.
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            
            # Verifica se o arquivo realmente existe no GCS antes de prosseguir.
            if not blob.exists():
                return f"Erro: O arquivo no caminho '{caminho_completo_do_blob}' não foi encontrado no Google Cloud Storage."
            
            # Baixa o conteúdo do arquivo como bytes.
            file_content = blob.download_as_bytes()
            # Tenta adivinhar o tipo de mídia do arquivo (ex: 'image/jpeg').
            content_type, encoding = mimetypes.guess_type(nome_do_arquivo_anexo)
            if content_type is None or encoding is not None:
                # Se não conseguir adivinhar, usa um tipo genérico.
                content_type = "application/octet-stream"
            main_type, sub_type = content_type.split("/", 1)

            # Cria a parte do anexo (MIMEBase).
            part = MIMEBase(main_type, sub_type)
            # Define o conteúdo do anexo.
            part.set_payload(file_content)
            # Codifica o anexo em Base64, um formato padrão para anexos de email.
            encoders.encode_base64(part)
            # Adiciona o cabeçalho 'Content-Disposition' para que o cliente de email saiba que é um anexo.
            part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(nome_do_arquivo_anexo)}")
            # Anexa a parte do arquivo à mensagem principal.
            message.attach(part)
        else:
            # Se não houver anexo, cria uma mensagem de texto simples.
            message = MIMEText(corpo_mensagem)

        # 4. Definição dos cabeçalhos e envio
        message["To"] = ", ".join(destinatarios) # Concatena a lista de destinatários em uma string.
        message["From"] = "me"                   # "me" é um alias para o usuário autenticado na API do Gmail.
        message["Subject"] = assunto
        
        # Codifica a mensagem inteira em bytes e depois em Base64 segura para URLs.
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        # Cria o corpo da requisição para a API do Gmail.
        create_message = {"raw": encoded_message}
        
        # Chama a API para enviar a mensagem.
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        
        # Constrói uma mensagem de sucesso para o usuário.
        msg_sucesso = f"Email enviado com sucesso para {len(destinatarios)} destinatário(s)."
        if nome_do_arquivo_anexo:
            msg_sucesso += f" Com o anexo '{os.path.basename(nome_do_arquivo_anexo)}'."
            
        return msg_sucesso

    # Captura qualquer erro inesperado durante o processo de envio.
    except Exception as e:
        return f"Ocorreu um erro inesperado: {e}"