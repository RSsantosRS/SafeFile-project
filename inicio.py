import tkinter as tk
from tkinter import font as tkFont
import subprocess
import sys
import os

# --- navegação ---
def ir_para_inicio():
    try:
        script_dir = os.path.dirname(__file__)
        caminho_inicio_py = os.path.join(script_dir, "inicio.py")

        if os.path.exists(caminho_inicio_py):
            janela.destroy()
            subprocess.Popen([sys.executable, caminho_inicio_py])
            print(f"retornando para '{caminho_inicio_py}'")
        else:
            print(f"erro: O arquivo de inicio '{caminho_inicio_py}' não foi encontrado.")
    except Exception as e:
        print(f"Erro ao tentar executar inicio.py: {e}")

def ir_para_login():
    try:
        script_dir = os.path.dirname(__file__)
        caminho_login_py = os.path.join(script_dir, "login.py")

        if os.path.exists(caminho_login_py):
            janela.destroy()
            subprocess.Popen([sys.executable, caminho_login_py])
            print(f"Indo para '{caminho_login_py}'")
        else:
            print(f"Erro: O arquivo de login '{caminho_login_py}' não foi encontrado.")
    except Exception as e:
        print(f"Erro ao tentar executar login.py: {e}")

def ir_para_cadastro():
    print("Botão Cadastre-se clicado: Tentando abrir cadastro.py...")
    try:   
        script_dir = os.path.dirname(__file__)
        caminho_cadastro_py = os.path.join(script_dir, "cadastro.py")

        if os.path.exists(caminho_cadastro_py):
            janela.destroy()
            subprocess.Popen([sys.executable, caminho_cadastro_py])
            print(f"Executando '{caminho_cadastro_py}'")
        else:
            print(f"Erro: O arquivo '{caminho_cadastro_py}' não foi encontrado.")
    except Exception as e:
        print(f"Erro ao tentar executar cadastro.py: {e}")


# --- Configurações da Janela Principal ---
janela = tk.Tk()
janela.title("SafeFile - Menu Principal")
LARGURA_JANELA = 800
ALTURA_JANELA = 600
janela.geometry(f"{LARGURA_JANELA}x{ALTURA_JANELA}")
janela.resizable(False, False)

# --- Cores ---
cor_azul_claro = "#80DEEA"
cor_azul_escuro = "#3161E6"
cor_texto_titulo = "white"
cor_botao_login_bg = "#FFFFFF" 
cor_botao_login_fg_text = "#5C00A4" 
cor_botao_secundario_fg_text = "white" 
cor_fundo_botao_secundario = cor_azul_escuro

# --- Fontes (usando tuplas para compatibilidade com create_text e Button) ---
fonte_titulo_str = ("Arial", 36, "bold")
fonte_botao_principal_str = ("Arial", 18, "bold")
fonte_botao_secundario_str = ("Arial", 12)

# --- Canvas para o Gradiente de Fundo ---
canvas_fundo = tk.Canvas(janela, highlightthickness=0)
canvas_fundo.pack(fill="both", expand=True)

def desenhar_titulo_no_canvas():
    canvas_fundo.delete("titulo_safefile")
    canvas_fundo.create_text(
        LARGURA_JANELA / 2,
        ALTURA_JANELA * 0.22,
        text="SafeFile",
        font=fonte_titulo_str,
        fill=cor_texto_titulo,
        tags="titulo_safefile",
        anchor="center"
    )

def desenhar_gradiente(event=None):
    canvas_fundo.delete("gradient")
    largura_canvas = canvas_fundo.winfo_width()
    altura_canvas = canvas_fundo.winfo_height()

    if largura_canvas == 0 or altura_canvas == 0:
        return

    # Cores do gradiente (da esquerda para a direita)
    r1, g1, b1 = janela.winfo_rgb(cor_azul_escuro)[0]//256, janela.winfo_rgb(cor_azul_escuro)[1]//256, janela.winfo_rgb(cor_azul_escuro)[2]//256
    r2, g2, b2 = janela.winfo_rgb(cor_azul_claro)[0]//256, janela.winfo_rgb(cor_azul_claro)[1]//256, janela.winfo_rgb(cor_azul_claro)[2]//256

    # Desenha o gradiente com linhas verticais finas
    for i in range(largura_canvas):
        r = int(r1 + (r2 - r1) * (i / largura_canvas))
        g = int(g1 + (g2 - g1) * (i / largura_canvas))
        b = int(b1 + (b2 - b1) * (i / largura_canvas))
        cor = f'#{r:02x}{g:02x}{b:02x}'
        canvas_fundo.create_line(i, 0, i, altura_canvas, fill=cor, tags="gradient")

    desenhar_titulo_no_canvas()

janela.update_idletasks()
desenhar_gradiente()

canvas_fundo.bind("<Configure>", desenhar_gradiente)


# --- Botões ---
LARGURA_BOTAO_PIXELS = 230
ALTURA_BOTAO_PRINCIPAL_PIXELS = 50 
ALTURA_BOTAO_SECUNDARIO_PIXELS = 45 

# Botão Login
botao_login = tk.Button(
    janela,
    text="Login",
    font=fonte_botao_principal_str, 
    fg=cor_botao_login_fg_text,
    bg=cor_botao_login_bg,
    activebackground="#E0E0E0",
    activeforeground=cor_botao_login_fg_text,
    command=ir_para_login,
    relief=tk.FLAT,
    borderwidth=0,
    highlightthickness=0
)

# Botão para ir para o cadastro
botao_cadastro = tk.Button(
    janela,
    text="Primeira vez? Cadastre-se",
    font=fonte_botao_secundario_str, 
    fg=cor_botao_secundario_fg_text,
    bg=cor_fundo_botao_secundario,
    activebackground=cor_azul_claro,
    activeforeground="white",
    command=ir_para_cadastro,
    relief=tk.FLAT,
    bd=0,
    highlightthickness=0
)

# Botão para voltar ao início
botao_inicio = tk.Button(
    janela,
    text="Voltar para o Início", 
    font=fonte_botao_secundario_str, 
    fg=cor_botao_secundario_fg_text,
    bg=cor_fundo_botao_secundario,
    activebackground=cor_azul_claro,
    activeforeground="white",
    command=ir_para_inicio,
    relief=tk.FLAT,
    bd=0,
    highlightthickness=0
)


RELY_LOGIN = 0.50 
RELY_CADASTRO = 0.62 
RELY_INICIO = 0.74

# Posicionando os botões
botao_login.place(
    relx=0.5,
    rely=RELY_LOGIN,
    anchor="center",
    width=LARGURA_BOTAO_PIXELS,
    height=ALTURA_BOTAO_PRINCIPAL_PIXELS
)

botao_cadastro.place(
    relx=0.5,
    rely=RELY_CADASTRO,
    anchor="center",
    width=LARGURA_BOTAO_PIXELS,
    height=ALTURA_BOTAO_SECUNDARIO_PIXELS
)

botao_inicio.place(
    relx=0.5,
    rely=RELY_INICIO,
    anchor="center",
    width=LARGURA_BOTAO_PIXELS,
    height=ALTURA_BOTAO_SECUNDARIO_PIXELS
)

janela.mainloop()
