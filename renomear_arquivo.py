import PyPDF2
import os
import re
import tkinter as tk
from tkinter import filedialog

def encontrar_nome(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text = page.extract_text()
            match = re.search(r'\d{3}\.\d{3}\.\d{3}-\d{2}\s+(.+)', text)
            if match:
                return match.group(1).strip()
    return None

def renomear_pdf(pdf_path, novo_nome):
    diretorio, nome_arquivo = os.path.split(pdf_path)
    novo_nome = "".join(c for c in novo_nome if c.isalpha() or c in [' ', '.', '_', '-']) # Remove caracteres não alfabéticos do nome do arquivo
    novo_nome_arquivo = os.path.join(diretorio, f"{novo_nome}.pdf")
    try:
        os.rename(pdf_path, novo_nome_arquivo)
        resultado_texto.insert(tk.END, f"Arquivo renomeado para: {novo_nome_arquivo}\n")
    except FileNotFoundError:
        resultado_texto.insert(tk.END, f"O arquivo '{pdf_path}' não foi encontrado.\n")
    except OSError as e:
        resultado_texto.insert(tk.END, f"Erro ao renomear o arquivo '{pdf_path}': {e}\n")

def selecionar_pasta():
    pasta = filedialog.askdirectory()
    pasta_texto.delete(0, tk.END)
    pasta_texto.insert(0, pasta)

def renomear_arquivos():
    pasta = pasta_texto.get()
    if not os.path.isdir(pasta):
        resultado_texto.insert(tk.END, f"O caminho '{pasta}' não é um diretório válido.\n")
        return
    
    resultado_texto.delete(1.0, tk.END)
    
    for nome_arquivo in os.listdir(pasta):
        if nome_arquivo.endswith('.pdf'):
            pdf_path = os.path.join(pasta, nome_arquivo)
            nome = encontrar_nome(pdf_path)
            if nome:
                renomear_pdf(pdf_path, nome)
            else:
                resultado_texto.insert(tk.END, f"Nome não encontrado no arquivo '{nome_arquivo}'.\n")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Renomeador de PDFs")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

pasta_label = tk.Label(frame, text="Caminho da Pasta:")
pasta_label.grid(row=0, column=0, sticky="w")

pasta_texto = tk.Entry(frame, width=50)
pasta_texto.grid(row=0, column=1, padx=5, pady=5)

selecionar_button = tk.Button(frame, text="Selecionar", command=selecionar_pasta)
selecionar_button.grid(row=0, column=2, padx=5, pady=5)

renomear_button = tk.Button(frame, text="Renomear Arquivos", command=renomear_arquivos)
renomear_button.grid(row=1, column=0, columnspan=3, pady=10)

resultado_texto = tk.Text(frame, height=10, width=70)
resultado_texto.grid(row=2, column=0, columnspan=3, pady=10)

root.mainloop()
