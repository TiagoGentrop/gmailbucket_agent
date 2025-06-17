document.getElementById('upload-form').addEventListener('submit', async (event) => {
    // Impede o comportamento padrão do formulário (que recarregaria a página).
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const resultDiv = document.getElementById('result');
    
    // Mostra uma mensagem de "Enviando..." enquanto a requisição está em andamento.
    resultDiv.innerHTML = "Enviando...";
    resultDiv.className = ''; // Limpa classes de erro/sucesso anteriores.

    try {
        // Envia os dados do formulário para o endpoint '/upload' usando o método POST.
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData,
        });

        // Converte a resposta do servidor de JSON para um objeto JavaScript.
        const data = await response.json();

        if (data.success) {
            // Se o upload foi bem-sucedido, exibe a mensagem de sucesso e o nome do arquivo.
            resultDiv.innerHTML = `<b>Sucesso!</b><br>Arquivo enviado. Agora, na conversa com o agente, diga que quer anexar o arquivo: <br><b><code>${data.filename}</code></b>`;
            resultDiv.className = 'success';
        } else {
            // Se o servidor retornou um erro, exibe a mensagem de erro.
            resultDiv.innerHTML = `<b>Erro:</b> ${data.error}`;
            resultDiv.className = 'error';
        }
    } catch (error) {
        // Se ocorreu um erro de rede ou conexão, exibe uma mensagem de erro genérica.
        resultDiv.innerHTML = `<b>Erro de conexão:</b> ${error}`;
        resultDiv.className = 'error';
    }
});