import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont
import os
from banco_documento import BancoDocumento
import subprocess
import sys

# --- Configurações da Janela Principal ---
janela = tk.Tk()
janela.title("SafeFile - Relatório de Documentos")
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
fonte_treeview_str = ("Arial", 10)

# --- Canvas para o Gradiente de Fundo ---
canvas_fundo = tk.Canvas(janela, highlightthickness=0)
canvas_fundo.pack(fill="both", expand=True)

def desenhar_titulo_no_canvas():
    canvas_fundo.delete("titulo_safefile")
    canvas_fundo.create_text(
        LARGURA_JANELA / 2,
        ALTURA_JANELA * 0.10,
        text="SafeFile - Relatório",
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
    if 'botao_voltar_widget' in globals() and botao_voltar_widget.winfo_exists():
        botao_voltar_widget.lift()

# --- Função para Voltar ao Gerenciador ---
def voltar_ao_gerenciador():
    print("Relatório: Voltando para o Gerenciador...")
    try:
        script_dir = os.path.dirname(__file__)
        caminho_gerenciador_py = os.path.join(script_dir, "gerenciamento.py")

        if os.path.exists(caminho_gerenciador_py):
            janela.destroy()
            subprocess.Popen([sys.executable, caminho_gerenciador_py])
            print(f"Relatório: Executando '{caminho_gerenciador_py}'")
        else:
            messagebox.showerror("Erro de Navegação", f"Arquivo 'gerenciamento.py' não encontrado em:\n{caminho_gerenciador_py}", parent=janela)
    except Exception as e:
        messagebox.showerror("Erro de Navegação", f"Não foi possível iniciar 'gerenciamento.py':\n{e}", parent=janela)

# --- Botão Voltar ---
botao_voltar_widget = tk.Button(
    janela,
    text="Voltar ao Gerenciador",
    font=fonte_botao_acao_str,
    fg=cor_botao_voltar_inicio_fg,
    bg=cor_botao_voltar_inicio_bg,
    activebackground=cor_azul_claro,
    activeforeground="white",
    command=voltar_ao_gerenciador,
    relief=tk.FLAT,
    borderwidth=0,
    highlightthickness=0,
    cursor="hand2"
)
botao_voltar_widget.place(relx=0.98, rely=0.02, anchor="ne", x=-10, y=10)

# --- Inicialização do Banco de Dados ---
banco = BancoDocumento()
banco.conectar()

# --- Configuração da Treeview ---
style = ttk.Style()
style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=fonte_treeview_str, rowheight=25)
style.configure("mystyle.Treeview.Heading", font=(fonte_treeview_str[0], int(fonte_treeview_str[1]), "bold"))
style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

tree_frame = tk.Frame(janela)
tree_frame.place(relx=0.05, rely=0.26, relwidth=0.9, relheight=0.65)

tree = ttk.Treeview(tree_frame, columns=("nome", "caminho", "tipo", "data", "tamanho"), style="mystyle.Treeview")
tree.heading("#0", text="")
tree.heading("nome", text="Nome")
tree.heading("caminho", text="Caminho")
tree.heading("tipo", text="Tipo")
tree.heading("data", text="Data de Criação")
tree.heading("tamanho", text="Tamanho (MB)")

tree.column("#0", width=0, stretch=tk.NO)
tree.column("nome", width=150)
tree.column("caminho", width=200)
tree.column("tipo", width=100)
tree.column("data", width=150)
tree.column("tamanho", width=100)

tree.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=scrollbar.set)

def atualizar_lista_documentos():
    for item in tree.get_children():
        tree.delete(item)
    
    documentos = banco.buscar_todos_documentos()
    for doc in documentos:
        tree.insert("", "end", values=(
            doc.nome_arquivo,
            doc.caminho,
            doc.tipo_arquivo,
            doc.data_criacao.strftime('%Y-%m-%d %H:%M:%S'),
            f"{doc.tamanho_mb:.2f}"
        ))

# --- Inicialização ---
janela.update_idletasks()
desenhar_gradiente()
canvas_fundo.bind("<Configure>", desenhar_gradiente)
atualizar_lista_documentos()

janela.mainloop() 