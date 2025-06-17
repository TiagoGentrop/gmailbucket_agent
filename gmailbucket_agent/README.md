🤖 Agente de E-mail com Gemini e FastAPI
Este projeto implementa um agente de inteligência artificial conversacional, construído com o modelo Gemini do Google através da Vertex AI. O agente é capaz de entender solicitações em linguagem natural para enviar e-mails, incluindo suporte para anexos, através de uma interface web interativa construída com FastAPI.

✨ Features Principais
Envio Conversacional de E-mails: Instrua o agente a enviar um e-mail para um ou mais destinatários com um assunto e corpo de mensagem específicos.
Suporte a Anexos: Faça o upload de arquivos que são armazenados no Google Cloud Storage (GCS) e peça ao agente para anexá-los ao e-mail.
Interface Web Interativa: Um frontend de chat simples e funcional para interagir com o agente.
Autenticação Segura: Utiliza o fluxo OAuth 2.0 do Google para autorizar o envio de e-mails de forma segura, sem expor senhas.
Configuração Flexível: Usa variáveis de ambiente (.env) para gerenciar as configurações do projeto de forma segura.
🚀 Tecnologias Utilizadas
Backend:
Python
FastAPI: Para criar o servidor web e as APIs (/chat, /upload).
Uvicorn: Como servidor ASGI para rodar a aplicação FastAPI.
Inteligência Artificial:
Google Vertex AI: Plataforma para executar o modelo de IA.
Modelo Gemini: O cérebro do agente.
Google Agent Development Kit (ADK): Para estruturar e executar o agente.
Frontend:
HTML5
CSS3
JavaScript
Cloud & Autenticação:
Google Cloud Storage (GCS): Para armazenamento de anexos.
Google OAuth 2.0: Para autenticação com a API do Gmail.
📂 Estrutura do Projeto
agent_gmailgit/
├── agent_gmail/
│   ├── templates/
│   │   ├── css/
│   │   │   └── style.css      # Folha de estilo unificada
│   │   ├── js/
│   │   │   └── chat.js        # Lógica do frontend
│   │   └── chat.html          # Interface principal do chat
│   ├── tools/
│   │   └── funcs.py           # Funções que o agente pode usar (ex: enviar_email)
│   ├── __init__.py
│   ├── agent.py               # Definição do Agente Gemini
│   ├── main.py                # Servidor FastAPI (rotas /chat, /upload, etc)
│   └── prompt.py              # Instruções principais para o agente
├── .env                       # Arquivo para variáveis de ambiente (NÃO ENVIAR PARA O GIT)
├── credentials.json           # Credenciais OAuth do Google (NÃO ENVIAR PARA O GIT)
├── requirements.txt           # Dependências do Python
└── README.md                  # Este arquivo
🛠️ Configuração e Instalação
Siga estes passos para configurar e rodar o projeto localmente.

Pré-requisitos
Python 3.9 ou superior.
Uma conta no Google Cloud com um projeto ativo.
APIs Vertex AI e Gmail API ativadas no seu projeto Google Cloud.
Um bucket no Google Cloud Storage.
Passos
Clonar o Repositório

Bash

git clone <url-do-seu-repositorio>
cd agent_gmailgit
Criar e Ativar Ambiente Virtual

Bash

# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
Instalar as Dependências

Bash

pip install -r requirements.txt
Configurar Credenciais do Google

No Console do Google Cloud, vá para "APIs e Serviços" -> "Credenciais".
Crie uma "ID do cliente OAuth 2.0" do tipo "App da área de trabalho".
Faça o download do arquivo JSON.
Renomeie o arquivo para credentials.json e coloque-o na pasta raiz do projeto (agent_gmailgit/).
Configurar o Arquivo .env

Crie um arquivo chamado .env na raiz do projeto (agent_gmailgit/).
Copie e cole o conteúdo abaixo, substituindo pelos seus valores.
<!-- end list -->

Snippet de código

# .env

# Suas configurações do Google Cloud
GOOGLE_CLOUD_PROJECT="seu-id-de-projeto-aqui"
GOOGLE_CLOUD_LOCATION="us-central1"

# Caminho completo para o seu bucket e pasta no Google Cloud Storage
# Exemplo: gs://meu-bucket-de-anexos/uploads
GCS_ATTACHMENT_PATH="gs://seu-bucket/sua-pasta-de-anexos"
⚡ Como Executar
Rodar o Servidor
No terminal, a partir da pasta raiz (agent_gmailgit), execute:

Bash

python -m agent_gmail.main
Primeira Autenticação (OAuth)

Ao realizar a primeira ação que exige envio de e-mail, uma nova aba será aberta no seu navegador.
Faça login com sua conta do Google e conceda as permissões solicitadas.
Após a autorização, um arquivo token.json será criado na raiz do projeto. Isso só precisa ser feito uma vez.
Acessar a Aplicação

Abra seu navegador e acesse: http://localhost:8001
🚀 Como Usar
A interface de chat será carregada.
Para enviar um anexo:
Use a seção "Anexar um arquivo" para escolher um arquivo do seu computador.
Clique em "1. Fazer Upload". O arquivo será enviado para o Google Cloud Storage.
Uma mensagem de sucesso aparecerá e o campo de texto será preenchido com uma sugestão.
Para enviar um e-mail:
Digite sua solicitação no campo de texto. Por exemplo:
"Enviar um email para fulano@exemplo.com com o assunto 'Relatório Semanal' e corpo 'Segue o relatório.'"
Se você fez o upload de um arquivo, use o comando sugerido: "Quero enviar um email com o anexo relatorio.pdf para ciclano@exemplo.com..."
Pressione "Enviar" e aguarde a resposta do agente.🤖 Agente de E-mail com Gemini e FastAPI
Este projeto implementa um agente de inteligência artificial conversacional, construído com o modelo Gemini do Google através da Vertex AI. O agente é capaz de entender solicitações em linguagem natural para enviar e-mails, incluindo suporte para anexos, através de uma interface web interativa construída com FastAPI.

