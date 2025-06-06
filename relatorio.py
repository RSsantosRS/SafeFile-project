import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont
import os
from banco_documento import BancoDocumento
import subprocess
import sys


class TelaRelatorio:
    def __init__(self, janela_principal):
        """Inicializa a tela de relatório."""
        self.janela = janela_principal
        self.janela.title("SafeFile - Relatório de Documentos")
        self.LARGURA_JANELA = 800
        self.ALTURA_JANELA = 600
        self.janela.geometry(f"{self.LARGURA_JANELA}x{self.ALTURA_JANELA}")
        self.janela.resizable(False, False)

        # Inicializa a classe do banco
        self.banco = BancoDocumento()
        self.banco.conectar()

        self.configurar_estilos()
        self.criar_widgets()
        self.carregar_dados_iniciais()

    def configurar_estilos(self):
        """Define as cores e fontes usadas na interface."""
        self.cor_azul_claro = "#80DEEA"
        self.cor_azul_escuro = "#3161E6"
        self.cor_texto_titulo = "white"
        self.cor_botao_acao_bg = "#FFFFFF"
        self.cor_botao_acao_fg_text = "#3161E6"
        self.cor_botao_navegacao_bg = self.cor_azul_escuro
        self.cor_botao_navegacao_fg_text = "white"
        self.cor_botao_voltar_inicio_bg = "#D32F2F"
        self.cor_botao_voltar_inicio_fg = "white"

        # Fontes
        self.fonte_titulo_str = ("Arial", 36, "bold")
        self.fonte_geral_str = ("Arial", 10)
        self.fonte_botao_acao_str = ("Arial", 10, "bold")
        self.fonte_treeview_str = ("Arial", 10)

        # Estilo do Treeview
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=self.fonte_treeview_str, rowheight=25)
        style.configure("mystyle.Treeview.Heading", font=(self.fonte_treeview_str[0], int(self.fonte_treeview_str[1]), "bold"))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

    def criar_widgets(self):
        """Cria e posiciona todos os widgets na janela."""
        self.criar_fundo_gradiente()
        self.criar_botao_voltar()
        self.criar_tabela_relatorio()

    def criar_fundo_gradiente(self):
        """Cria um canvas com um fundo gradiente e o título."""
        self.canvas_fundo = tk.Canvas(self.janela, highlightthickness=0)
        self.canvas_fundo.pack(fill="both", expand=True)
        self.canvas_fundo.bind("<Configure>", self.desenhar_gradiente)
        self.janela.update_idletasks()
        self.desenhar_gradiente()

    def desenhar_gradiente(self, event=None):
        """Desenha o gradiente de cores e o título no canvas."""
        self.canvas_fundo.delete("gradient", "titulo_safefile")
        
        largura_canvas_grad = self.LARGURA_JANELA
        altura_canvas_grad = self.ALTURA_JANELA

        r1, g1, b1 = self.janela.winfo_rgb(self.cor_azul_escuro)[0]//256, self.janela.winfo_rgb(self.cor_azul_escuro)[1]//256, self.janela.winfo_rgb(self.cor_azul_escuro)[2]//256
        r2, g2, b2 = self.janela.winfo_rgb(self.cor_azul_claro)[0]//256, self.janela.winfo_rgb(self.cor_azul_claro)[1]//256, self.janela.winfo_rgb(self.cor_azul_claro)[2]//256

        for i in range(int(largura_canvas_grad)):
            if largura_canvas_grad == 0: break
            r = int(r1 + (r2 - r1) * (i / largura_canvas_grad))
            g = int(g1 + (g2 - g1) * (i / largura_canvas_grad))
            b = int(b1 + (b2 - b1) * (i / largura_canvas_grad))
            cor = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas_fundo.create_line(i, 0, i, altura_canvas_grad, fill=cor, tags="gradient")

        # Desenha o título
        self.canvas_fundo.create_text(
            self.LARGURA_JANELA / 2, self.ALTURA_JANELA * 0.10,
            text="SafeFile - Relatório", font=self.fonte_titulo_str,
            fill=self.cor_texto_titulo, tags="titulo_safefile", anchor="center"
        )
        
        # Garante que o botão de voltar fique visível
        if hasattr(self, 'botao_voltar_widget') and self.botao_voltar_widget.winfo_exists():
            self.botao_voltar_widget.lift()

    def criar_botao_voltar(self):
        """Cria o botão para voltar à tela de gerenciamento."""
        self.botao_voltar_widget = tk.Button(
            self.janela, text="Voltar ao Gerenciador", font=self.fonte_botao_acao_str,
            fg=self.cor_botao_voltar_inicio_fg, bg=self.cor_botao_voltar_inicio_bg,
            activebackground=self.cor_azul_claro, activeforeground="white",
            command=self.voltar_ao_gerenciador, relief=tk.FLAT, borderwidth=0,
            highlightthickness=0, cursor="hand2"
        )
        self.botao_voltar_widget.place(relx=0.98, rely=0.02, anchor="ne", x=-10, y=10)

    def criar_tabela_relatorio(self):
        """Cria e configura o Treeview para exibir os documentos."""
        tree_frame = tk.Frame(self.janela)
        tree_frame.place(relx=0.05, rely=0.26, relwidth=0.9, relheight=0.65)

        self.tree = ttk.Treeview(tree_frame, columns=("nome", "caminho", "tipo", "data", "tamanho"), style="mystyle.Treeview")
        self.tree.heading("#0", text="")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("caminho", text="Caminho")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("data", text="Data de Criação")
        self.tree.heading("tamanho", text="Tamanho (MB)")

        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("nome", width=150)
        self.tree.column("caminho", width=200)
        self.tree.column("tipo", width=100)
        self.tree.column("data", width=150)
        self.tree.column("tamanho", width=100)

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def atualizar_lista_documentos(self):
        """Limpa o Treeview e o preenche com os documentos do banco de dados."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            documentos = self.banco.buscar_todos_documentos()
            for doc in documentos:
                self.tree.insert("", "end", values=(
                    doc.nome_arquivo,
                    doc.caminho,
                    doc.tipo_arquivo,
                    doc.data_criacao.strftime('%Y-%m-%d %H:%M:%S'),
                    f"{doc.tamanho_mb:.2f}"
                ))
        except Exception as e:
            messagebox.showerror("Erro ao Carregar", f"Não foi possível carregar os documentos do banco de dados:\n{e}", parent=self.janela)

    def carregar_dados_iniciais(self):
        """Carrega os dados iniciais na tabela."""
        self.atualizar_lista_documentos()
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_janela)

    def voltar_ao_gerenciador(self):
        """Navega de volta para a tela de gerenciamento."""
        self.abrir_nova_janela("gerenciamento.py")

    def abrir_nova_janela(self, nome_arquivo_py):
        """Fecha a janela atual e abre um novo script Python."""
        print(f"Relatório: Tentando abrir '{nome_arquivo_py}'...")
        try:
            script_dir = os.path.dirname(__file__)
            caminho_script = os.path.join(script_dir, nome_arquivo_py)

            if os.path.exists(caminho_script):
                self.fechar_janela() # Fecha a conexão com o banco e destrói a janela
                subprocess.Popen([sys.executable, caminho_script])
            else:
                messagebox.showerror("Erro de Navegação", f"Arquivo '{nome_arquivo_py}' não encontrado.", parent=self.janela)
        except Exception as e:
            messagebox.showerror("Erro de Navegação", f"Não foi possível iniciar '{nome_arquivo_py}':\n{e}", parent=self.janela)

    def fechar_janela(self):
        """Fecha a conexão com o banco de dados antes de fechar a janela."""
        print("Fechando conexão com o banco de dados...")
        self.banco.fechar_conexao()
        self.janela.destroy()

# --- Ponto de Entrada Principal da Aplicação ---
if __name__ == "__main__":
    janela_principal = tk.Tk()
    app = TelaRelatorio(janela_principal)
    janela_principal.mainloop()