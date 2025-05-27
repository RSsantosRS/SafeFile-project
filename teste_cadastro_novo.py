import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
import sqlite3
import hashlib

# --- Constantes ---
CPF_PLACEHOLDER_TEXT = "somente números..."
CPF_PLACEHOLDER_COLOR = "grey"
CPF_NORMAL_TEXT_COLOR = "black"
CAMINHO_BANCO = "banco_documento.sqlite"

# --- Funções de navegação ---
def ir_para_inicio_da_tela_cadastro():
    try:
        script_dir = os.path.dirname(__file__)
        caminho_inicio_py = os.path.join(script_dir, "inicio.py")

        if os.path.exists(caminho_inicio_py):
            janela_cadastro.destroy()
            subprocess.Popen([sys.executable, caminho_inicio_py])
        else:
            messagebox.showerror("Erro", f"Arquivo 'inicio.py' não encontrado:\n{caminho_inicio_py}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao iniciar 'inicio.py':\n{e}")

# --- Banco de dados ---
def cadastrar_usuario(nome, email, senha, cpf):
    try:
        conexao = sqlite3.connect(CAMINHO_BANCO)
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO Usuario (cpf, nome, email, senha) VALUES (?, ?, ?, ?)", (cpf, nome, email, senha))
        conexao.commit()
        conexao.close()
        return True, "Usuário cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "CPF já cadastrado. Use outro CPF."
    except Exception as e:
        return False, f"Erro ao cadastrar: {e}"

# Função para gerar hash da senha
def gerar_hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# --- Lógica do cadastro ---
def processar_cadastro():
    nome = entry_nome.get().strip()
    email = entry_email.get().strip()
    senha = entry_senha.get().strip()
    cpf_valor = entry_cpf.get().strip()
    cpf_final = "" if cpf_valor == CPF_PLACEHOLDER_TEXT else cpf_valor

    if not nome or not email or not senha or not cpf_final:
        messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos.")
        return

    if cpf_final and not cpf_final.isdigit():
        messagebox.showwarning("CPF Inválido", "O CPF deve conter apenas números.")
        return

    print("--- Dados do Cadastro ---")
    print(f"Nome Completo: {nome}")
    print(f"Email: {email}")
    print(f"Senha: {senha}")  # Aqui o print da senha original
    print(f"CPF: {cpf_final}")

    senha_hash = gerar_hash_senha(senha)  # Gerar hash da senha antes de salvar no banco

    sucesso, mensagem = cadastrar_usuario(nome, email, senha_hash, cpf_final)  # Passa o hash para salvar

    if sucesso:
        messagebox.showinfo("Cadastro", mensagem)
        janela_cadastro.destroy()
        try:
            caminho_login_py = os.path.join(os.path.dirname(__file__), "login.py")
            if os.path.exists(caminho_login_py):
                subprocess.Popen([sys.executable, caminho_login_py])
            else:
                print(f"Arquivo login.py não encontrado: {caminho_login_py}")
        except Exception as e:
            print(f"Erro ao abrir login.py: {e}")
    else:
        messagebox.showerror("Erro", mensagem)

# --- Placeholder do CPF ---
def on_cpf_focus_in(event):
    if entry_cpf.get() == CPF_PLACEHOLDER_TEXT:
        entry_cpf.delete(0, tk.END)
        entry_cpf.config(fg=CPF_NORMAL_TEXT_COLOR)

def on_cpf_focus_out(event):
    if not entry_cpf.get():
        entry_cpf.insert(0, CPF_PLACEHOLDER_TEXT)
        entry_cpf.config(fg=CPF_PLACEHOLDER_COLOR)

# --- Janela Principal ---
janela_cadastro = tk.Tk()
janela_cadastro.title("SafeFile - Cadastro")
janela_cadastro.geometry("800x600")
janela_cadastro.resizable(False, False)

# --- Cores e fontes ---
cor_azul_claro = "#80DEEA"
cor_azul_escuro = "#3161E6"
cor_label_campo = "white"
cor_botao_principal_bg = "#FFFFFF"
cor_botao_principal_fg_text = "#5C00A4"
cor_botao_secundario_fg_text = "white"
cor_fundo_botao_secundario = cor_azul_escuro

