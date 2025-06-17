# Importa o módulo 'os', que fornece uma maneira de usar funcionalidades dependentes do sistema operacional.
# Usaremos para manipular caminhos de arquivos e diretórios.
import os

# Pega o caminho absoluto do diretório onde este script (verify.py) está localizado.
# __file__ é uma variável especial que contém o caminho para o arquivo de script atual.
# os.path.abspath() converte para um caminho absoluto.
# os.path.dirname() extrai apenas o diretório desse caminho.
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Define o nome do arquivo que estamos procurando.
nome_do_arquivo = "credentials.json"

# Junta o caminho do diretório com o nome do arquivo para criar um caminho completo e independente do sistema operacional.
caminho_completo = os.path.join(diretorio_atual, nome_do_arquivo)

# Imprime um cabeçalho para indicar o início do teste de verificação.
print("--- INICIANDO TESTE DEFINITIVO ---")
# Mostra ao usuário em qual diretório o script está sendo executado.
print(f"Estou neste diretório: {diretorio_atual}")
# Mostra ao usuário o caminho completo do arquivo que está sendo procurado.
print(f"Estou procurando pelo arquivo: {caminho_completo}")
# Imprime uma linha separadora para melhor visualização.
print("-" * 20)

# A função os.path.exists() verifica se um arquivo ou diretório existe no caminho especificado.
if os.path.exists(caminho_completo):
    # Se o arquivo for encontrado, imprime uma mensagem de sucesso.
    print(">>> SUCESSO! O arquivo 'credentials.json' FOI ENCONTRADO.")
else:
    # Se o arquivo não for encontrado, imprime uma mensagem de erro.
    print(">>> ERRO: O arquivo 'credentials.json' NÃO FOI ENCONTRADO neste caminho.")
    # Imprime outra linha separadora.
    print("-" * 20)
    # Tenta fornecer mais informações de depuração para o usuário.
    try:
        # Informa ao usuário que tentará listar o conteúdo da pasta.
        print("Conteúdo da pasta que estou vendo:")
        # os.listdir() retorna uma lista com todos os nomes de arquivos e pastas no diretório especificado.
        # Percorre cada item (arquivo ou pasta) encontrado no diretório atual.
        for item in os.listdir(diretorio_atual):
            # Imprime o nome de cada item encontrado.
            print(f"- {item}")
    # Captura qualquer exceção que possa ocorrer ao tentar listar o diretório (ex: problemas de permissão).
    except Exception as e:
        # Informa ao usuário que houve um erro ao tentar listar os arquivos.
        print(f"Não consegui listar os arquivos da pasta. Erro: {e}")

# Imprime uma mensagem para indicar que o script concluiu sua execução.
print("--- TESTE FINALIZADO ---")