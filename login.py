import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox
import subprocess
import sys
import os
import sqlite3
import hashlib

# --- Função para gerar hash SHA-256 da senha ---
def gerar_hash_senha(senha):
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

# --- Função para o botão "Login" ---
def processar_login():
    email = entry_email.get().strip()
    senha = entry_senha.get().strip()

    if not email or not senha:
        messagebox.showwarning("Campos Vazios", "Por favor, preencha seu email e senha.")
        return

    try:
        # Ajuste o caminho se o banco de dados não estiver no mesmo diretório do script
        db_path = os.path.join(os.path.dirname(__file__), "banco_documento.sqlite")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT nome, senha FROM Usuario WHERE email = ?", (email,))
        resultado = cursor.fetchone()

        if resultado:
            nome_db, senha_hash_db = resultado
            senha_hash_digitada = gerar_hash_senha(senha)
            if senha_hash_db == senha_hash_digitada:
                messagebox.showinfo("Login Bem-Sucedido", f"Bem-vindo, {nome_db}!")
                print(f"Login bem-sucedido para o usuário: {nome_db}")
                
                # Tenta abrir o gerenciador.py
                try:
                    script_dir = os.path.dirname(__file__)
                    caminho_gerenciador_py = os.path.join(script_dir, "gerenciador.py")

                    if os.path.exists(caminho_gerenciador_py):
                        # Abre gerenciador.py e passa o nome do usuário como argumento
                        subprocess.Popen([sys.executable, caminho_gerenciador_py, nome_db])
                        janela_login.destroy() # Fecha a janela de login
                    else:
                        messagebox.showerror("Erro de Navegação", f"Arquivo 'gerenciador.py' não encontrado em:\n{caminho_gerenciador_py}")
                except Exception as e:
                    messagebox.showerror("Erro ao Abrir Gerenciador", f"Não foi possível iniciar 'gerenciador.py':\n{e}")
            else:
                messagebox.showerror("Erro", "Senha incorreta.")
        else:
            messagebox.showerror("Erro", "Email não encontrado.")

        conn.close()
    except sqlite3.Error as e_sql:
        messagebox.showerror("Erro de Banco de Dados", f"Erro ao acessar o banco de dados:\n{e_sql}\nVerifique se o arquivo 'banco_documento.sqlite' existe no local correto e não está corrompido.")
    except Exception as e:
        messagebox.showerror("Erro Inesperado", f"Ocorreu um erro:\n{e}")

# --- Funções de Navegação ---
def ir_para_cadastro_desta_tela():
    """Fecha a janela de login e abre a tela de cadastro."""
    print("Redirecionando para a tela de cadastro...")
    try:
        script_dir = os.path.dirname(__file__)
        caminho_cadastro_py = os.path.join(script_dir, "cadastro.py") # Supondo que cadastro.py está no mesmo diretório

        if os.path.exists(caminho_cadastro_py):
            janela_login.destroy() # Fecha a janela de login atual
            subprocess.Popen([sys.executable, caminho_cadastro_py])
            print(f"Executando '{caminho_cadastro_py}'")
        else:
            messagebox.showerror("Erro de Navegação", f"Arquivo 'cadastro.py' não encontrado em:\n{caminho_cadastro_py}")
    except Exception as e:
        messagebox.showerror("Erro de Navegação", f"Não foi possível iniciar a tela de cadastro:\n{e}")

def ir_para_inicio_da_tela_login():
    """Fecha a janela de login e abre a tela de início."""
    print("Redirecionando para a tela de início...")
    try:
        script_dir = os.path.dirname(__file__)
        caminho_inicio_py = os.path.join(script_dir, "inicio.py") # Supondo que inicio.py está no mesmo diretório

        if os.path.exists(caminho_inicio_py):
            janela_login.destroy() # Fecha a janela de login atual
            subprocess.Popen([sys.executable, caminho_inicio_py])
            print(f"Navegando para '{caminho_inicio_py}'")
        else:
            messagebox.showerror("Erro de Navegação", f"Arquivo 'inicio.py' não encontrado em:\n{caminho_inicio_py}")
    except Exception as e:
        messagebox.showerror("Erro de Navegação", f"Não foi possível iniciar 'inicio.py':\n{e}")

