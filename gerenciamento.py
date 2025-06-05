import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter import font as tkFont
import os
from banco_documento import BancoDocumento
from documento import Documento
from datetime import datetime
import subprocess
import sys

# --- Configurações da Janela Principal ---
janela = tk.Tk()
janela.title("SafeFile - Gerenciador de Documentos")
LARGURA_JANELA = 800
ALTURA_JANELA = 600
janela.geometry(f"{LARGURA_JANELA}x{ALTURA_JANELA}")
janela.resizable(False, False)

# --- Cores ---
cor_azul_claro = "#80DEEA"
cor_azul_escuro = "#3161E6"
cor_texto_titulo = "white"
cor_botao_acao_bg = "#FFFFFF"
cor_botao_acao_fg_text = "#3161E6"
cor_botao_navegacao_bg = cor_azul_escuro
cor_botao_navegacao_fg_text = "white"
cor_botao_voltar_inicio_bg = "#D32F2F"
cor_botao_voltar_inicio_fg = "white"

# --- Fontes ---
fonte_titulo_str = ("Arial", 36, "bold")
fonte_geral_str = ("Arial", 10)
fonte_botao_acao_str = ("Arial", 10, "bold")
fonte_botao_relatorio_str = ("Arial", 14, "bold")
fonte_botao_voltar_inicio_str = ("Arial", 10, "bold")

# --- Canvas para o Gradiente de Fundo ---
canvas_fundo = tk.Canvas(janela, highlightthickness=0)
canvas_fundo.pack(fill="both", expand=True)

def desenhar_titulo_no_canvas():
    canvas_fundo.delete("titulo_safefile")
    canvas_fundo.create_text(
        LARGURA_JANELA / 2,
        ALTURA_JANELA * 0.10,
        text="SafeFile - Documentos",
        font=fonte_titulo_str,
        fill=cor_texto_titulo,
        tags="titulo_safefile",
        anchor="center"
    )

def desenhar_gradiente(event=None):
    canvas_fundo.delete("gradient")
    largura_canvas_grad = LARGURA_JANELA
    altura_canvas_grad = ALTURA_JANELA

    if largura_canvas_grad <= 1 or altura_canvas_grad <= 1:
        largura_canvas_grad = janela.winfo_width()
        altura_canvas_grad = janela.winfo_height()
        if largura_canvas_grad <= 1 or altura_canvas_grad <= 1:
            return

    r1, g1, b1 = janela.winfo_rgb(cor_azul_escuro)[0]//256, janela.winfo_rgb(cor_azul_escuro)[1]//256, janela.winfo_rgb(cor_azul_escuro)[2]//256
    r2, g2, b2 = janela.winfo_rgb(cor_azul_claro)[0]//256, janela.winfo_rgb(cor_azul_claro)[1]//256, janela.winfo_rgb(cor_azul_claro)[2]//256

    for i in range(int(largura_canvas_grad)):
        if largura_canvas_grad == 0: break
        r = int(r1 + (r2 - r1) * (i / largura_canvas_grad))
        g = int(g1 + (g2 - g1) * (i / largura_canvas_grad))
        b = int(b1 + (b2 - b1) * (i / largura_canvas_grad))
        cor = f'#{r:02x}{g:02x}{b:02x}'
        canvas_fundo.create_line(i, 0, i, altura_canvas_grad, fill=cor, tags="gradient")

    desenhar_titulo_no_canvas()
    if 'botao_voltar_inicio_widget' in globals() and botao_voltar_inicio_widget.winfo_exists():
        botao_voltar_inicio_widget.lift()

