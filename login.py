import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox
import subprocess
import sys
import os
import sqlite3
import hashlib
from banco_documento import BancoDocumento


class TelaLogin:
    def __init__(self, janela_principal):
        """Inicializa a tela de login."""
        self.janela = janela_principal
        self.janela.title("SafeFile - Login")
        self.LARGURA_JANELA = 800
        self.ALTURA_JANELA = 600
        self.janela.geometry(f"{self.LARGURA_JANELA}x{self.ALTURA_JANELA}")
        self.janela.resizable(False, False)

        # Inicializa a classe do banco
        self.banco = BancoDocumento()

        self.configurar_estilos()
        self.criar_widgets()

    def configurar_estilos(self):
        """Define as cores e fontes usadas na interface."""
        self.cor_azul_claro = "#80DEEA"
        self.cor_azul_escuro = "#3161E6"
        self.cor_texto_titulo = "white"
        self.cor_label_campo = "white"
        self.cor_botao_principal_bg = "#FFFFFF"
        self.cor_botao_principal_fg_text = "#5C00A4"
        self.cor_botao_secundario_fg_text = "white"
        self.cor_fundo_botao_secundario = self.cor_azul_escuro
        
        # Fontes
        self.fonte_titulo_str = ("Arial", 36, "bold")
        self.fonte_label_campo_str = ("Arial", 12)
        self.fonte_entry_str = ("Arial", 12)
        self.fonte_botao_login_str = ("Arial", 16, "bold")
        self.fonte_botao_secundario_str = ("Arial", 12)

    def criar_widgets(self):
        """Cria e posiciona todos os widgets na janela."""
        self.criar_fundo_gradiente()
        self.criar_campos_login()
        self.criar_botoes()

    def criar_fundo_gradiente(self):
        """Cria um canvas com um fundo gradiente e o título."""
        self.canvas_fundo = tk.Canvas(self.janela, highlightthickness=0)
        self.canvas_fundo.pack(fill="both", expand=True)

        # O bind para redesenhar o gradiente se a janela fosse redimensionável
        self.canvas_fundo.bind("<Configure>", self.desenhar_gradiente)
        
        # Desenho inicial
        self.janela.update_idletasks() 
        self.desenhar_gradiente()

    def desenhar_gradiente(self, event=None):
        """Desenha o gradiente de cores e o título no canvas."""
        self.canvas_fundo.delete("gradient", "titulo_safefile")
        
        r1, g1, b1 = self.janela.winfo_rgb(self.cor_azul_escuro)[0]//256, self.janela.winfo_rgb(self.cor_azul_escuro)[1]//256, self.janela.winfo_rgb(self.cor_azul_escuro)[2]//256
        r2, g2, b2 = self.janela.winfo_rgb(self.cor_azul_claro)[0]//256, self.janela.winfo_rgb(self.cor_azul_claro)[1]//256, self.janela.winfo_rgb(self.cor_azul_claro)[2]//256

        for i in range(self.LARGURA_JANELA):
            r = int(r1 + (r2 - r1) * (i / self.LARGURA_JANELA))
            g = int(g1 + (g2 - g1) * (i / self.LARGURA_JANELA))
            b = int(b1 + (b2 - b1) * (i / self.LARGURA_JANELA))
            cor = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas_fundo.create_line(i, 0, i, self.ALTURA_JANELA, fill=cor, tags="gradient")
        
        # Desenha o título sobre o gradiente
        self.canvas_fundo.create_text(
            self.LARGURA_JANELA / 2,
            self.ALTURA_JANELA * 0.18,
            text="SafeFile",
            font=self.fonte_titulo_str,
            fill=self.cor_texto_titulo,
            tags="titulo_safefile",
            anchor="center"
        )

    def criar_campos_login(self):
        """Cria e posiciona os campos de email e senha."""
        y_pos_label_email = 0.35
        y_pos_entry_email = 0.40
        y_pos_label_senha = 0.48
        y_pos_entry_senha = 0.53

        largura_campos = self.LARGURA_JANELA * 0.5
        altura_campos = 35

        # Email
        label_email = tk.Label(self.janela, text="Email:", font=self.fonte_label_campo_str, fg=self.cor_label_campo, bg=self.cor_azul_escuro)
        label_email.place(relx=0.5, rely=y_pos_label_email, anchor="center", width=largura_campos)
        self.entry_email = tk.Entry(self.janela, font=self.fonte_entry_str, width=40)
        self.entry_email.place(relx=0.5, rely=y_pos_entry_email, anchor="center", width=largura_campos, height=altura_campos)

        # Senha
        label_senha = tk.Label(self.janela, text="Senha:", font=self.fonte_label_campo_str, fg=self.cor_label_campo, bg=self.cor_azul_escuro)
        label_senha.place(relx=0.5, rely=y_pos_label_senha, anchor="center", width=largura_campos)
        self.entry_senha = tk.Entry(self.janela, font=self.fonte_entry_str, show="*", width=40)
        self.entry_senha.place(relx=0.5, rely=y_pos_entry_senha, anchor="center", width=largura_campos, height=altura_campos)

    def criar_botoes(self):
        """Cria e posiciona os botões de login, cadastro e voltar."""
        LARGURA_BOTAO_PIXELS = 230
        ALTURA_BOTAO_PRINCIPAL_PIXELS = 50
        ALTURA_BOTAO_SECUNDARIO_PIXELS = 45

        # Botão de Login
        botao_acessar = tk.Button(
            self.janela, text="Login", font=self.fonte_botao_login_str,
            fg=self.cor_botao_principal_fg_text, bg=self.cor_botao_principal_bg,
            activebackground="#E0E0E0", activeforeground=self.cor_botao_principal_fg_text,
            command=self.processar_login, relief=tk.FLAT, borderwidth=0, highlightthickness=0
        )
        botao_acessar.place(relx=0.5, rely=0.65, anchor="center", width=LARGURA_BOTAO_PIXELS, height=ALTURA_BOTAO_PRINCIPAL_PIXELS)

        # Botão para Cadastro
        botao_link_cadastro = tk.Button(
            self.janela, text="Primeira vez? Cadastre-se", font=self.fonte_botao_secundario_str,
            fg=self.cor_botao_secundario_fg_text, bg=self.cor_fundo_botao_secundario,
            activebackground=self.cor_azul_claro, activeforeground="white",
            command=self.ir_para_cadastro, relief=tk.FLAT, bd=0, highlightthickness=0, cursor="hand2"
        )
        botao_link_cadastro.place(relx=0.5, rely=0.75, anchor="center", width=LARGURA_BOTAO_PIXELS, height=ALTURA_BOTAO_SECUNDARIO_PIXELS)

        # Botão Voltar para Início
        botao_voltar_inicio = tk.Button(
            self.janela, text="Voltar para o Início", font=self.fonte_botao_secundario_str,
            fg=self.cor_botao_secundario_fg_text, bg=self.cor_fundo_botao_secundario,
            activebackground=self.cor_azul_claro, activeforeground="white",
            command=self.ir_para_inicio, relief=tk.FLAT, bd=0, highlightthickness=0, cursor="hand2"
        )
        botao_voltar_inicio.place(relx=0.5, rely=0.85, anchor="center", width=LARGURA_BOTAO_PIXELS, height=ALTURA_BOTAO_SECUNDARIO_PIXELS)

    def gerar_hash_senha(self, senha):
        """Gera um hash SHA-256 para a senha fornecida."""
        return hashlib.sha256(senha.encode()).hexdigest()

    def processar_login(self):
        """Valida as credenciais de login e navega para a próxima tela."""
        email = self.entry_email.get().strip()
        senha = self.entry_senha.get().strip()

        if not email or not senha:
            messagebox.showwarning("Campos Vazios", "Por favor, preencha seu email e senha.")
            return

        try:
            self.banco.conectar()
            resultado = self.banco.verificar_login(email, senha)
            self.banco.fechar_conexao()
            
            if resultado:
                nome_db, senha_hash_db = resultado
                senha_hash_digitada = self.gerar_hash_senha(senha)

                if senha_hash_db == senha_hash_digitada:
                    messagebox.showinfo("Login Bem-Sucedido", f"Bem-vindo, {nome_db}!")
                    self.abrir_nova_janela("gerenciador.py", nome_db)
                else:
                    messagebox.showerror("Erro", "Senha incorreta.")
            else:
                messagebox.showerror("Erro", "Email não encontrado.")
        except sqlite3.Error as e_sql:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao acessar o banco de dados:\n{e_sql}")
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro:\n{e}")

    def abrir_nova_janela(self, nome_arquivo_py, *args):
        """Fecha a janela atual e abre um novo script Python."""
        print(f"Tentando abrir '{nome_arquivo_py}'...")
        try:
            script_dir = os.path.dirname(__file__)
            caminho_script = os.path.join(script_dir, nome_arquivo_py)

            if os.path.exists(caminho_script):
                self.janela.destroy()
                subprocess.Popen([sys.executable, caminho_script] + list(args))
            else:
                messagebox.showerror("Erro de Navegação", f"Arquivo '{nome_arquivo_py}' não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro de Navegação", f"Não foi possível iniciar '{nome_arquivo_py}':\n{e}")
    
    def ir_para_cadastro(self):
        """Navega para a tela de cadastro."""
        self.abrir_nova_janela("cadastro.py")

    def ir_para_inicio(self):
        """Navega para a tela de início."""
        self.abrir_nova_janela("inicio.py")

# --- Ponto de Entrada Principal da Aplicação ---
if __name__ == "__main__":
    janela_principal = tk.Tk()
    app = TelaLogin(janela_principal)
    janela_principal.mainloop()