fonte_titulo_str = ("Arial", 36, "bold")
fonte_label_campo_str = ("Arial", 12)
fonte_entry_str = ("Arial", 12)
fonte_botao_cadastrar_str = ("Arial", 16, "bold")
fonte_botao_voltar_str = ("Arial", 12)

# --- Canvas com gradiente ---
canvas_fundo = tk.Canvas(janela_cadastro, highlightthickness=0)
canvas_fundo.pack(fill="both", expand=True)

def desenhar_titulo():
    canvas_fundo.delete("titulo")
    canvas_fundo.create_text(
        400, 72,
        text="SafeFile",
        font=fonte_titulo_str,
        fill="white",
        tags="titulo"
    )

def desenhar_gradiente(event=None):
    canvas_fundo.delete("gradient")
    w = canvas_fundo.winfo_width()
    h = canvas_fundo.winfo_height()
    r1, g1, b1 = [x//256 for x in janela_cadastro.winfo_rgb(cor_azul_escuro)]
    r2, g2, b2 = [x//256 for x in janela_cadastro.winfo_rgb(cor_azul_claro)]

    for i in range(w):
        r = int(r1 + (r2 - r1) * (i / w))
        g = int(g1 + (g2 - g1) * (i / w))
        b = int(b1 + (b2 - b1) * (i / w))
        cor = f'#{r:02x}{g:02x}{b:02x}'
        canvas_fundo.create_line(i, 0, i, h, fill=cor, tags="gradient")
    desenhar_titulo()

canvas_fundo.bind("<Configure>", desenhar_gradiente)

# --- Layout campos ---
def adicionar_label_entry(texto, y_label, y_entry):
    label = tk.Label(janela_cadastro, text=texto, font=fonte_label_campo_str, fg=cor_label_campo, bg=cor_azul_escuro)
    label.place(relx=0.5, rely=y_label, anchor="center", width=400)
    entry = tk.Entry(janela_cadastro, font=fonte_entry_str, width=40)
    entry.place(relx=0.5, rely=y_entry, anchor="center", width=400, height=35)
    return entry

entry_nome = adicionar_label_entry("Nome Completo:", 0.25, 0.30)
entry_email = adicionar_label_entry("Email:", 0.36, 0.41)
entry_senha = adicionar_label_entry("Senha:", 0.47, 0.52)
entry_senha.config(show="*")

label_cpf = tk.Label(janela_cadastro, text="CPF:", font=fonte_label_campo_str, fg=cor_label_campo, bg=cor_azul_escuro)
label_cpf.place(relx=0.5, rely=0.58, anchor="center", width=400)
entry_cpf = tk.Entry(janela_cadastro, font=fonte_entry_str, fg=CPF_PLACEHOLDER_COLOR, width=40)
entry_cpf.insert(0, CPF_PLACEHOLDER_TEXT)
entry_cpf.bind("<FocusIn>", on_cpf_focus_in)
entry_cpf.bind("<FocusOut>", on_cpf_focus_out)
entry_cpf.place(relx=0.5, rely=0.63, anchor="center", width=400, height=35)

# --- Botões ---
botao_cadastrar = tk.Button(
    janela_cadastro,
    text="Cadastrar",
    font=fonte_botao_cadastrar_str,
    fg=cor_botao_principal_fg_text,
    bg=cor_botao_principal_bg,
    command=processar_cadastro,
    relief=tk.FLAT
)
botao_cadastrar.place(relx=0.5, rely=0.73, anchor="center", width=230, height=50)

botao_voltar = tk.Button(
    janela_cadastro,
    text="Voltar",
    font=fonte_botao_voltar_str,
    fg=cor_botao_secundario_fg_text,
    bg=cor_fundo_botao_secundario,
    command=ir_para_inicio_da_tela_cadastro,
    relief=tk.FLAT
)
botao_voltar.place(relx=0.5, rely=0.81, anchor="center", width=230, height=45)

# --- Loop principal ---
janela_cadastro.mainloop()
