import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox
import subprocess # Para chamar outro script
import sys        # Para obter o executável do Python
import os         # Para manipulação de caminhos

# --- Constantes para o Placeholder do CPF ---
CPF_PLACEHOLDER_TEXT = "somente números..."
CPF_PLACEHOLDER_COLOR = "grey"
CPF_NORMAL_TEXT_COLOR = "black" # Ou a cor padrão do Entry que você preferir

# --- Funções de Navegação ---
def ir_para_inicio_da_tela_cadastro():
    """Fecha a janela de cadastro e abre a tela de início."""
    try:
        script_dir = os.path.dirname(__file__) # Diretório do script atual
        caminho_inicio_py = os.path.join(script_dir, "inicio.py")

        if os.path.exists(caminho_inicio_py):
            janela_cadastro.destroy() # Fecha a janela de cadastro atual
            subprocess.Popen([sys.executable, caminho_inicio_py])
            print(f"Navegando para '{caminho_inicio_py}'")
        else:
            messagebox.showerror("Erro de Navegação", f"Arquivo 'inicio.py' não encontrado em:\n{caminho_inicio_py}")
            # A janela de cadastro não será destruída se o arquivo não for encontrado,
            # permitindo que o usuário veja o erro.
    except Exception as e:
        messagebox.showerror("Erro de Navegação", f"Não foi possível iniciar 'inicio.py':\n{e}")

# --- Função para o botão Cadastrar ---
def processar_cadastro():
    nome = entry_nome.get()
    email = entry_email.get()
    senha = entry_senha.get()
    cpf_valor = entry_cpf.get()

    # Considera o placeholder como campo vazio para validação
    if cpf_valor == CPF_PLACEHOLDER_TEXT:
        cpf_final = ""
    else:
        cpf_final = cpf_valor

    # Validação simples (pode ser expandida)
    if not nome or not email or not senha or not cpf_final: # cpf_final já tratado
        messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos.")
        return

    # Adicional: Validação para verificar se o CPF (se preenchido) contém apenas números
    if cpf_final and not cpf_final.isdigit():
        messagebox.showwarning("CPF Inválido", "O CPF deve conter apenas números.")
        return

    print("--- Dados do Cadastro ---")
    print(f"Nome Completo: {nome}")
    print(f"Email: {email}")
    print(f"Senha: {senha}") 
    print(f"CPF: {cpf_final}")

    messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso! (Simulação)")

    # Fecha a janela de cadastro
    janela_cadastro.destroy()

    # Tenta executar o login.py
    try:
        script_dir = os.path.dirname(__file__) # Diretório do script atual
        caminho_login_py = os.path.join(script_dir, "login.py")

        if os.path.exists(caminho_login_py):
            subprocess.Popen([sys.executable, caminho_login_py])
            print(f"Retornando para '{caminho_login_py}'")
        else:
            # Se login.py não for encontrado, o usuário já viu o sucesso do cadastro.
            # Poderia logar este erro ou informar o usuário de forma não intrusiva.
            print(f"Erro: O arquivo de login '{caminho_login_py}' não foi encontrado após o cadastro.")
    except Exception as e:
        print(f"Erro ao tentar executar login.py após o cadastro: {e}")


# --- Funções de Evento para o Placeholder do CPF ---
def on_cpf_focus_in(event):
    if entry_cpf.get() == CPF_PLACEHOLDER_TEXT:
        entry_cpf.delete(0, tk.END)
        entry_cpf.config(fg=CPF_NORMAL_TEXT_COLOR)

def on_cpf_focus_out(event):
    if not entry_cpf.get():
        entry_cpf.insert(0, CPF_PLACEHOLDER_TEXT)
        entry_cpf.config(fg=CPF_PLACEHOLDER_COLOR)


# --- Configurações da Janela Principal ---
janela_cadastro = tk.Tk()
janela_cadastro.title("SafeFile - Cadastro")
LARGURA_JANELA = 800
ALTURA_JANELA = 600 # Mantida para consistência, pode ser ajustada se necessário
janela_cadastro.geometry(f"{LARGURA_JANELA}x{ALTURA_JANELA}")
janela_cadastro.resizable(False, False)

