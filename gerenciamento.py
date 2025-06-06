import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
from banco_documento import BancoDocumento
from documento import Documento
from datetime import datetime
import subprocess
import sys

class TelaGerenciador:
    def __init__(self, janela_principal):
        self.janela = janela_principal
        self.janela.title("SafeFile - Gerenciador de Documentos")
        self.LARGURA_JANELA = 800
        self.ALTURA_JANELA = 600
        self.janela.geometry(f"{self.LARGURA_JANELA}x{self.ALTURA_JANELA}")
        self.janela.resizable(False, False)

        self.banco = BancoDocumento()
        self.banco.conectar()

        self.configurar_estilos()
        self.criar_variaveis_tk()
        self.criar_widgets()
        self.carregar_dados_iniciais()

    def configurar_estilos(self):
        self.cor_azul_claro = "#80DEEA"
        self.cor_azul_escuro = "#3161E6"
        self.cor_texto_titulo = "white"
        self.cor_botao_acao_bg = "#FFFFFF"
        self.cor_botao_acao_fg_text = "#3161E6"
        self.cor_botao_voltar_bg = "#D32F2F"
        self.cor_botao_voltar_fg = "white"

        self.fonte_titulo_str = ("Arial", 36, "bold")
        self.fonte_geral_str = ("Arial", 10)
        self.fonte_botao_acao_str = ("Arial", 10, "bold")
        self.fonte_botao_voltar_str = ("Arial", 10, "bold")

    def criar_variaveis_tk(self):
        self.var_nome_arquivo = tk.StringVar()
        self.var_caminho = tk.StringVar()
        self.var_tipo_arquivo = tk.StringVar()
        self.var_tamanho_mb = tk.StringVar()
        self.var_documento_selecionado = tk.StringVar(value="Novo documento")

    def criar_widgets(self):
        self.criar_fundo_gradiente()
        self.criar_formulario_central()
        self.criar_botoes_inferiores()

    def criar_fundo_gradiente(self):
        self.canvas_fundo = tk.Canvas(self.janela, highlightthickness=0)
        self.canvas_fundo.pack(fill="both", expand=True)
        self.canvas_fundo.bind("<Configure>", self.desenhar_gradiente)

        # Botão para voltar ao Gerenciador de Arquivos
        tk.Button(self.janela, text="Voltar ao Gerenciador", font=self.fonte_botao_voltar_str,
                  fg=self.cor_botao_voltar_fg, bg=self.cor_botao_voltar_bg,
                  command=self.ir_para_gerenciador, relief=tk.FLAT, borderwidth=0,
                  highlightthickness=0, cursor="hand2").place(relx=0.98, rely=0.02, anchor="ne", x=-10, y=10)
        
        self.janela.update_idletasks()
        self.desenhar_gradiente()
    
    def desenhar_gradiente(self, event=None):
        self.canvas_fundo.delete("gradient")
        largura, altura = self.LARGURA_JANELA, self.ALTURA_JANELA
        
        r1, g1, b1 = self.janela.winfo_rgb(self.cor_azul_escuro)[0]//256, self.janela.winfo_rgb(self.cor_azul_escuro)[1]//256, self.janela.winfo_rgb(self.cor_azul_escuro)[2]//256
        r2, g2, b2 = self.janela.winfo_rgb(self.cor_azul_claro)[0]//256, self.janela.winfo_rgb(self.cor_azul_claro)[1]//256, self.janela.winfo_rgb(self.cor_azul_claro)[2]//256

        for i in range(largura):
            r, g, b = int(r1 + (r2-r1) * i/largura), int(g1 + (g2-g1) * i/largura), int(b1 + (b2-b1) * i/largura)
            cor = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas_fundo.create_line(i, 0, i, altura, fill=cor, tags="gradient")
            
        self.canvas_fundo.create_text(
            largura / 2, altura * 0.10, text="SafeFile - Documentos",
            font=self.fonte_titulo_str, fill=self.cor_texto_titulo, tags="titulo_safefile"
        )
        
        if hasattr(self, 'frame_central'): self.frame_central.lift()
        if hasattr(self, 'frame_botoes_acao'): self.frame_botoes_acao.lift()

    def criar_formulario_central(self):
        self.frame_central = tk.Frame(self.janela, bg=self.cor_azul_claro, bd=2, relief=tk.GROOVE)
        self.frame_central.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)

        self.combo_documentos = ttk.Combobox(self.frame_central, textvariable=self.var_documento_selecionado, state="readonly", font=self.fonte_geral_str)
        self.combo_documentos.pack(pady=10)
        self.combo_documentos.bind("<<ComboboxSelected>>", self.atualizar_formulario)

        campos = [("Nome do Arquivo:", self.var_nome_arquivo), ("Caminho:", self.var_caminho),
                  ("Tipo do Arquivo:", self.var_tipo_arquivo), ("Tamanho (MB):", self.var_tamanho_mb)]

        for label_text, var in campos:
            frame_campo = tk.Frame(self.frame_central, bg=self.cor_azul_claro)
            frame_campo.pack(pady=5, fill='x', padx=20)
            tk.Label(frame_campo, text=label_text, font=self.fonte_geral_str, bg=self.cor_azul_claro).pack(anchor="w")
            tk.Entry(frame_campo, textvariable=var, font=self.fonte_geral_str, width=80).pack(anchor="w")

        tk.Button(self.frame_central, text="Salvar Alterações", font=self.fonte_botao_acao_str,
                  fg=self.cor_botao_acao_fg_text, bg=self.cor_botao_acao_bg, command=self.enviar_formulario,
                  relief=tk.FLAT, activebackground="#E0E0E0", activeforeground=self.cor_botao_acao_fg_text,
                  width=20, height=2).pack(pady=10)

    def criar_botoes_inferiores(self):
        self.frame_botoes_acao = tk.Frame(self.janela, bd=2, relief=tk.GROOVE)
        self.frame_botoes_acao.place(relx=0.05, rely=0.90, relwidth=0.9, height=50)

        botoes_info = [("Excluir Documento", self.excluir_documento), ("Acessar Relatório", self.acessar_relatorio)]

        for texto, comando in botoes_info:
            tk.Button(self.frame_botoes_acao, text=texto, command=comando,
                      font=self.fonte_botao_acao_str, fg=self.cor_botao_acao_fg_text, bg=self.cor_botao_acao_bg,
                      relief=tk.FLAT, activebackground="#E0E0E0", activeforeground=self.cor_botao_acao_fg_text,
                      width=20, height=2).pack(side=tk.LEFT, expand=True, padx=5, pady=5)

    def atualizar_formulario(self, event=None):
        documento_selecionado = self.var_documento_selecionado.get()
        if documento_selecionado == "Novo documento":
            self.var_nome_arquivo.set("")
            self.var_caminho.set("")
            self.var_tipo_arquivo.set("")
            self.var_tamanho_mb.set("")
        else:
            documento = self.banco.buscar_documento_por_nome(documento_selecionado)
            if documento:
                self.var_nome_arquivo.set(documento.nome_arquivo)
                self.var_caminho.set(documento.caminho)
                self.var_tipo_arquivo.set(documento.tipo_arquivo)
                self.var_tamanho_mb.set(str(documento.tamanho_mb))

    def atualizar_combobox(self):
        documentos = self.banco.buscar_todos_documentos()
        valores = ["Novo documento"] + [doc.nome_arquivo for doc in documentos]
        self.combo_documentos['values'] = valores
        self.combo_documentos.set("Novo documento")
        self.atualizar_formulario()

    def enviar_formulario(self):
        nome_arquivo, caminho, tipo_arquivo, tamanho_mb_str = (self.var_nome_arquivo.get(), self.var_caminho.get(),
                                                               self.var_tipo_arquivo.get(), self.var_tamanho_mb.get())

        if not all([nome_arquivo, caminho, tipo_arquivo, tamanho_mb_str]):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!", parent=self.janela)
            return

        try:
            tamanho_mb = float(tamanho_mb_str)
        except ValueError:
            messagebox.showerror("Erro", "O tamanho deve ser um número válido!", parent=self.janela)
            return

        doc = Documento(nome_arquivo, caminho, tipo_arquivo, datetime.now(), tamanho_mb)
        doc_selecionado = self.var_documento_selecionado.get()

        try:
            if doc_selecionado == "Novo documento":
                self.banco.inserir_documento(doc)
                messagebox.showinfo("Sucesso", "Documento adicionado!", parent=self.janela)
            else:
                self.banco.atualizar_documento_por_nome(doc_selecionado, doc)
                messagebox.showinfo("Sucesso", "Documento atualizado!", parent=self.janela)
            self.atualizar_combobox()
        except Exception as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao processar documento: {e}", parent=self.janela)

    def excluir_documento(self):
        doc_selecionado = self.var_documento_selecionado.get()
        if doc_selecionado == "Novo documento":
            messagebox.showerror("Erro", "Selecione um documento para excluir!", parent=self.janela)
            return

        if messagebox.askyesno("Confirmar", f"Deseja realmente excluir o documento '{doc_selecionado}'?", parent=self.janela):
            try:
                self.banco.apagar_documento(doc_selecionado)
                messagebox.showinfo("Sucesso", "Documento excluído!", parent=self.janela)
                self.atualizar_combobox()
            except Exception as e:
                messagebox.showerror("Erro de Banco de Dados", f"Erro ao excluir documento: {e}", parent=self.janela)

    def acessar_relatorio(self):
        self.abrir_nova_janela("relatorio.py")
    
    def carregar_dados_iniciais(self):
        self.atualizar_combobox()
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        
    def abrir_nova_janela(self, nome_arquivo_py):
        try:
            caminho_script = os.path.join(os.path.dirname(__file__), nome_arquivo_py)
            if os.path.exists(caminho_script):
                self.fechar_janela()
                subprocess.Popen([sys.executable, caminho_script])
            else:
                messagebox.showerror("Erro de Navegação", f"Arquivo '{nome_arquivo_py}' não encontrado.", parent=self.janela)
        except Exception as e:
            messagebox.showerror("Erro de Navegação", f"Não foi possível iniciar '{nome_arquivo_py}':\n{e}", parent=self.janela)
            
    def ir_para_gerenciador(self):
        self.abrir_nova_janela("gerenciador.py")
            
    def fechar_janela(self):
        self.banco.fechar_conexao()
        self.janela.destroy()

if __name__ == "__main__":
    janela_principal = tk.Tk()
    app = TelaGerenciador(janela_principal)
    janela_principal.mainloop()