# --- Configurações da Janela Principal ---
janela_login = tk.Tk()
janela_login.title("SafeFile - Login")
LARGURA_JANELA = 800
ALTURA_JANELA = 600
janela_login.geometry(f"{LARGURA_JANELA}x{ALTURA_JANELA}")
janela_login.resizable(False, False)

# --- Cores ---
cor_azul_claro = "#80DEEA"
cor_azul_escuro = "#3161E6"
cor_texto_titulo = "white"
cor_label_campo = "white"
cor_botao_principal_bg = "#FFFFFF" # Fundo do botão "Login"
cor_botao_principal_fg_text = "#5C00A4" # Texto do botão "Login" (roxo)
cor_botao_secundario_fg_text = "white" # Para os botões "Cadastre-se" e "Voltar"
cor_fundo_botao_secundario = cor_azul_escuro # Fundo para os botões "Cadastre-se" e "Voltar"

# --- Fontes ---
fonte_titulo_str = ("Arial", 36, "bold")
fonte_label_campo_str = ("Arial", 12)
fonte_entry_str = ("Arial", 12)
fonte_botao_login_str = ("Arial", 16, "bold") # Para o botão "Login"
fonte_botao_secundario_str = ("Arial", 12) # Fonte comum para botões secundários

# --- Canvas para o Gradiente de Fundo ---
canvas_fundo = tk.Canvas(janela_login, highlightthickness=0)
canvas_fundo.pack(fill="both", expand=True)

def desenhar_titulo_no_canvas():
    canvas_fundo.delete("titulo_safefile")
    canvas_fundo.create_text(
        LARGURA_JANELA / 2,
        ALTURA_JANELA * 0.18,  # Ajustado um pouco para cima para mais espaço abaixo
        text="SafeFile",
        font=fonte_titulo_str,
        fill=cor_texto_titulo,
        tags="titulo_safefile",
        anchor="center"
    )

def desenhar_gradiente(event=None):
    canvas_fundo.delete("gradient")
    largura_canvas = LARGURA_JANELA # Usar dimensões fixas da janela
    altura_canvas = ALTURA_JANELA  # Usar dimensões fixas da janela

    if largura_canvas == 1 or altura_canvas == 1: # Evita erro se for 0,0 (winfo_width pode ser 1 inicialmente)
        largura_canvas = janela_login.winfo_width()
        altura_canvas = janela_login.winfo_height()
        if largura_canvas <= 1 or altura_canvas <= 1 : return


    r1, g1, b1 = janela_login.winfo_rgb(cor_azul_escuro)[0]//256, janela_login.winfo_rgb(cor_azul_escuro)[1]//256, janela_login.winfo_rgb(cor_azul_escuro)[2]//256
    r2, g2, b2 = janela_login.winfo_rgb(cor_azul_claro)[0]//256, janela_login.winfo_rgb(cor_azul_claro)[1]//256, janela_login.winfo_rgb(cor_azul_claro)[2]//256

    for i in range(largura_canvas):
        r = int(r1 + (r2 - r1) * (i / largura_canvas))
        g = int(g1 + (g2 - g1) * (i / largura_canvas))
        b = int(b1 + (b2 - b1) * (i / largura_canvas))
        cor = f'#{r:02x}{g:02x}{b:02x}'
        canvas_fundo.create_line(i, 0, i, altura_canvas, fill=cor, tags="gradient")
    desenhar_titulo_no_canvas() # Redesenha o título sobre o novo gradiente

# --- Chamada inicial para desenhar e bind para redimensionar ---
# Para garantir que o gradiente seja desenhado corretamente na inicialização
janela_login.update_idletasks() 
desenhar_gradiente()
# Se a janela fosse redimensionável, este bind seria mais útil.
# Como é fixa, o desenho inicial após update_idletasks é o mais importante.
canvas_fundo.bind("<Configure>", desenhar_gradiente)


