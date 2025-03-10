# commands_terminal.py

import socket
import os
import requests

def hello():
    """
    Retorna uma saudação para o Nexus.
    """
    return "Hello Nexus!"

def ipconfig():
    """
    Retorna o IP local da máquina e o nome do usuário logado.
    """
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        username = os.getlogin()
        return f"Your local IP is {local_ip}, and the user logged in is {username}."
    except Exception as e:
        return f"Erro ao obter informações: {e}"

def publicip():
    """
    Retorna o IP público da máquina.
    """
    try:
        response = requests.get('https://api.ipify.org?format=json')
        return response.json().get('ip')
    except Exception as e:
        return f"Erro ao obter IP público: {e}"

def ls():
    """
    Retorna a lista de arquivos e pastas no diretório atual.
    """
    return '\n'.join(os.listdir())

def pwd():
    """
    Retorna o caminho do diretório atual.
    """
    return os.getcwd()

def check_internet():
    """
    Verifica se a máquina está conectada à internet.
    """
    try:
        response = os.system("ping -c 1 google.com")
        if response == 0:
            return "Conectado à Internet."
        else:
            return "Sem conexão com a Internet."
    except Exception as e:
        return f"Erro ao verificar a conexão com a Internet: {e}"

def create_directory(directory_name):
    """
    Cria um diretório com o nome especificado.
    """
    try:
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
            return f"Diretório '{directory_name}' criado com sucesso!"
        else:
            return f"O diretório '{directory_name}' já existe."
    except Exception as e:
        return f"Erro ao criar o diretório: {e}"

def open_file():
    """
    Lê o conteúdo de um arquivo chamado 'code.txt' no diretório atual.
    """
    try:
        with open("code.txt", "r") as f:
            open_file_content = f.read()
        return open_file_content
    except Exception as e:
        return f"Erro ao abrir o arquivo: {e}"
