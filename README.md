# 🤖 Agente de E-mail com Gemini e FastAPI

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green.svg)
![Vertex AI](https://img.shields.io/badge/Vertex%20AI-Gemini-purple.svg)

Este projeto implementa um agente de inteligência artificial conversacional, construído com o modelo Gemini do Google através da Vertex AI. O agente é capaz de entender solicitações em linguagem natural para enviar e-mails, incluindo suporte para anexos, através de uma interface web interativa construída com FastAPI.

## ✨ Features Principais

-   **Envio Conversacional de E-mails:** Instrua o agente a enviar um e-mail para um ou mais destinatários com um assunto e corpo de mensagem específicos.
-   **Suporte a Anexos:** Faça o upload de arquivos que são armazenados no Google Cloud Storage (GCS) e peça ao agente para anexá-los ao e-mail.
-   **Interface Web Interativa:** Um frontend de chat simples e funcional para interagir com o agente.
-   **Autenticação Segura:** Utiliza o fluxo OAuth 2.0 do Google para autorizar o envio de e-mails de forma segura, sem expor senhas.
-   **Configuração Flexível:** Usa variáveis de ambiente (`.env`) para gerenciar as configurações do projeto de forma segura.

## 🚀 Tecnologias Utilizadas

-   **Backend:**
    -   Python
    -   FastAPI: Para criar o servidor web e as APIs (`/chat`, `/upload`).
    -   Uvicorn: Como servidor ASGI para rodar a aplicação FastAPI.
-   **Inteligência Artificial:**
    -   Google Vertex AI
    -   Modelo Gemini
    -   Google Agent Development Kit (ADK)
-   **Frontend:**
    -   HTML5, CSS3, JavaScript
-   **Cloud & Autenticação:**
    -   Google Cloud Storage (GCS)
    -   Google OAuth 2.0

## 📂 Estrutura do Projeto

```
agent_gmailgit/
├── agent_gmail/
│   ├── templates/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── chat.js
│   │   └── chat.html
│   ├── tools/
│   │   └── funcs.py
│   ├── __init__.py
│   ├── agent.py
│   ├── main.py
│   └── prompt.py
├── .env
├── credentials.json
├── requirements.txt
└── README.md
```

## 🛠️ Configuração e Instalação

### Pré-requisitos

-   Python 3.9 ou superior.
-   Uma conta no Google Cloud com um projeto ativo.
-   APIs **Vertex AI** e **Gmail API** ativadas no seu projeto Google Cloud.
-   Um bucket no **Google Cloud Storage**.

### Passos

1.  **Clonar o Repositório**
    ```bash
    git clone <url-do-seu-repositorio>
    cd agent_gmailgit
    ```

2.  **Criar e Ativar Ambiente Virtual**

    *Windows:*
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

    *macOS / Linux:*
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar as Dependências**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Credenciais do Google**
    -   No Console do Google Cloud, vá para "APIs e Serviços" -> "Credenciais".
    -   Crie uma "ID do cliente OAuth 2.0" do tipo "App da área de trabalho".
    -   Faça o download do arquivo JSON.
    -   Renomeie o arquivo para `credentials.json` e coloque-o na pasta raiz do projeto.

5.  **Configurar o Arquivo `.env`**
    -   Crie um arquivo chamado `.env` na raiz do projeto.
    -   Copie e cole o conteúdo abaixo, substituindo pelos seus valores.

    ```ini
    # Suas configurações do Google Cloud
    GOOGLE_CLOUD_PROJECT="seu-id-de-projeto-aqui"
    GOOGLE_CLOUD_LOCATION="us-central1"

    # Caminho completo para o seu bucket e pasta no Google Cloud Storage
    # Exemplo: gs://meu-bucket-de-anexos/uploads
    GCS_ATTACHMENT_PATH="gs://seu-bucket/sua-pasta-de-anexos"
    ```

## ⚡ Como Executar

1.  **Rodar o Servidor**
    No terminal, a partir da pasta raiz do projeto, execute:
    ```bash
    python -m gmailbucket_agent.main
    ```

2.  **Primeira Autenticação (OAuth)**
    -   Na primeira vez que o agente precisar enviar um e-mail, uma aba do navegador será aberta.
    -   Faça login com sua conta Google e conceda as permissões.
    -   Um arquivo `token.json` será criado na raiz do projeto para salvar sua autorização.

3.  **Acessar a Aplicação**
    -   Abra seu navegador e acesse: `http://localhost:8001`

## 🚀 Como Usar

1.  Acesse a interface de chat no seu navegador.
2.  **Para enviar um anexo:**
    -   Use a seção "Anexar um arquivo" para fazer o upload de um arquivo.
    -   Uma mensagem de sucesso aparecerá com uma sugestão de comando.
3.  **Para enviar um e-mail:**
    -   Digite sua solicitação na caixa de texto.
    -   *Exemplo sem anexo:* `"Enviar um email para fulano@exemplo.com com o assunto 'Reunião' e corpo 'Olá, a reunião está confirmada.'"`
    -   *Exemplo com anexo:* `"Quero enviar um email com o anexo relatorio.pdf para ciclano@exemplo.com com o assunto 'Relatório Mensal'"`
    -   Clique em "Enviar" e aguarde a confirmação do agente.
