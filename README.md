# 🤖 Agente de E-mail com Gemini e FastAPI

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green.svg)
![Vertex AI](https://img.shields.io/badge/Vertex%20AI-Gemini-purple.svg)

Este projeto implementa um agente de inteligência artificial conversacional, construído com o modelo Gemini do Google através da Vertex AI. O agente é capaz de entender solicitações em linguagem natural para enviar e-mails.

O projeto utiliza uma arquitetura híbrida:
1.  **`adk-web`**: Fornece uma interface de chat robusta para interagir com o agente.
2.  **FastAPI**: Um servidor dedicado atua como um microserviço para lidar com o upload de anexos para o Google Cloud Storage.

## ✨ Features Principais

-   **Envio Conversacional de E-mails:** Instrua o agente a enviar um e-mail para um ou mais destinatários com um assunto e corpo de mensagem específicos.
-   **Suporte a Anexos:** Um endpoint de API dedicado para fazer o upload de arquivos para o Google Cloud Storage (GCS), que podem ser usados pelo agente.
-   **Interface Web Gerada:** A interface de chat é servida pela ferramenta `adk-web`.
-   **Autenticação Segura:** Utiliza o fluxo OAuth 2.0 do Google para autorizar o envio de e-mails de forma segura, sem expor senhas.
-   **Configuração Flexível:** Usa variáveis de ambiente (`.env`) para gerenciar as configurações do projeto de forma segura.

## 🚀 Tecnologias Utilizadas

-   **Backend (Lógica do Agente):**
    -   Python
-   **Inteligência Artificial:**
    -   Google Vertex AI
    -   Modelo Gemini
    -   Google Agent Development Kit (ADK)
-   **Servidor de API (Upload):**
    -   FastAPI
    -   Uvicorn
-   **Servidor e Frontend (Chat):**
    -   `adk-web`
-   **Cloud & Autenticação:**
    -   Google Cloud Storage (GCS)
    -   Google OAuth 2.0

## 📂 Estrutura do Projeto

```
gmailbucket_agent/
├── tools/
│   └── funcs.py           # Ferramentas do agente (ex: enviar_email)
├── agent.py               # Definição principal do Agente Gemini
├── main.py                # Servidor FastAPI com o endpoint /upload
└── prompt.py              # Instruções (prompt) para o agente

# Arquivos de configuração na raiz
.env
credentials.json
requirements.txt
README.md
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
    git clone [https://github.com/TiagoGentrop/gmailbucket_agent.git](https://github.com/TiagoGentrop/gmailbucket_agent.git)
    cd gmailbucket_agent
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

    - Verifique se seu arquivo `requirements.txt` contém `fastapi`, `uvicorn` e `google-adk-web`.
    - Execute o comando:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Credenciais do Google**
    -   No Console do Google Cloud, vá para "APIs e Serviços" -> "Credenciais".
    -   Crie uma "ID do cliente OAuth 2.0" do tipo "App da área de trabalho".
    -   Faça o download do arquivo JSON, renomeie para `credentials.json` e coloque-o na pasta raiz do projeto.

5.  **Configurar o Arquivo `.env`**
    -   Crie um arquivo `.env` na raiz do projeto.
    -   Copie e cole o conteúdo abaixo, substituindo pelos seus valores.

    ```ini
    # Suas configurações do Google Cloud
    GOOGLE_CLOUD_PROJECT="seu-id-de-projeto-aqui"
    GOOGLE_CLOUD_LOCATION="us-central1"

    # Caminho completo para o seu bucket e pasta no Google Cloud Storage
    GCS_ATTACHMENT_PATH="gs://seu-bucket/sua-pasta-de-anexos"
    ```

## ⚡ Como Executar (Arquitetura Híbrida)

Este projeto utiliza dois servidores que devem ser executados **simultaneamente**. A melhor forma de fazer isso é usando **dois terminais separados**.

---

### **Terminal 1: Iniciar o Servidor de Upload (FastAPI)**

Este servidor lida apenas com o upload de arquivos para o Google Cloud Storage.

1.  Abra um terminal na pasta raiz do projeto.
2.  Ative o ambiente virtual (`.\venv\Scripts\activate`).
3.  Execute o comando:
    ```bash
    python -m gmailbucket_agent.main
    ```
4.  Este servidor estará rodando na porta `8001` (por padrão). Deixe este terminal aberto.

---

### **Terminal 2: Iniciar o Servidor do Agente e Chat (`adk-web`)**

Este servidor executa o agente e fornece a interface de chat para você interagir.

1.  Abra um **segundo** terminal na pasta raiz do projeto.
2.  Ative o ambiente virtual (`.\venv\Scripts\activate`).
3.  Execute o comando:
    ```bash
    adk-web
    ```
4.  Este servidor estará rodando na porta `8000` (por padrão). Deixe este terminal aberto também.

---

### **Acessando e Usando a Aplicação**

1.  **Acesse a Interface de Chat**
    -   Para interagir com o agente, abra a URL do servidor `adk-web` no seu navegador: `http://localhost:8080`

2.  **Upload de Arquivos**
    -   A interface de chat servida pelo `adk-web` está configurada para usar o endpoint de upload (`http://localhost:8001/upload`) fornecido pelo outro servidor (FastAPI). Use a função de upload na interface para enviar seus anexos.

3.  **Interaja com o Agente**
    -   Converse com o agente para enviar e-mails, mencionando os arquivos que você enviou por upload.
