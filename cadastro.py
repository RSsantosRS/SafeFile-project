import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
import sqlite3
import hashlib
from banco_documento import BancoDocumento
from usuario import Usuario


class TelaCadastro:
    def __init__(self, janela_principal):
        """Inicializa a tela de cadastro."""
        self.janela = janela_principal
        self.janela.title("SafeFile - Cadastro")
        self.janela.geometry("800x600")
        self.janela.resizable(False, False)

        # Constantes e Estilos
        self.CPF_PLACEHOLDER_TEXT = "somente números..."
        self.CPF_PLACEHOLDER_COLOR = "grey"
        self.CPF_NORMAL_TEXT_COLOR = "black"
        
        self.configurar_estilos()
        
        # Inicializa a classe do banco
        self.banco = BancoDocumento()

        # Cria a interface gráfica
        self.criar_widgets()

    def configurar_estilos(self):
        """Define as cores e fontes usadas na interface."""
        self.cor_azul_claro = "#80DEEA"
        self.cor_azul_escuro = "#3161E6"
        self.cor_label_campo = "white"
        self.cor_botao_principal_bg = "#FFFFFF"
        self.cor_botao_principal_fg_text = "#5C00A4"
        self.cor_botao_secundario_fg_text = "white"
        self.cor_fundo_botao_secundario = self.cor_azul_escuro

        self.fonte_titulo_str = ("Arial", 36, "bold")
        self.fonte_label_campo_str = ("Arial", 12)
        self.fonte_entry_str = ("Arial", 12)
        self.fonte_botao_cadastrar_str = ("Arial", 16, "bold")
        self.fonte_botao_voltar_str = ("Arial", 12)

    def criar_widgets(self):
        """Cria e posiciona todos os widgets na janela."""
        self.criar_fundo_gradiente()
        self.criar_formulario_cadastro()
        self.criar_botoes_navegacao()

    def criar_fundo_gradiente(self):
        """Cria um canvas com um fundo gradiente e o título."""
        self.canvas_fundo = tk.Canvas(self.janela, highlightthickness=0)
        self.canvas_fundo.pack(fill="both", expand=True)
        self.canvas_fundo.bind("<Configure>", self.desenhar_gradiente)

    def desenhar_gradiente(self, event=None):
        """Desenha o gradiente de cores e o título no canvas."""
        self.canvas_fundo.delete("gradient", "titulo")
        w = self.canvas_fundo.winfo_width()
        h = self.canvas_fundo.winfo_height()
        
        if w <= 1 or h <= 1: return

        r1, g1, b1 = [x//256 for x in self.janela.winfo_rgb(self.cor_azul_escuro)]
        r2, g2, b2 = [x//256 for x in self.janela.winfo_rgb(self.cor_azul_claro)]

        for i in range(w):
            r, g, b = int(r1 + (r2-r1)*i/w), int(g1 + (g2-g1)*i/w), int(b1 + (b2-b1)*i/w)
            cor = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas_fundo.create_line(i, 0, i, h, fill=cor, tags="gradient")
            
        self.canvas_fundo.create_text(
            400, 72, text="SafeFile", font=self.fonte_titulo_str,
            fill="white", tags="titulo"
        )

    def _adicionar_label_entry(self, texto, y_label, y_entry):
        """Helper para criar um par de Label e Entry."""
        tk.Label(self.janela, text=texto, font=self.fonte_label_campo_str, fg=self.cor_label_campo, bg=self.cor_azul_escuro).place(
            relx=0.5, rely=y_label, anchor="center", width=400
        )
        entry = tk.Entry(self.janela, font=self.fonte_entry_str, width=40)
        entry.place(relx=0.5, rely=y_entry, anchor="center", width=400, height=35)
        return entry

    def criar_formulario_cadastro(self):
        """Cria os campos de entrada de dados para o cadastro."""
        self.entry_nome = self._adicionar_label_entry("Nome Completo:", 0.25, 0.30)
        self.entry_email = self._adicionar_label_entry("Email:", 0.36, 0.41)
        self.entry_senha = self._adicionar_label_entry("Senha:", 0.47, 0.52)
        self.entry_senha.config(show="*")

        # Campo CPF com placeholder
        tk.Label(self.janela, text="CPF:", font=self.fonte_label_campo_str, fg=self.cor_label_campo, bg=self.cor_azul_escuro).place(
            relx=0.5, rely=0.58, anchor="center", width=400
        )
        self.entry_cpf = tk.Entry(self.janela, font=self.fonte_entry_str, fg=self.CPF_PLACEHOLDER_COLOR, width=40)
        self.entry_cpf.insert(0, self.CPF_PLACEHOLDER_TEXT)
        self.entry_cpf.bind("<FocusIn>", self._on_cpf_focus_in)
        self.entry_cpf.bind("<FocusOut>", self._on_cpf_focus_out)
        self.entry_cpf.place(relx=0.5, rely=0.63, anchor="center", width=400, height=35)

    def criar_botoes_navegacao(self):
        """Cria os botões de ação (Cadastrar e Voltar)."""
        tk.Button(self.janela, text="Cadastrar", font=self.fonte_botao_cadastrar_str,
                  fg=self.cor_botao_principal_fg_text, bg=self.cor_botao_principal_bg,
                  command=self.processar_cadastro, relief=tk.FLAT).place(
                      relx=0.5, rely=0.73, anchor="center", width=230, height=50
                  )

        tk.Button(self.janela, text="Voltar", font=self.fonte_botao_voltar_str,
                  fg=self.cor_botao_secundario_fg_text, bg=self.cor_fundo_botao_secundario,
                  command=self.ir_para_inicio, relief=tk.FLAT).place(
                      relx=0.5, rely=0.81, anchor="center", width=230, height=45
                  )

    # --- Lógica de Eventos e Processamento ---
    
    def _on_cpf_focus_in(self, event):
        """Limpa o placeholder do CPF quando o campo recebe foco."""
        if self.entry_cpf.get() == self.CPF_PLACEHOLDER_TEXT:
            self.entry_cpf.delete(0, tk.END)
            self.entry_cpf.config(fg=self.CPF_NORMAL_TEXT_COLOR)

    def _on_cpf_focus_out(self, event):
        """Restaura o placeholder do CPF se o campo estiver vazio ao perder o foco."""
        if not self.entry_cpf.get():
            self.entry_cpf.insert(0, self.CPF_PLACEHOLDER_TEXT)
            self.entry_cpf.config(fg=self.CPF_PLACEHOLDER_COLOR)

    def processar_cadastro(self):
        """Coleta, valida e envia os dados do formulário para o banco."""
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        senha = self.entry_senha.get().strip()
        cpf_valor = self.entry_cpf.get().strip()
        cpf_final = "" if cpf_valor == self.CPF_PLACEHOLDER_TEXT else cpf_valor

        if not nome or not email or not senha or not cpf_final:
            messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos.")
            return

        if not cpf_final.isdigit():
            messagebox.showwarning("CPF Inválido", "O CPF deve conter apenas números.")
            return

        try:
            self.banco.conectar()
            self.banco.inserir_usuario(Usuario(cpf=cpf_final, senha=senha, nome=nome, email=email))
            self.banco.fechar_conexao()
            messagebox.showinfo("Cadastro Realizado", "Usuário cadastrado com sucesso!")
            self.abrir_nova_janela("login.py")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro de Cadastro", "CPF ou Email já cadastrado.")
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro ao cadastrar: {e}")

    # --- Funções de Navegação ---

    def abrir_nova_janela(self, nome_arquivo_py):
        """Fecha a janela atual e abre um novo script Python."""
        print(f"Navegando para '{nome_arquivo_py}'...")
        try:
            caminho_script = os.path.join(os.path.dirname(__file__), nome_arquivo_py)
            if os.path.exists(caminho_script):
                self.janela.destroy()
                subprocess.Popen([sys.executable, caminho_script])
            else:
                messagebox.showerror("Erro de Navegação", f"Arquivo '{nome_arquivo_py}' não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro de Navegação", f"Não foi possível iniciar '{nome_arquivo_py}':\n{e}")

    def ir_para_inicio(self):
        """Navega para a tela de início."""
        self.abrir_nova_janela("inicio.py")

# --- Ponto de Entrada Principal da Aplicação ---
if __name__ == "__main__":
    janela_principal = tk.Tk()
    app = TelaCadastro(janela_principal)
    janela_principal.mainloop()