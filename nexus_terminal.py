import tkinter as tk
import customtkinter as ctk
import sys
import importlib.util
from tkinter.scrolledtext import ScrolledText

class RedirectOutput:
    """Redireciona a saída padrão e de erro para o terminal Nexus."""
    def __init__(self, terminal_widget):
        self.terminal_widget = terminal_widget

    def write(self, text):
        if text.strip():  # Apenas exibe texto não vazio
            self.terminal_widget.insert(tk.END, text)
            self.terminal_widget.see(tk.END)

    def flush(self):
        pass  # Necessário para compatibilidade com alguns ambientes

def load_command(command):
    """Carrega o módulo de comandos e executa a função correspondente."""
    try:
        # Caminho para o arquivo de comandos
        comandos_module_path = "comandos/commands_terminal.py"

        spec = importlib.util.spec_from_file_location("comandos", comandos_module_path)
        comandos_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(comandos_module)

        # Verifica se o comando existe no módulo
        if hasattr(comandos_module, command):
            func = getattr(comandos_module, command)
            if callable(func):
                return func  # Retorna a função para execução posterior
            else:
                return f"'{command}' não é uma função."
        else:
            return f"Comando '{command}' desconhecido."
    except Exception as e:
        return f"Erro ao executar o comando: {e}"

def on_terminal_input(event, terminal_text):
    """Manipula a entrada no terminal."""
    user_input = terminal_text.get("insert linestart", "insert lineend").strip()
    if user_input.startswith("Nexus>"):
        command = user_input[6:].strip()  # Remove o prefixo 'Nexus>'
        output = ""

        # Verifica se o comando contém parênteses (indicando que é uma chamada de função)
        if "(" in command and ")" in command:
            command_name = command.split("(")[0].strip()
            try:
                # Tenta pegar os parâmetros da função
                params = command.split("(")[1].split(")")[0]
                params = params.split(",")  # Separa por vírgulas
                params = [param.strip().strip('"').strip("'") for param in params]  # Remove espaços extras e aspas

                # Carrega o comando correspondente
                func = load_command(command_name)
                if callable(func):
                    output = func(*params)  # Passa os parâmetros para a função
                else:
                    output = f"Comando {command_name} não aceitou parâmetros."
            except Exception as e:
                output = f"Erro ao processar parâmetros: {e}"
        else:
            # Quando o comando não contém parênteses, executa a função diretamente
            func = load_command(command)
            if callable(func):
                output = func()  # Chama a função sem parâmetros
            else:
                output = f"Comando '{command}' não é uma função válida."

        terminal_text.insert(tk.END, f"\n{output}\nNexus> ")
        terminal_text.mark_set(tk.INSERT, "end-1c")
        return "break"

def create_terminal():
    """Cria a interface de terminal com prompt Nexus>"""
    root = ctk.CTk()
    root.title("Nexus Terminal")
    root.geometry("800x600")
    root.iconbitmap("icons/icone.ico")

    # Terminal de saída
    terminal_text = ScrolledText(root, wrap=tk.WORD, height=20)
    terminal_text.configure(bg="black", fg="white", font=("Courier", 12))
    terminal_text.pack(fill=tk.BOTH, expand=True)

    # Redireciona saída para o terminal
    sys.stdout = RedirectOutput(terminal_text)
    terminal_text.insert(tk.END, "Nexus> ")

    # Configura o evento para capturar a entrada do terminal
    terminal_text.bind("<Return>", lambda event: on_terminal_input(event, terminal_text))

    # Definir o foco no terminal
    terminal_text.focus_set()
    
    # Inicia o loop principal do Tkinter
    root.mainloop()

# Rodar a interface
create_terminal()
