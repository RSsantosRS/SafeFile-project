import tkinter as tk
from tkinter import font as tkFont
import subprocess
import sys
import os


class TelaPrincipal:
    def __init__(self, janela_principal):
        """Inicializa a tela principal (menu)."""
        self.janela = janela_principal
        self.janela.title("SafeFile - Menu Principal")
        self.LARGURA_JANELA = 800
        self.ALTURA_JANELA = 600
        self.janela.geometry(f"{self.LARGURA_JANELA}x{self.ALTURA_JANELA}")
        self.janela.resizable(False, False)

        self.configurar_estilos()
        self.criar_widgets()

    def configurar_estilos(self):
        """Define as cores e fontes usadas na interface."""
        self.cor_azul_claro = "#80DEEA"
        self.cor_azul_escuro = "#3161E6"
        self.cor_texto_titulo = "white"
        self.cor_botao_login_bg = "#FFFFFF" 
        self.cor_botao_login_fg_text = "#5C00A4" 
        self.cor_botao_secundario_fg_text = "white" 
        self.cor_fundo_botao_secundario = self.cor_azul_escuro

        # Fontes
        self.fonte_titulo_str = ("Arial", 36, "bold")
        self.fonte_botao_principal_str = ("Arial", 18, "bold")
        self.fonte_botao_secundario_str = ("Arial", 12)

    def criar_widgets(self):
        """Cria e posiciona todos os widgets na janela."""
        self.criar_fundo_gradiente()
        self.criar_botoes()

    def criar_fundo_gradiente(self):
        """Cria um canvas com um fundo gradiente e o título."""
        self.canvas_fundo = tk.Canvas(self.janela, highlightthickness=0)
        self.canvas_fundo.pack(fill="both", expand=True)
        self.canvas_fundo.bind("<Configure>", self.desenhar_gradiente)
        
        # Garante o primeiro desenho
        self.janela.update_idletasks()
        self.desenhar_gradiente()

    def desenhar_gradiente(self, event=None):
        """Desenha o gradiente de cores e o título no canvas."""
        self.canvas_fundo.delete("gradient")
        
        largura_canvas = self.canvas_fundo.winfo_width()
        altura_canvas = self.canvas_fundo.winfo_height()

        if largura_canvas <= 1 or altura_canvas <= 1:
            return

        r1, g1, b1 = self.janela.winfo_rgb(self.cor_azul_escuro)[0]//256, self.janela.winfo_rgb(self.cor_azul_escuro)[1]//256, self.janela.winfo_rgb(self.cor_azul_escuro)[2]//256
        r2, g2, b2 = self.janela.winfo_rgb(self.cor_azul_claro)[0]//256, self.janela.winfo_rgb(self.cor_azul_claro)[1]//256, self.janela.winfo_rgb(self.cor_azul_claro)[2]//256

        for i in range(largura_canvas):
            r = int(r1 + (r2 - r1) * (i / largura_canvas))
            g = int(g1 + (g2 - g1) * (i / largura_canvas))
            b = int(b1 + (b2 - b1) * (i / largura_canvas))
            cor = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas_fundo.create_line(i, 0, i, altura_canvas, fill=cor, tags="gradient")

        # Desenha o título
        self.canvas_fundo.create_text(
            self.LARGURA_JANELA / 2, self.ALTURA_JANELA * 0.22,
            text="SafeFile", font=self.fonte_titulo_str,
            fill=self.cor_texto_titulo, tags="titulo_safefile", anchor="center"
        )

    def criar_botoes(self):
        """Cria e posiciona os botões de navegação."""
        LARGURA_BOTAO_PIXELS = 230
        ALTURA_BOTAO_PRINCIPAL_PIXELS = 50 
        ALTURA_BOTAO_SECUNDARIO_PIXELS = 45 

        # Botão Login
        botao_login = tk.Button(
            self.janela, text="Login", font=self.fonte_botao_principal_str, 
            fg=self.cor_botao_login_fg_text, bg=self.cor_botao_login_bg,
            activebackground="#E0E0E0", activeforeground=self.cor_botao_login_fg_text,
            command=self.ir_para_login, relief=tk.FLAT, borderwidth=0, highlightthickness=0
        )
        botao_login.place(relx=0.5, rely=0.50, anchor="center", width=LARGURA_BOTAO_PIXELS, height=ALTURA_BOTAO_PRINCIPAL_PIXELS)

        # Botão Cadastro
        botao_cadastro = tk.Button(
            self.janela, text="Primeira vez? Cadastre-se", font=self.fonte_botao_secundario_str, 
            fg=self.cor_botao_secundario_fg_text, bg=self.cor_fundo_botao_secundario,
            activebackground=self.cor_azul_claro, activeforeground="white",
            command=self.ir_para_cadastro, relief=tk.FLAT, bd=0, highlightthickness=0
        )
        botao_cadastro.place(relx=0.5, rely=0.62, anchor="center", width=LARGURA_BOTAO_PIXELS, height=ALTURA_BOTAO_SECUNDARIO_PIXELS)

        # Botão Voltar ao Início (caso esta tela seja chamada de outra)
        botao_inicio = tk.Button(
            self.janela, text="Voltar para o Início", font=self.fonte_botao_secundario_str, 
            fg=self.cor_botao_secundario_fg_text, bg=self.cor_fundo_botao_secundario,
            activebackground=self.cor_azul_claro, activeforeground="white",
            command=self.ir_para_inicio, relief=tk.FLAT, bd=0, highlightthickness=0
        )
        botao_inicio.place(relx=0.5, rely=0.74, anchor="center", width=LARGURA_BOTAO_PIXELS, height=ALTURA_BOTAO_SECUNDARIO_PIXELS)

    def abrir_nova_janela(self, nome_arquivo_py):
        """Fecha a janela atual e abre um novo script Python."""
        print(f"Navegando para '{nome_arquivo_py}'...")
        try:
            script_dir = os.path.dirname(__file__)
            caminho_script = os.path.join(script_dir, nome_arquivo_py)

            if os.path.exists(caminho_script):
                self.janela.destroy()
                subprocess.Popen([sys.executable, caminho_script])
            else:
                print(f"Erro: O arquivo '{caminho_script}' não foi encontrado.")
                # Em uma aplicação real, você poderia mostrar um messagebox aqui.
        except Exception as e:
            print(f"Erro ao tentar executar {nome_arquivo_py}: {e}")

    def ir_para_login(self):
        """Navega para a tela de login."""
        self.abrir_nova_janela("login.py")

    def ir_para_cadastro(self):
        """Navega para a tela de cadastro."""
        self.abrir_nova_janela("cadastro.py")
        
    def ir_para_inicio(self):
        """Navega para a tela de início (a própria tela, neste caso)."""
        # Se esta tela for a "inicio.py", este botão pode fechar e reabrir a si mesmo
        # ou, alternativamente, não fazer nada ou ir para uma tela "splash".
        # Vamos assumir que ele recarrega a si mesmo.
        self.abrir_nova_janela("inicio.py")

# --- Ponto de Entrada Principal da Aplicação ---
if __name__ == "__main__":
    janela_principal = tk.Tk()
    app = TelaPrincipal(janela_principal)
    janela_principal.mainloop()