✨ Features Principais
Envio Conversacional de E-mails: Instrua o agente a enviar um e-mail para um ou mais destinatários com um assunto e corpo de mensagem específicos.
Suporte a Anexos: Faça o upload de arquivos que são armazenados no Google Cloud Storage (GCS) e peça ao agente para anexá-los ao e-mail.
Interface Web Interativa: Um frontend de chat simples e funcional para interagir com o agente.
Autenticação Segura: Utiliza o fluxo OAuth 2.0 do Google para autorizar o envio de e-mails de forma segura, sem expor senhas.
Configuração Flexível: Usa variáveis de ambiente (.env) para gerenciar as configurações do projeto de forma segura.
🚀 Tecnologias Utilizadas
Backend:
Python
FastAPI: Para criar o servidor web e as APIs (/chat, /upload).
Uvicorn: Como servidor ASGI para rodar a aplicação FastAPI.
Inteligência Artificial:
Google Vertex AI: Plataforma para executar o modelo de IA.
Modelo Gemini: O cérebro do agente.
Google Agent Development Kit (ADK): Para estruturar e executar o agente.
Frontend:
HTML5
CSS3
JavaScript
Cloud & Autenticação:
Google Cloud Storage (GCS): Para armazenamento de anexos.
Google OAuth 2.0: Para autenticação com a API do Gmail.
📂 Estrutura do Projeto
agent_gmailgit/
├── agent_gmail/
│   ├── templates/
│   │   ├── css/
│   │   │   └── style.css      # Folha de estilo unificada
│   │   ├── js/
│   │   │   └── chat.js        # Lógica do frontend
│   │   └── chat.html          # Interface principal do chat
│   ├── tools/
│   │   └── funcs.py           # Funções que o agente pode usar (ex: enviar_email)
│   ├── __init__.py
│   ├── agent.py               # Definição do Agente Gemini
│   ├── main.py                # Servidor FastAPI (rotas /chat, /upload, etc)
│   └── prompt.py              # Instruções principais para o agente
├── .env                       # Arquivo para variáveis de ambiente (NÃO ENVIAR PARA O GIT)
├── credentials.json           # Credenciais OAuth do Google (NÃO ENVIAR PARA O GIT)
├── requirements.txt           # Dependências do Python
└── README.md                  # Este arquivo
🛠️ Configuração e Instalação
Siga estes passos para configurar e rodar o projeto localmente.

Pré-requisitos
Python 3.9 ou superior.
Uma conta no Google Cloud com um projeto ativo.
APIs Vertex AI e Gmail API ativadas no seu projeto Google Cloud.
Um bucket no Google Cloud Storage.
Passos
Clonar o Repositório

Bash

git clone <url-do-seu-repositorio>
cd agent_gmailgit
Criar e Ativar Ambiente Virtual

Bash

# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
Instalar as Dependências

Bash

pip install -r requirements.txt
Configurar Credenciais do Google

No Console do Google Cloud, vá para "APIs e Serviços" -> "Credenciais".
Crie uma "ID do cliente OAuth 2.0" do tipo "App da área de trabalho".
Faça o download do arquivo JSON.
Renomeie o arquivo para credentials.json e coloque-o na pasta raiz do projeto (agent_gmailgit/).
Configurar o Arquivo .env

Crie um arquivo chamado .env na raiz do projeto (agent_gmailgit/).
Copie e cole o conteúdo abaixo, substituindo pelos seus valores.
<!-- end list -->

Snippet de código

# .env

# Suas configurações do Google Cloud
GOOGLE_CLOUD_PROJECT="seu-id-de-projeto-aqui"
GOOGLE_CLOUD_LOCATION="us-central1"

# Caminho completo para o seu bucket e pasta no Google Cloud Storage
# Exemplo: gs://meu-bucket-de-anexos/uploads
GCS_ATTACHMENT_PATH="gs://seu-bucket/sua-pasta-de-anexos"
⚡ Como Executar
Rodar o Servidor
No terminal, a partir da pasta raiz (agent_gmailgit), execute:

Bash

python -m agent_gmail.main
Primeira Autenticação (OAuth)

Ao realizar a primeira ação que exige envio de e-mail, uma nova aba será aberta no seu navegador.
Faça login com sua conta do Google e conceda as permissões solicitadas.
Após a autorização, um arquivo token.json será criado na raiz do projeto. Isso só precisa ser feito uma vez.
Acessar a Aplicação

Abra seu navegador e acesse: http://localhost:8001
🚀 Como Usar
A interface de chat será carregada.
Para enviar um anexo:
Use a seção "Anexar um arquivo" para escolher um arquivo do seu computador.
Clique em "1. Fazer Upload". O arquivo será enviado para o Google Cloud Storage.
Uma mensagem de sucesso aparecerá e o campo de texto será preenchido com uma sugestão.
Para enviar um e-mail:
Digite sua solicitação no campo de texto. Por exemplo:
"Enviar um email para fulano@exemplo.com com o assunto 'Relatório Semanal' e corpo 'Segue o relatório.'"
Se você fez o upload de um arquivo, use o comando sugerido: "Quero enviar um email com o anexo relatorio.pdf para ciclano@exemplo.com..."
Pressione "Enviar" e aguarde a resposta do agente.