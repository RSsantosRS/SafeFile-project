import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
import os
import shutil
import sys
import subprocess

class TelaGerenciadorArquivos:
    def __init__(self, janela_principal):
        self.janela = janela_principal
        self.janela.title("SafeFile - Gerenciador de Arquivos")
        self.LARGURA_JANELA = 800
        self.ALTURA_JANELA = 600
        self.janela.geometry(f"{self.LARGURA_JANELA}x{self.ALTURA_JANELA}")
        self.janela.resizable(False, False)

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
        self.cor_botao_navegacao_bg = self.cor_azul_escuro
        self.cor_botao_navegacao_fg_text = "white"
        self.cor_botao_voltar_inicio_bg = "#D32F2F"
        self.cor_botao_voltar_inicio_fg = "white"
        
        self.fonte_titulo_str = ("Arial", 36, "bold")
        self.fonte_botao_acao_str = ("Arial", 10, "bold")
        self.fonte_treeview_str = ("Arial", 10)
        self.fonte_path_entry_str = ("Arial", 10)
        self.fonte_botao_voltar_inicio_str = ("Arial", 10, "bold")

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=self.fonte_treeview_str, rowheight=25)
        style.configure("mystyle.Treeview.Heading", font=(self.fonte_treeview_str[0], int(self.fonte_treeview_str[1]), "bold"))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

    def criar_variaveis_tk(self):
        self.diretorio_atual = tk.StringVar(value=os.path.abspath(os.getcwd()))

    def criar_widgets(self):
        self.criar_fundo_gradiente()
        self.criar_navegacao_superior()
        self.criar_visualizador_arquivos()
        self.criar_botoes_acao()

    def criar_fundo_gradiente(self):
        self.canvas_fundo = tk.Canvas(self.janela, highlightthickness=0)
        self.canvas_fundo.pack(fill="both", expand=True)
        self.canvas_fundo.bind("<Configure>", self.desenhar_gradiente)

        tk.Button(self.janela, text="Voltar ao Início", font=self.fonte_botao_voltar_inicio_str,
                  fg=self.cor_botao_voltar_inicio_fg, bg=self.cor_botao_voltar_inicio_bg,
                  command=self.ir_para_script_inicio, relief=tk.FLAT, borderwidth=0,
                  highlightthickness=0, cursor="hand2").place(relx=0.98, rely=0.02, anchor="ne", x=-10, y=10)
        
        self.janela.update_idletasks()
        self.desenhar_gradiente()

    def desenhar_gradiente(self, event=None):
        self.canvas_fundo.delete("gradient")
        largura, altura = self.LARGURA_JANELA, self.ALTURA_JANELA

        r1,g1,b1 = self.janela.winfo_rgb(self.cor_azul_escuro)[0]//256, self.janela.winfo_rgb(self.cor_azul_escuro)[1]//256, self.janela.winfo_rgb(self.cor_azul_escuro)[2]//256
        r2,g2,b2 = self.janela.winfo_rgb(self.cor_azul_claro)[0]//256, self.janela.winfo_rgb(self.cor_azul_claro)[1]//256, self.janela.winfo_rgb(self.cor_azul_claro)[2]//256
        
        for i in range(largura):
            r,g,b = int(r1+(r2-r1)*i/largura), int(g1+(g2-g1)*i/largura), int(b1+(b2-b1)*i/largura)
            self.canvas_fundo.create_line(i,0,i,altura, fill=f'#{r:02x}{g:02x}{b:02x}', tags="gradient")

        self.canvas_fundo.create_text(
            largura/2, altura*0.10, text="SafeFile", font=self.fonte_titulo_str,
            fill=self.cor_texto_titulo, tags="titulo_safefile"
        )
        
        if hasattr(self, 'frame_navegacao'): self.frame_navegacao.lift()
        if hasattr(self, 'tree_frame'): self.tree_frame.lift()
        if hasattr(self, 'frame_botoes_acao'): self.frame_botoes_acao.lift()

    def criar_navegacao_superior(self):
        self.frame_navegacao = tk.Frame(self.janela, bg=self.cor_azul_escuro)
        self.frame_navegacao.place(relx=0.05, rely=0.18, relwidth=0.9, height=40)

        tk.Button(self.frame_navegacao, text="↑ Voltar", command=self.voltar_diretorio,
                  font=self.fonte_botao_acao_str, fg=self.cor_botao_navegacao_fg_text, bg=self.cor_botao_navegacao_bg,
                  relief=tk.FLAT, activebackground=self.cor_azul_claro, activeforeground="white").pack(side=tk.LEFT, padx=5, pady=5)

        path_entry = tk.Entry(self.frame_navegacao, textvariable=self.diretorio_atual, font=self.fonte_path_entry_str, bd=2, relief=tk.SUNKEN)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        path_entry.bind("<Return>", self.navegar_pelo_entry)
        
        tk.Button(self.frame_navegacao, text="Ir", command=self.navegar_pelo_entry,
                  font=self.fonte_botao_acao_str, fg=self.cor_botao_navegacao_fg_text, bg=self.cor_botao_navegacao_bg,
                  relief=tk.FLAT, activebackground=self.cor_azul_claro, activeforeground="white").pack(side=tk.LEFT, padx=5, pady=5)

    def criar_visualizador_arquivos(self):
        self.tree_frame = tk.Frame(self.janela)
        self.tree_frame.place(relx=0.05, rely=0.26, relwidth=0.9, relheight=0.55)

        self.tree = ttk.Treeview(self.tree_frame, columns=("path", "type"), displaycolumns=(), style="mystyle.Treeview")
        self.tree.heading("#0", text="Nome", anchor='w')
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind("<Double-1>", self.on_item_double_click)

    def criar_botoes_acao(self):
        self.frame_botoes_acao = tk.Frame(self.janela, bg=self.cor_azul_escuro)
        self.frame_botoes_acao.place(relx=0.05, rely=0.83, relwidth=0.9, height=80)

        botoes_info = [("Criar Arquivo", self.criar_arquivo), ("Criar Pasta", self.criar_pasta),
                       ("Apagar", self.apagar_item), ("Renomear", self.renomear_item),
                       ("Mover", self.mover_item), ("Gerenciador", self.abrir_gerenciamento)]

        for texto, comando in botoes_info:
            tk.Button(self.frame_botoes_acao, text=texto, command=comando,
                      font=self.fonte_botao_acao_str, fg=self.cor_botao_acao_fg_text, bg=self.cor_botao_acao_bg,
                      relief=tk.FLAT, activebackground="#E0E0E0", activeforeground=self.cor_botao_acao_fg_text,
                      width=12, height=2).pack(side=tk.LEFT, expand=True, padx=5, pady=10)

    def carregar_dados_iniciais(self):
        self.atualizar_lista_arquivos()

    def atualizar_lista_arquivos(self):
        path = self.diretorio_atual.get()
        try:
            for i in self.tree.get_children():
                self.tree.delete(i)

            if not os.path.isdir(path):
                messagebox.showerror("Erro de Caminho", f"O diretório '{path}' não existe.", parent=self.janela)
                self.diretorio_atual.set(os.path.abspath(os.getcwd()))
                return

            parent_dir = os.path.dirname(path)
            if path != parent_dir:
                self.tree.insert("", "end", text="..", values=(parent_dir, "folder_up"))

            items_list = []
            for item_name in os.listdir(path):
                try:
                    item_path = os.path.join(path, item_name)
                    is_dir = os.path.isdir(item_path)
                    items_list.append((item_name, item_path, "folder" if is_dir else "file"))
                except OSError:
                    continue
            
            items_list.sort(key=lambda x: (x[2] != 'folder', x[0].lower()))
            for item_name, item_path, tipo in items_list:
                self.tree.insert("", "end", text=item_name, values=(item_path, tipo))
        except Exception as e:
            messagebox.showerror("Erro ao Listar", f"Não foi possível listar arquivos: {e}", parent=self.janela)

    def on_item_double_click(self, event):
        item_id = self.tree.focus()
        if not item_id:
            return
        item = self.tree.item(item_id)
        path, item_type = item['values']

        if item_type in ("folder", "folder_up"):
            self.diretorio_atual.set(path)
            self.atualizar_lista_arquivos()
        elif item_type == "file":
            try:
                if sys.platform == "win32":
                    os.startfile(path)
                elif sys.platform == "darwin":
                    subprocess.call(["open", path])
                else:
                    subprocess.call(["xdg-open", path])
            except Exception as e:
                messagebox.showerror("Erro ao Abrir", f"Não foi possível abrir o arquivo:\n{e}", parent=self.janela)

    def navegar_pelo_entry(self, event=None):
        path = self.diretorio_atual.get()
        if os.path.isdir(path):
            self.atualizar_lista_arquivos()
        else:
            messagebox.showerror("Caminho Inválido", "O caminho especificado não é um diretório válido.", parent=self.janela)

    def voltar_diretorio(self):
        current_path = self.diretorio_atual.get()
        parent_path = os.path.dirname(current_path)
        if os.path.isdir(parent_path) and current_path != parent_path:
            self.diretorio_atual.set(parent_path)
            self.atualizar_lista_arquivos()

    def criar_arquivo(self):
        file_name = simpledialog.askstring("Criar Arquivo", "Digite o nome do novo arquivo:", parent=self.janela)
        if file_name:
            try:
                file_path = os.path.join(self.diretorio_atual.get(), file_name)
                if not os.path.exists(file_path):
                    with open(file_path, 'a'):
                        pass
                    self.atualizar_lista_arquivos()
                else:
                    messagebox.showwarning("Aviso", "Um arquivo com este nome já existe.", parent=self.janela)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível criar o arquivo: {e}", parent=self.janela)

    def criar_pasta(self):
        folder_name = simpledialog.askstring("Criar Pasta", "Digite o nome da nova pasta:", parent=self.janela)
        if folder_name:
            try:
                folder_path = os.path.join(self.diretorio_atual.get(), folder_name)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    self.atualizar_lista_arquivos()
                else:
                    messagebox.showwarning("Aviso", "Uma pasta com este nome já existe.", parent=self.janela)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível criar a pasta: {e}", parent=self.janela)

    def apagar_item(self):
        item_id = self.tree.focus()
        if not item_id:
            messagebox.showwarning("Nenhum item selecionado", "Por favor, selecione um item para apagar.", parent=self.janela)
            return

        item = self.tree.item(item_id)
        if item['values'][1] == 'folder_up':
            return
            
        if messagebox.askyesno("Confirmar Exclusão", f"Você tem certeza que deseja apagar '{item['text']}'?", parent=self.janela):
            try:
                item_path = item['values'][0]
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
                self.atualizar_lista_arquivos()
            except Exception as e:
                messagebox.showerror("Erro ao Apagar", f"Não foi possível apagar o item: {e}", parent=self.janela)

    def renomear_item(self):
        item_id = self.tree.focus()
        if not item_id:
            messagebox.showwarning("Nenhum item selecionado", "Por favor, selecione um item para renomear.", parent=self.janela)
            return

        item = self.tree.item(item_id)
        if item['values'][1] == 'folder_up':
            return

        old_name = item['text']
        old_path = item['values'][0]
        new_name = simpledialog.askstring("Renomear", f"Novo nome para '{old_name}':", initialvalue=old_name, parent=self.janela)
        
        if new_name and new_name != old_name:
            try:
                new_path = os.path.join(os.path.dirname(old_path), new_name)
                os.rename(old_path, new_path)
                self.atualizar_lista_arquivos()
            except Exception as e:
                messagebox.showerror("Erro ao Renomear", f"Não foi possível renomear: {e}", parent=self.janela)

    def mover_item(self):
        item_id = self.tree.focus()
        if not item_id:
            messagebox.showwarning("Nenhum item selecionado", "Por favor, selecione um item para mover.", parent=self.janela)
            return

        item = self.tree.item(item_id)
        if item['values'][1] == 'folder_up':
            return
            
        source_path = item['values'][0]
        destination_folder = filedialog.askdirectory(title=f"Selecione a pasta de destino para '{item['text']}'", parent=self.janela)
        
        if destination_folder:
            try:
                shutil.move(source_path, destination_folder)
                self.atualizar_lista_arquivos()
            except Exception as e:
                messagebox.showerror("Erro ao Mover", f"Não foi possível mover o item: {e}", parent=self.janela)

    def abrir_nova_janela(self, nome_arquivo_py):
        try:
            caminho_script = os.path.join(os.path.dirname(__file__), nome_arquivo_py)
            if os.path.exists(caminho_script):
                self.janela.destroy()
                subprocess.Popen([sys.executable, caminho_script])
            else:
                messagebox.showerror("Erro de Navegação", f"Arquivo '{nome_arquivo_py}' não encontrado.", parent=self.janela)
        except Exception as e:
            messagebox.showerror("Erro de Navegação", f"Não foi possível iniciar '{nome_arquivo_py}':\n{e}", parent=self.janela)

    def ir_para_script_inicio(self):
        self.abrir_nova_janela("inicio.py")

    def abrir_gerenciamento(self):
        self.abrir_nova_janela("gerenciamento.py")


if __name__ == "__main__":
    janela_principal = tk.Tk()
    app = TelaGerenciadorArquivos(janela_principal)
    janela_principal.mainloop()