# --- Cores ---
cor_azul_claro = "#80DEEA"
cor_azul_escuro = "#3161E6"
cor_texto_titulo = "white"
cor_label_campo = "white"
cor_botao_principal_bg = "#FFFFFF" # Para o botão "Cadastrar"
cor_botao_principal_fg_text = "#5C00A4" # Texto do botão "Cadastrar"
cor_botao_secundario_fg_text = "white" # Para o botão "Voltar para o Início"
cor_fundo_botao_secundario = cor_azul_escuro # Fundo para o botão "Voltar para o Início"

# --- Fontes ---
fonte_titulo_str = ("Arial", 36, "bold")
fonte_label_campo_str = ("Arial", 12)
fonte_entry_str = ("Arial", 12)
fonte_botao_cadastrar_str = ("Arial", 16, "bold")
fonte_botao_voltar_str = ("Arial", 12) # Fonte para o botão "Voltar para o Início"

# --- Canvas para o Gradiente de Fundo ---
canvas_fundo = tk.Canvas(janela_cadastro, highlightthickness=0)
canvas_fundo.pack(fill="both", expand=True)

def desenhar_titulo_no_canvas():
    canvas_fundo.delete("titulo_safefile")
    canvas_fundo.create_text(
        LARGURA_JANELA / 2,
        ALTURA_JANELA * 0.12, # Ajustado para dar mais espaço para os botões abaixo
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

    if largura_canvas == 0 or altura_canvas == 0: return

    r1, g1, b1 = janela_cadastro.winfo_rgb(cor_azul_escuro)[0]//256, janela_cadastro.winfo_rgb(cor_azul_escuro)[1]//256, janela_cadastro.winfo_rgb(cor_azul_escuro)[2]//256
    r2, g2, b2 = janela_cadastro.winfo_rgb(cor_azul_claro)[0]//256, janela_cadastro.winfo_rgb(cor_azul_claro)[1]//256, janela_cadastro.winfo_rgb(cor_azul_claro)[2]//256

    for i in range(largura_canvas):
        r = int(r1 + (r2 - r1) * (i / largura_canvas))
        g = int(g1 + (g2 - g1) * (i / largura_canvas))
        b = int(b1 + (b2 - b1) * (i / largura_canvas))
        cor = f'#{r:02x}{g:02x}{b:02x}'
        canvas_fundo.create_line(i, 0, i, altura_canvas, fill=cor, tags="gradient")
    desenhar_titulo_no_canvas()

janela_cadastro.update_idletasks()
desenhar_gradiente()
canvas_fundo.bind("<Configure>", desenhar_gradiente)

# --- Campos de Cadastro ---
y_pos_inicial_label = 0.25 # Posição Y inicial para o primeiro label
y_pos_inicial_entry = 0.30 # Posição Y inicial para a primeira entry
incremento_y_grupo = 0.11  # Espaçamento vertical entre os grupos (label + entry)
largura_campos = LARGURA_JANELA * 0.5
altura_campos = 35

# Nome Completo
label_nome = tk.Label(janela_cadastro, text="Nome Completo:", font=fonte_label_campo_str, fg=cor_label_campo, bg=cor_azul_escuro)
label_nome.place(relx=0.5, rely=y_pos_inicial_label, anchor="center", width=largura_campos)
entry_nome = tk.Entry(janela_cadastro, font=fonte_entry_str, width=40)
entry_nome.place(relx=0.5, rely=y_pos_inicial_entry, anchor="center", width=largura_campos, height=altura_campos)

y_pos_inicial_label += incremento_y_grupo
y_pos_inicial_entry += incremento_y_grupo

# Email
label_email = tk.Label(janela_cadastro, text="Email:", font=fonte_label_campo_str, fg=cor_label_campo, bg=cor_azul_escuro)
label_email.place(relx=0.5, rely=y_pos_inicial_label, anchor="center", width=largura_campos)
entry_email = tk.Entry(janela_cadastro, font=fonte_entry_str, width=40)
entry_email.place(relx=0.5, rely=y_pos_inicial_entry, anchor="center", width=largura_campos, height=altura_campos)

y_pos_inicial_label += incremento_y_grupo
y_pos_inicial_entry += incremento_y_grupo

# Senha
label_senha = tk.Label(janela_cadastro, text="Senha:", font=fonte_label_campo_str, fg=cor_label_campo, bg=cor_azul_escuro)
label_senha.place(relx=0.5, rely=y_pos_inicial_label, anchor="center", width=largura_campos)
entry_senha = tk.Entry(janela_cadastro, font=fonte_entry_str, show="*", width=40)
entry_senha.place(relx=0.5, rely=y_pos_inicial_entry, anchor="center", width=largura_campos, height=altura_campos)

y_pos_inicial_label += incremento_y_grupo
y_pos_inicial_entry += incremento_y_grupo

# CPF
label_cpf = tk.Label(janela_cadastro, text="CPF:", font=fonte_label_campo_str, fg=cor_label_campo, bg=cor_azul_escuro)
label_cpf.place(relx=0.5, rely=y_pos_inicial_label, anchor="center", width=largura_campos)
entry_cpf = tk.Entry(janela_cadastro, font=fonte_entry_str, fg=CPF_PLACEHOLDER_COLOR, width=40)
entry_cpf.insert(0, CPF_PLACEHOLDER_TEXT) # Insere o placeholder inicialmente
entry_cpf.bind("<FocusIn>", on_cpf_focus_in)
entry_cpf.bind("<FocusOut>", on_cpf_focus_out)
entry_cpf.place(relx=0.5, rely=y_pos_inicial_entry, anchor="center", width=largura_campos, height=altura_campos)

# --- Botões ---
LARGURA_BOTAO_PIXELS = 230 # Largura comum para os botões
ALTURA_BOTAO_PRINCIPAL_PIXELS = 50
ALTURA_BOTAO_SECUNDARIO_PIXELS = 45

# Posição Y para o botão "Cadastrar"
RELY_BOTAO_CADASTRAR = y_pos_inicial_entry + incremento_y_grupo * 0.7 # Ajustado para dar espaço para o botão abaixo

botao_cadastrar = tk.Button(
    janela_cadastro,
    text="Cadastrar",
    font=fonte_botao_cadastrar_str,
    fg=cor_botao_principal_fg_text,
    bg=cor_botao_principal_bg,
    activebackground="#E0E0E0",
    activeforeground=cor_botao_principal_fg_text,
    command=processar_cadastro,
    relief=tk.FLAT,
    borderwidth=0,
    highlightthickness=0
)
botao_cadastrar.place(
    relx=0.5,
    rely=RELY_BOTAO_CADASTRAR,
    anchor="center",
    width=LARGURA_BOTAO_PIXELS,
    height=ALTURA_BOTAO_PRINCIPAL_PIXELS # Altura do botão principal
)

# Posição Y para o botão "Voltar para o Início"
# O valor 0.09 representa aproximadamente 9% da altura da janela como espaçamento.
RELY_BOTAO_VOLTAR_INICIO = RELY_BOTAO_CADASTRAR + 0.09

botao_voltar_inicio = tk.Button(
    janela_cadastro,
    text="Voltar para o Início",
    font=fonte_botao_voltar_str, # Fonte específica para este botão
    fg=cor_botao_secundario_fg_text,
    bg=cor_fundo_botao_secundario,
    activebackground=cor_azul_claro, # Efeito ao clicar
    activeforeground="white",
    command=ir_para_inicio_da_tela_cadastro, # Chama a nova função
    relief=tk.FLAT,
    bd=0,
    highlightthickness=0
)
botao_voltar_inicio.place(
    relx=0.5,
    rely=RELY_BOTAO_VOLTAR_INICIO,
    anchor="center",
    width=LARGURA_BOTAO_PIXELS, # Mesma largura dos outros botões
    height=ALTURA_BOTAO_SECUNDARIO_PIXELS # Altura dos botões secundários
)
janela_cadastro.mainloop()
