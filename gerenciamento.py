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
fonte_botao_voltar_inicio_str = ("Arial", 10, "bold") # Garante que esta fonte existe

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
        caminho_gerenciador_py = os.path.join(script_dir, "gerenciador.py") # Caminho para gerenciador.py

        if os.path.exists(caminho_gerenciador_py):
            janela.destroy() # Destrói a janela atual
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

# --- Botão Retornar (substituindo "Voltar ao Início") ---
botao_voltar_inicio_widget = tk.Button( # Mantido o nome da variável para não quebrar a referência no desenhar_gradiente
    janela,
    text="Retornar", # Texto alterado
    font=fonte_botao_voltar_inicio_str,
    fg=cor_botao_voltar_inicio_fg,
    bg=cor_botao_voltar_inicio_bg,
    activebackground=cor_azul_claro,
    activeforeground="white",
    command=retornar_ao_gerenciador, # Comando alterado
    relief=tk.FLAT,
    borderwidth=0,
    highlightthickness=0,
    cursor="hand2"
)
botao_voltar_inicio_widget.place(relx=0.98, rely=0.02, anchor="ne", x=-10, y=10)

# --- Botão Acessar Relatório ---
botao_relatorio = tk.Button(
    janela,
    text="Acessar Relatório",
    font=fonte_botao_relatorio_str,
    fg=cor_botao_acao_fg_text,
    bg=cor_botao_acao_bg,
    activebackground="#E0E0E0",
    activeforeground=cor_botao_acao_fg_text,
    command=acessar_relatorio,
    relief=tk.FLAT,
    borderwidth=0,
    highlightthickness=0,
    cursor="hand2",
    width=20,
    height=3
)
botao_relatorio.place(relx=0.5, rely=0.5, anchor="center")

# --- Inicialização do Banco de Dados ---
banco = BancoDocumento()
banco.conectar()

# --- Funções de Gerenciamento de Documentos ---
def adicionar_documento():
    nome_arquivo = simpledialog.askstring("Adicionar", "Nome do arquivo:", parent=janela)
    if not nome_arquivo:
        return
        
    caminho = simpledialog.askstring("Adicionar", "Caminho do arquivo:", parent=janela)
    if not caminho:
        return
        
    tipo_arquivo = simpledialog.askstring("Adicionar", "Tipo do arquivo:", parent=janela)
    if not tipo_arquivo:
        return
        
    tamanho_mb = simpledialog.askfloat("Adicionar", "Tamanho em MB:", parent=janela)
    if tamanho_mb is None:
        return
        
    documento = Documento(
        nome_arquivo=nome_arquivo,
        caminho=caminho,
        tipo_arquivo=tipo_arquivo,
        data_criacao=datetime.now(),
        tamanho_mb=tamanho_mb
    )
    
    try:
        banco.inserir_documento(documento)
        messagebox.showinfo("Sucesso", "Documento adicionado com sucesso!", parent=janela)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao adicionar documento: {str(e)}", parent=janela)

def atualizar_documento():
    nome_arquivo = simpledialog.askstring("Atualizar", "Nome do arquivo a ser atualizado:", parent=janela)
    if not nome_arquivo:
        return
        
    documento = banco.buscar_documento_por_nome(nome_arquivo)
    if not documento:
        messagebox.showerror("Erro", "Documento não encontrado!", parent=janela)
        return
        
    novo_nome = simpledialog.askstring("Atualizar", "Novo nome do arquivo:", initialvalue=documento.nome_arquivo, parent=janela)
    if not novo_nome:
        return
        
    caminho = simpledialog.askstring("Atualizar", "Novo caminho:", initialvalue=documento.caminho, parent=janela)
    if not caminho:
        return
        
    tipo_arquivo = simpledialog.askstring("Atualizar", "Novo tipo:", initialvalue=documento.tipo_arquivo, parent=janela)
    if not tipo_arquivo:
        return
        
    tamanho_mb = simpledialog.askfloat("Atualizar", "Novo tamanho em MB:", initialvalue=documento.tamanho_mb, parent=janela)
    if tamanho_mb is None:
        return
    
    try:
        # Se o nome foi alterado, precisamos fazer uma atualização especial
        if novo_nome != documento.nome_arquivo:
            documento.nome_arquivo = novo_nome
            documento.caminho = caminho
            documento.tipo_arquivo = tipo_arquivo
            documento.tamanho_mb = tamanho_mb
            banco.atualizar_documento_por_nome(nome_arquivo, documento)
        else:
            documento.caminho = caminho
            documento.tipo_arquivo = tipo_arquivo
            documento.tamanho_mb = tamanho_mb
            banco.atualizar_documento(documento)
            
        messagebox.showinfo("Sucesso", "Documento atualizado com sucesso!", parent=janela)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar documento: {str(e)}", parent=janela)

def excluir_documento():
    nome_arquivo = simpledialog.askstring("Excluir", "Nome do arquivo a ser excluído:", parent=janela)
    if not nome_arquivo:
        return
        
    if messagebox.askyesno("Confirmar", f"Deseja realmente excluir o documento {nome_arquivo}?", parent=janela):
        try:
            banco.apagar_documento(nome_arquivo)
            messagebox.showinfo("Sucesso", "Documento excluído com sucesso!", parent=janela)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir documento: {str(e)}", parent=janela)

def buscar_documento():
    nome_arquivo = simpledialog.askstring("Buscar", "Nome do arquivo a ser buscado:", parent=janela)
    if not nome_arquivo:
        return
        
    documento = banco.buscar_documento_por_nome(nome_arquivo)
    if documento:
        mensagem = f"""
        Nome: {documento.nome_arquivo}
        Caminho: {documento.caminho}
        Tipo: {documento.tipo_arquivo}
        Data de Criação: {documento.data_criacao}
        Tamanho: {documento.tamanho_mb} MB
        """
        messagebox.showinfo("Documento Encontrado", mensagem, parent=janela)
    else:
        messagebox.showinfo("Busca", "Documento não encontrado!", parent=janela)

# --- Frame para Botões de Ação ---
frame_botoes_acao = tk.Frame(janela, bg=cor_azul_escuro)
frame_botoes_acao.place(relx=0.05, rely=0.83, relwidth=0.9, height=80)

botoes_info = [
    ("Adicionar", adicionar_documento),
    ("Atualizar", atualizar_documento),
    ("Excluir", excluir_documento),
    ("Buscar", buscar_documento)
]

for i, (texto, comando) in enumerate(botoes_info):
    btn = tk.Button(frame_botoes_acao, text=texto, command=comando,
                    font=fonte_botao_acao_str, fg=cor_botao_acao_fg_text, bg=cor_botao_acao_bg,
                    relief=tk.FLAT, activebackground="#E0E0E0", activeforeground=cor_botao_acao_fg_text,
                    width=12, height=2)
    btn.pack(side=tk.LEFT, expand=True, padx=5, pady=10)

# --- Inicialização ---
janela.update_idletasks()
desenhar_gradiente()
canvas_fundo.bind("<Configure>", desenhar_gradiente)

janela.mainloop()