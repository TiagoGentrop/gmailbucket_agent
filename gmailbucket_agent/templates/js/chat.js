// Seleciona os elementos principais da página para manipulação.
const chatWindow = document.getElementById('chat-window');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const uploadForm = document.getElementById('upload-form');
const uploadResult = document.getElementById('upload-result');

/**
 * Adiciona uma nova mensagem à janela de chat.
 * @param {string} text - O texto da mensagem.
 * @param {string} sender - 'user' para mensagem do usuário, 'agent' para mensagem do agente.
 */
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + (sender === 'user' ? 'user-message' : 'agent-message');
    messageDiv.innerText = text;
    chatWindow.appendChild(messageDiv);
    // Rola a janela de chat para a parte inferior para mostrar a última mensagem.
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Adiciona um evento para o envio do formulário de upload.
uploadForm.addEventListener('submit', async (event) => {
    event.preventDefault(); // Impede que a página seja recarregada.
    const formData = new FormData(uploadForm);
    uploadResult.innerText = "Enviando para o bucket...";

    try {
        const response = await fetch('/upload', { method: 'POST', body: formData });
        const data = await response.json();
        if (data.success) {
            uploadResult.innerText = `Sucesso! Arquivo '${data.filename}' pronto para ser usado.`;
            // Preenche automaticamente o campo de chat com uma sugestão de comando.
            chatInput.value = `Quero enviar um email com o anexo ${data.filename}`;
        } else {
            uploadResult.innerText = `Erro no upload: ${data.error}`;
        }
    } catch (error) {
        uploadResult.innerText = `Erro de conexão no upload.`;
    }
});

/**
 * Função assíncrona para lidar com o envio de uma mensagem de chat.
 */
async function handleSend() {
    const messageText = chatInput.value.trim();
    if (!messageText) return; // Não faz nada se a mensagem estiver vazia.

    addMessage(messageText, 'user');
    chatInput.value = ''; // Limpa o campo de entrada.
    addMessage("...", 'agent'); // Adiciona uma mensagem de "pensando...".

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: messageText }),
        });
        const data = await response.json();
        
        // Remove a mensagem de "pensando..." antes de adicionar a resposta final.
        chatWindow.removeChild(chatWindow.lastChild);

        if(data.success) {
            addMessage(data.response, 'agent');
        } else {
            addMessage(`Erro do agente: ${data.error}`, 'agent');
        }

    } catch (error) {
        // Remove a mensagem de "pensando..." mesmo se houver um erro de conexão.
        chatWindow.removeChild(chatWindow.lastChild);
        addMessage(`Erro de conexão com o agente.`, 'agent');
    }
}

// Associa a função handleSend ao clique do botão de enviar.
sendBtn.addEventListener('click', handleSend);
// Associa a função handleSend à tecla 'Enter' no campo de texto.
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSend();
});