# --- Função para Retornar ao Gerenciador de Arquivos ---
def retornar_ao_gerenciador():
    print("Gerenciador de Documentos: Retornando para o Gerenciador de Arquivos...")
    try:
        script_dir = os.path.dirname(__file__)
        caminho_gerenciador_py = os.path.join(script_dir, "gerenciador.py")

        if os.path.exists(caminho_gerenciador_py):
            janela.destroy()
            subprocess.Popen([sys.executable, caminho_gerenciador_py])
            print(f"Gerenciador de Documentos: Executando '{caminho_gerenciador_py}'")
        else:
            messagebox.showerror("Erro de Navegação", f"Arquivo 'gerenciador.py' não encontrado em:\n{caminho_gerenciador_py}", parent=janela)
    except Exception as e:
        messagebox.showerror("Erro de Navegação", f"Não foi possível iniciar 'gerenciador.py':\n{e}", parent=janela)

# --- Função para Acessar Relatório ---
def acessar_relatorio():
    print("Acessando Relatório de Documentos...")
    try:
        script_dir = os.path.dirname(__file__)
        caminho_relatorio_py = os.path.join(script_dir, "relatorio.py")

        if os.path.exists(caminho_relatorio_py):
            janela.destroy()
            subprocess.Popen([sys.executable, caminho_relatorio_py])
            print(f"Gerenciador de Documentos: Executando '{caminho_relatorio_py}'")
        else:
            messagebox.showerror("Erro de Navegação", f"Arquivo 'relatorio.py' não encontrado em:\n{caminho_relatorio_py}", parent=janela)
    except Exception as e:
        messagebox.showerror("Erro de Navegação", f"Não foi possível iniciar 'relatorio.py':\n{e}", parent=janela)

# --- Botão Retornar ---
botao_voltar_inicio_widget = tk.Button(
    janela,
    text="Retornar",
    font=fonte_botao_voltar_inicio_str,
    fg=cor_botao_voltar_inicio_fg,
    bg=cor_botao_voltar_inicio_bg,
    activebackground=cor_azul_claro,
    activeforeground="white",
    command=retornar_ao_gerenciador,
    relief=tk.FLAT,
    borderwidth=0,
    highlightthickness=0,
    cursor="hand2"
)
botao_voltar_inicio_widget.place(relx=0.98, rely=0.02, anchor="ne", x=-10, y=10)

# --- Inicialização do Banco de Dados ---
banco = BancoDocumento()
banco.conectar()

# --- Variáveis para o Formulário ---
var_nome_arquivo = tk.StringVar()
var_caminho = tk.StringVar()
var_tipo_arquivo = tk.StringVar()
var_tamanho_mb = tk.StringVar()
var_documento_selecionado = tk.StringVar(value="Novo documento")

# --- Função para Atualizar o Formulário ---
def atualizar_formulario(*args):
    documento_selecionado = var_documento_selecionado.get()
    if documento_selecionado == "Novo documento":
        var_nome_arquivo.set("")
        var_caminho.set("")
        var_tipo_arquivo.set("")
        var_tamanho_mb.set("")
    else:
        documento = banco.buscar_documento_por_nome(documento_selecionado)
        if documento:
            var_nome_arquivo.set(documento.nome_arquivo)
            var_caminho.set(documento.caminho)
            var_tipo_arquivo.set(documento.tipo_arquivo)
            var_tamanho_mb.set(str(documento.tamanho_mb))

# --- Função para Atualizar o Combobox ---
def atualizar_combobox():
    documentos = banco.buscar_todos_documentos()
    valores = ["Novo documento"] + [doc.nome_arquivo for doc in documentos]
    combo_documentos['values'] = valores
    combo_documentos.set("Novo documento")

# --- Função para Enviar o Formulário ---
def enviar_formulario():
    nome_arquivo = var_nome_arquivo.get()
    caminho = var_caminho.get()
    tipo_arquivo = var_tipo_arquivo.get()
    tamanho_mb = var_tamanho_mb.get()

    if not all([nome_arquivo, caminho, tipo_arquivo, tamanho_mb]):
        messagebox.showerror("Erro", "Todos os campos são obrigatórios!", parent=janela)
        return

    try:
        tamanho_mb = float(tamanho_mb)
    except ValueError:
        messagebox.showerror("Erro", "O tamanho deve ser um número válido!", parent=janela)
        return

    documento = Documento(
        nome_arquivo=nome_arquivo,
        caminho=caminho,
        tipo_arquivo=tipo_arquivo,
        data_criacao=datetime.now(),
        tamanho_mb=tamanho_mb
    )

    documento_selecionado = var_documento_selecionado.get()
    try:
        if documento_selecionado == "Novo documento":
            banco.inserir_documento(documento)
            messagebox.showinfo("Sucesso", "Documento adicionado com sucesso!", parent=janela)
        else:
            banco.atualizar_documento_por_nome(documento_selecionado, documento)
            messagebox.showinfo("Sucesso", "Documento atualizado com sucesso!", parent=janela)
        atualizar_combobox()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar documento: {str(e)}", parent=janela)