# --- Campos de Login ---
y_pos_label_email = 0.35
y_pos_entry_email = 0.40
y_pos_label_senha = 0.48
y_pos_entry_senha = 0.53

largura_campos = LARGURA_JANELA * 0.5
altura_campos = 35

# Email
label_email = tk.Label(janela_login, text="Email:", font=fonte_label_campo_str, fg=cor_label_campo, bg=cor_azul_escuro)
label_email.place(relx=0.5, rely=y_pos_label_email, anchor="center", width=largura_campos)
entry_email = tk.Entry(janela_login, font=fonte_entry_str, width=40)
entry_email.place(relx=0.5, rely=y_pos_entry_email, anchor="center", width=largura_campos, height=altura_campos)

# Senha
label_senha = tk.Label(janela_login, text="Senha:", font=fonte_label_campo_str, fg=cor_label_campo, bg=cor_azul_escuro)
label_senha.place(relx=0.5, rely=y_pos_label_senha, anchor="center", width=largura_campos)
entry_senha = tk.Entry(janela_login, font=fonte_entry_str, show="*", width=40)
entry_senha.place(relx=0.5, rely=y_pos_entry_senha, anchor="center", width=largura_campos, height=altura_campos)

# --- Botões ---
LARGURA_BOTAO_PIXELS = 230
ALTURA_BOTAO_PRINCIPAL_PIXELS = 50
ALTURA_BOTAO_SECUNDARIO_PIXELS = 45

RELY_BOTAO_LOGIN = 0.65

botao_acessar = tk.Button(
    janela_login,
    text="Login",
    font=fonte_botao_login_str,
    fg=cor_botao_principal_fg_text,
    bg=cor_botao_principal_bg,
    activebackground="#E0E0E0",
    activeforeground=cor_botao_principal_fg_text,
    command=processar_login,
    relief=tk.FLAT,
    borderwidth=0,
    highlightthickness=0
)
botao_acessar.place(
    relx=0.5,
    rely=RELY_BOTAO_LOGIN,
    anchor="center",
    width=LARGURA_BOTAO_PIXELS,
    height=ALTURA_BOTAO_PRINCIPAL_PIXELS
)

RELY_LINK_CADASTRO = RELY_BOTAO_LOGIN + 0.10

botao_link_cadastro = tk.Button(
    janela_login,
    text="Primeira vez? Cadastre-se",
    font=fonte_botao_secundario_str,
    fg=cor_botao_secundario_fg_text,
    bg=cor_fundo_botao_secundario,
    activebackground=cor_azul_claro,
    activeforeground="white",
    command=ir_para_cadastro_desta_tela,
    relief=tk.FLAT,
    bd=0,
    highlightthickness=0,
    cursor="hand2"
)
botao_link_cadastro.place(
    relx=0.5,
    rely=RELY_LINK_CADASTRO,
    anchor="center",
    width=LARGURA_BOTAO_PIXELS,
    height=ALTURA_BOTAO_SECUNDARIO_PIXELS
)

RELY_BOTAO_VOLTAR_INICIO = RELY_LINK_CADASTRO + 0.10

botao_voltar_inicio = tk.Button(
    janela_login,
    text="Voltar para o Início",
    font=fonte_botao_secundario_str,
    fg=cor_botao_secundario_fg_text,
    bg=cor_fundo_botao_secundario,
    activebackground=cor_azul_claro,
    activeforeground="white",
    command=ir_para_inicio_da_tela_login,
    relief=tk.FLAT,
    bd=0,
    highlightthickness=0,
    cursor="hand2"
)
botao_voltar_inicio.place(
    relx=0.5,
    rely=RELY_BOTAO_VOLTAR_INICIO,
    anchor="center",
    width=LARGURA_BOTAO_PIXELS,
    height=ALTURA_BOTAO_SECUNDARIO_PIXELS
)

janela_login.mainloop()