# --- Função para Excluir Documento ---
def excluir_documento():
    documento_selecionado = var_documento_selecionado.get()
    if documento_selecionado == "Novo documento":
        messagebox.showerror("Erro", "Selecione um documento para excluir!", parent=janela)
        return

    if messagebox.askyesno("Confirmar", f"Deseja realmente excluir o documento {documento_selecionado}?", parent=janela):
        try:
            banco.apagar_documento(documento_selecionado)
            messagebox.showinfo("Sucesso", "Documento excluído com sucesso!", parent=janela)
            atualizar_combobox()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir documento: {str(e)}", parent=janela)

# --- Frame Central para o Formulário ---
frame_central = tk.Frame(janela, bg=cor_azul_claro, bd=2, relief=tk.GROOVE)
frame_central.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)

# --- Combobox para Seleção de Documento ---
combo_documentos = ttk.Combobox(frame_central, textvariable=var_documento_selecionado, state="readonly", font=fonte_geral_str)
combo_documentos.pack(pady=10)
combo_documentos.bind("<<ComboboxSelected>>", atualizar_formulario)

# --- Campos do Formulário ---
campos = [
    ("Nome do Arquivo:", var_nome_arquivo),
    ("Caminho:", var_caminho),
    ("Tipo do Arquivo:", var_tipo_arquivo),
    ("Tamanho (MB):", var_tamanho_mb)
]

for i, (label_text, var) in enumerate(campos):
    frame_campo = tk.Frame(frame_central, bg=cor_azul_claro)
    frame_campo.pack(pady=5)
    
    label = tk.Label(frame_campo, text=label_text, font=fonte_geral_str, bg=cor_azul_claro)
    label.pack(anchor="w")
    
    entry = tk.Entry(frame_campo, textvariable=var, font=fonte_geral_str, width=50)
    entry.pack(anchor="w")

# --- Botão Enviar ---
botao_enviar = tk.Button(
    frame_central,
    text="Enviar",
    font=fonte_botao_acao_str,
    fg=cor_botao_acao_fg_text,
    bg=cor_botao_acao_bg,
    command=enviar_formulario,
    relief=tk.FLAT,
    activebackground="#E0E0E0",
    activeforeground=cor_botao_acao_fg_text,
    width=15,
    height=2
)
botao_enviar.pack(pady=10)

# --- Frame para Botões de Ação ---
frame_botoes_acao = tk.Frame(janela, bd=2, relief=tk.GROOVE)
frame_botoes_acao.place(relx=0.05, rely=0.90, relwidth=0.9, height=50)

botoes_info = [
    ("Excluir", excluir_documento),
    ("Acessar Relatório", acessar_relatorio)
]

for i, (texto, comando) in enumerate(botoes_info):
    btn = tk.Button(frame_botoes_acao, text=texto, command=comando,
                    font=fonte_botao_acao_str, fg=cor_botao_acao_fg_text, bg=cor_botao_acao_bg,
                    relief=tk.FLAT, activebackground="#E0E0E0", activeforeground=cor_botao_acao_fg_text,
                    width=15, height=2)
    btn.pack(side=tk.LEFT, expand=True, padx=5, pady=10)

# --- Inicialização ---
janela.update_idletasks()
desenhar_gradiente()
canvas_fundo.bind("<Configure>", desenhar_gradiente)
atualizar_combobox()

janela.mainloop()