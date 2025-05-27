import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
from tkinter import font as tkFont # Importado mas não usado diretamente, tk.font é o padrão
import os
import shutil
import sys
import subprocess # ADICIONADO para chamar inicio.py e abrir arquivos

# --- Configurações da Janela Principal ---
janela = tk.Tk()
janela.title("SafeFile - Gerenciador de Arquivos")
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
# Cor para o novo botão "Voltar ao Início"
cor_botao_voltar_inicio_bg = "#D32F2F" # Um vermelho para destaque, ou use cor_botao_navegacao_bg
cor_botao_voltar_inicio_fg = "white"

# --- Fontes ---
fonte_titulo_str = ("Arial", 36, "bold")
fonte_geral_str = ("Arial", 10) # Não usado diretamente, mas definido
fonte_botao_acao_str = ("Arial", 10, "bold")
fonte_treeview_str = ("Arial", 10)
fonte_path_entry_str = ("Arial", 10)
fonte_botao_voltar_inicio_str = ("Arial", 10, "bold")


# --- Variável Global para Caminho Atual ---
diretorio_atual = tk.StringVar(value=os.path.abspath(os.getcwd()))

# --- Canvas para o Gradiente de Fundo ---
canvas_fundo = tk.Canvas(janela, highlightthickness=0)
canvas_fundo.pack(fill="both", expand=True)

def desenhar_titulo_no_canvas():
    canvas_fundo.delete("titulo_safefile")
    canvas_fundo.create_text(
        LARGURA_JANELA / 2,
        ALTURA_JANELA * 0.10,
        text="SafeFile",
        font=fonte_titulo_str,
        fill=cor_texto_titulo,
        tags="titulo_safefile",
        anchor="center"
    )

def desenhar_gradiente(event=None):
    canvas_fundo.delete("gradient")
    # Usa as dimensões fixas da janela para o gradiente, já que não é redimensionável
    largura_canvas_grad = LARGURA_JANELA
    altura_canvas_grad = ALTURA_JANELA

    # Fallback se as dimensões ainda forem muito pequenas no início
    if largura_canvas_grad <= 1 or altura_canvas_grad <= 1:
        largura_canvas_grad = janela.winfo_width()
        altura_canvas_grad = janela.winfo_height()
        if largura_canvas_grad <= 1 or altura_canvas_grad <= 1:
            return # Adia o desenho se as dimensões não estiverem prontas

    r1, g1, b1 = janela.winfo_rgb(cor_azul_escuro)[0]//256, janela.winfo_rgb(cor_azul_escuro)[1]//256, janela.winfo_rgb(cor_azul_escuro)[2]//256
    r2, g2, b2 = janela.winfo_rgb(cor_azul_claro)[0]//256, janela.winfo_rgb(cor_azul_claro)[1]//256, janela.winfo_rgb(cor_azul_claro)[2]//256

    for i in range(int(largura_canvas_grad)): # Certifica que é int
        # Previne divisão por zero se largura_canvas_grad for zero (embora a checagem acima deva cobrir)
        if largura_canvas_grad == 0: break
        r = int(r1 + (r2 - r1) * (i / largura_canvas_grad))
        g = int(g1 + (g2 - g1) * (i / largura_canvas_grad))
        b = int(b1 + (b2 - b1) * (i / largura_canvas_grad))
        cor = f'#{r:02x}{g:02x}{b:02x}'
        canvas_fundo.create_line(i, 0, i, altura_canvas_grad, fill=cor, tags="gradient")

    desenhar_titulo_no_canvas()
    # Levanta o botão "Voltar ao Início" para que fique sobre o gradiente, se já existir
    if 'botao_voltar_inicio_widget' in globals() and botao_voltar_inicio_widget.winfo_exists():
        botao_voltar_inicio_widget.lift()


# --- Função para Navegação para Início ---
def ir_para_script_inicio():
    print("Gerenciador: Voltando para o Início...")
    try:
        script_dir = os.path.dirname(__file__)
        caminho_inicio_py = os.path.join(script_dir, "inicio.py")

        if os.path.exists(caminho_inicio_py):
            janela.destroy() # Fecha a janela do gerenciador
            subprocess.Popen([sys.executable, caminho_inicio_py])
            print(f"Gerenciador: Executando '{caminho_inicio_py}'")
        else:
            messagebox.showerror("Erro de Navegação", f"Arquivo 'inicio.py' não encontrado em:\n{caminho_inicio_py}", parent=janela) # parent adicionado
    except Exception as e:
        messagebox.showerror("Erro de Navegação", f"Não foi possível iniciar 'inicio.py':\n{e}", parent=janela) # parent adicionado


# --- Botão Voltar ao Início ---
botao_voltar_inicio_widget = tk.Button(
    janela, # Pai é a janela principal
    text="Voltar ao Início",
    font=fonte_botao_voltar_inicio_str,
    fg=cor_botao_voltar_inicio_fg,
    bg=cor_botao_voltar_inicio_bg,
    activebackground=cor_azul_claro, # Pode ajustar a cor ativa
    activeforeground="white",
    command=ir_para_script_inicio,
    relief=tk.FLAT,
    borderwidth=0,
    highlightthickness=0,
    cursor="hand2"
)
# Posiciona no canto superior direito, abaixo da barra de título
botao_voltar_inicio_widget.place(relx=0.98, rely=0.02, anchor="ne", x=-10, y=10)


# --- Funções de Gerenciamento de Arquivos ---
def atualizar_lista_arquivos():
    try:
        path = diretorio_atual.get()
        if not os.path.isdir(path): # Validação se o path é um diretório
            messagebox.showerror("Erro de Caminho", f"O caminho '{path}' não é um diretório válido ou está inacessível.", parent=janela)
            # Tenta reverter para um diretório conhecido (ex: CWD) ou o pai do caminho inválido
            parent_dir = os.path.dirname(path)
            if os.path.isdir(parent_dir):
                diretorio_atual.set(parent_dir)
            else:
                diretorio_atual.set(os.path.abspath(os.getcwd()))
            # Chama recursivamente para tentar atualizar com o novo caminho
            # Cuidado com recursão infinita aqui, adicione um limite se necessário ou um estado.
            # Por simplicidade, vamos apenas tentar uma vez.
            path = diretorio_atual.get()
            if not os.path.isdir(path): # Se ainda não for válido, desiste.
                 messagebox.showerror("Erro Crítico", "Não foi possível encontrar um diretório válido para listar.", parent=janela)
                 return

        for i in tree.get_children():
            tree.delete(i)

        if os.path.abspath(path) != os.path.abspath(os.sep) and os.path.dirname(path) != path :
            tree.insert("", "end", text="..", values=(os.path.dirname(path), "folder_up"))

        items_list = []
        for item_name in os.listdir(path):
            item_path = os.path.join(path, item_name)
            try:
                is_dir = os.path.isdir(item_path)
                items_list.append((item_name, item_path, "folder" if is_dir else "file"))
            except OSError: # Ignora links quebrados, etc.
                continue
        
        items_list.sort(key=lambda x: (x[2] != 'folder', x[0].lower())) # Pastas primeiro, depois por nome

        for item_name, item_path, tipo in items_list:
            tree.insert("", "end", text=item_name, values=(item_path, tipo))

    except Exception as e:
        messagebox.showerror("Erro ao Listar", f"Não foi possível listar arquivos: {e}", parent=janela)
        # Em caso de erro mais genérico, não chama voltar_diretorio() para evitar loops se a causa for outra.

def on_item_double_click(event):
    if not tree.selection(): return # Se nada estiver selecionado
    item_id = tree.selection()[0]
    item_text = tree.item(item_id, "text")
    item_values = tree.item(item_id, "values")
    
    path = ""
    item_type = ""

    if not item_values: # Provavelmente o item ".."
        if item_text == "..":
            path = os.path.dirname(diretorio_atual.get())
            item_type = "folder_up"
        else:
            return # Item desconhecido sem valores
    else:
        path = item_values[0]
        item_type = item_values[1]


    if item_type == "folder" or item_type == "folder_up":
        try:
            if not os.access(path, os.R_OK):
                messagebox.showerror("Acesso Negado", f"Sem permissão para acessar:\n{path}", parent=janela)
                return
            # os.chdir(path) # Evitar mudar CWD globalmente em apps GUI se possível
            diretorio_atual.set(os.path.abspath(path))
            atualizar_lista_arquivos()
        except Exception as e:
            messagebox.showerror("Erro de Navegação", f"Não foi possível acessar o diretório: {path}\n{e}", parent=janela)
    elif item_type == "file":
        try:
            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
        except FileNotFoundError:
            cmd_missing = 'open' if sys.platform == "darwin" else 'xdg-open'
            messagebox.showerror("Erro ao Abrir", f"Comando '{cmd_missing}' não encontrado para abrir arquivos.", parent=janela)
        except Exception as e:
            messagebox.showerror("Erro ao Abrir", f"Não foi possível abrir o arquivo: {path}\n{e}", parent=janela)


def navegar_pelo_entry(event=None):
    novo_caminho = path_entry.get()
    if os.path.isdir(novo_caminho):
        if not os.access(novo_caminho, os.R_OK):
            messagebox.showerror("Acesso Negado", f"Sem permissão para acessar:\n{novo_caminho}", parent=janela)
            return
        diretorio_atual.set(os.path.abspath(novo_caminho))
        atualizar_lista_arquivos()
    else:
        messagebox.showerror("Erro de Caminho", "Caminho inválido ou não é um diretório.", parent=janela)

def voltar_diretorio():
    path_atual = diretorio_atual.get()
    path_pai = os.path.dirname(path_atual)
    if os.path.abspath(path_atual) != os.path.abspath(path_pai):
        if not os.access(path_pai, os.R_OK): # Checa permissão do pai
            messagebox.showerror("Acesso Negado", f"Sem permissão para acessar o diretório pai:\n{path_pai}", parent=janela)
            return
        diretorio_atual.set(path_pai)
        atualizar_lista_arquivos()
    else:
        messagebox.showinfo("Info", "Já está no diretório raiz.", parent=janela)

def criar_arquivo():
    nome_arquivo = simpledialog.askstring("Criar Arquivo", "Nome do novo arquivo (com extensão):", parent=janela)
    if nome_arquivo:
        if os.path.sep in nome_arquivo or any(c in nome_arquivo for c in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']):
            messagebox.showerror("Nome Inválido", "O nome do arquivo contém caracteres inválidos.", parent=janela)
            return
        caminho_completo = os.path.join(diretorio_atual.get(), nome_arquivo)
        try:
            if not os.path.exists(caminho_completo):
                with open(caminho_completo, "w", encoding='utf-8') as f: # Especificar encoding
                    f.write("")
                atualizar_lista_arquivos()
                messagebox.showinfo("Sucesso", f"Arquivo '{nome_arquivo}' criado.", parent=janela)
            else:
                messagebox.showwarning("Aviso", f"Arquivo '{nome_arquivo}' já existe.", parent=janela)
        except Exception as e:
            messagebox.showerror("Erro ao Criar", f"Não foi possível criar o arquivo: {e}", parent=janela)

def criar_pasta():
    nome_pasta = simpledialog.askstring("Criar Pasta", "Nome da nova pasta:", parent=janela)
    if nome_pasta:
        if os.path.sep in nome_pasta or any(c in nome_pasta for c in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']):
            messagebox.showerror("Nome Inválido", "O nome da pasta contém caracteres inválidos.", parent=janela)
            return
        caminho_completo = os.path.join(diretorio_atual.get(), nome_pasta)
        try:
            os.makedirs(caminho_completo, exist_ok=False) # exist_ok=False para erro se já existir
            atualizar_lista_arquivos()
            messagebox.showinfo("Sucesso", f"Pasta '{nome_pasta}' criada.", parent=janela)
        except FileExistsError:
            messagebox.showwarning("Aviso", f"A pasta '{nome_pasta}' já existe.", parent=janela)
        except Exception as e:
            messagebox.showerror("Erro ao Criar", f"Não foi possível criar a pasta: {e}", parent=janela)

def apagar_item():
    if not tree.selection():
        messagebox.showwarning("Aviso", "Nenhum item selecionado.", parent=janela)
        return

    item_id = tree.selection()[0]
    nome_item = tree.item(item_id, "text")
    item_values = tree.item(item_id, "values")

    if not item_values and nome_item == "..": # Checa se é o item ".."
        messagebox.showwarning("Aviso", "Não é possível apagar o item de navegação '..'.", parent=janela)
        return
    elif not item_values: # Outro item sem valor (improvável com a lógica atual)
        messagebox.showerror("Erro", "Item selecionado inválido para exclusão.", parent=janela)
        return
        
    caminho_item = item_values[0]

    confirmar = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja apagar '{nome_item}'?\nEsta ação é irreversível!", icon='warning', parent=janela)
    if confirmar:
        try:
            if os.path.isfile(caminho_item):
                os.remove(caminho_item)
            elif os.path.isdir(caminho_item):
                shutil.rmtree(caminho_item)
            atualizar_lista_arquivos()
            messagebox.showinfo("Sucesso", f"'{nome_item}' apagado.", parent=janela)
        except Exception as e:
            messagebox.showerror("Erro ao Apagar", f"Não foi possível apagar '{nome_item}': {e}", parent=janela)

def renomear_item():
    if not tree.selection():
        messagebox.showwarning("Aviso", "Nenhum item selecionado.", parent=janela)
        return

    item_id = tree.selection()[0]
    nome_antigo = tree.item(item_id, "text")
    item_values = tree.item(item_id, "values")

    if not item_values and nome_antigo == "..":
        messagebox.showwarning("Aviso", "Não é possível renomear o item de navegação '..'.", parent=janela)
        return
    elif not item_values:
        messagebox.showerror("Erro", "Item selecionado inválido para renomear.", parent=janela)
        return

    caminho_antigo = item_values[0]

    novo_nome = simpledialog.askstring("Renomear", f"Novo nome para '{nome_antigo}':", initialvalue=nome_antigo, parent=janela)
    if novo_nome and novo_nome != nome_antigo:
        if os.path.sep in novo_nome or any(c in novo_nome for c in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']):
            messagebox.showerror("Nome Inválido", "O novo nome contém caracteres inválidos.", parent=janela)
            return
        caminho_novo = os.path.join(diretorio_atual.get(), novo_nome) # O novo nome é relativo ao diretório atual
        try:
            os.rename(caminho_antigo, caminho_novo)
            atualizar_lista_arquivos()
            messagebox.showinfo("Sucesso", f"'{nome_antigo}' renomeado para '{novo_nome}'.", parent=janela)
        except Exception as e:
            messagebox.showerror("Erro ao Renomear", f"Não foi possível renomear: {e}", parent=janela)

def mover_item():
    if not tree.selection():
        messagebox.showwarning("Aviso", "Nenhum item selecionado.", parent=janela)
        return

    item_id = tree.selection()[0]
    nome_item = tree.item(item_id, "text")
    item_values = tree.item(item_id, "values")

    if not item_values and nome_item == "..":
        messagebox.showwarning("Aviso", "Não é possível mover o item de navegação '..'.", parent=janela)
        return
    elif not item_values:
        messagebox.showerror("Erro", "Item selecionado inválido para mover.", parent=janela)
        return
        
    caminho_origem = item_values[0]

    novo_diretorio = filedialog.askdirectory(title=f"Mover '{nome_item}' para:", initialdir=diretorio_atual.get(), parent=janela)
    if novo_diretorio:
        caminho_destino = os.path.join(novo_diretorio, nome_item) # Nome do item é mantido no novo diretório
        if os.path.abspath(caminho_origem) == os.path.abspath(caminho_destino):
            messagebox.showinfo("Info", "O local de origem e destino são os mesmos.", parent=janela)
            return
        if os.path.exists(caminho_destino):
            confirmar_subs = messagebox.askyesno("Confirmar Substituição",
                                                 f"O item '{nome_item}' já existe em '{novo_diretorio}'. Deseja substituí-lo?",
                                                 icon='warning', parent=janela)
            if not confirmar_subs:
                messagebox.showinfo("Movimentação Cancelada", "A operação foi cancelada.", parent=janela)
                return
        try:
            shutil.move(caminho_origem, caminho_destino)
            atualizar_lista_arquivos()
            messagebox.showinfo("Sucesso", f"'{nome_item}' movido para '{novo_diretorio}'.", parent=janela)
        except Exception as e:
            messagebox.showerror("Erro ao Mover", f"Não foi possível mover '{nome_item}': {e}", parent=janela)

# --- Widgets da Interface do Gerenciador de Arquivos ---
frame_navegacao = tk.Frame(janela, bg=cor_azul_escuro)
frame_navegacao.place(relx=0.05, rely=0.18, relwidth=0.9, height=40)

btn_voltar = tk.Button(frame_navegacao, text="↑ Voltar", command=voltar_diretorio,
                       font=fonte_botao_acao_str, fg=cor_botao_navegacao_fg_text, bg=cor_botao_navegacao_bg,
                       relief=tk.FLAT, activebackground=cor_azul_claro, activeforeground="white")
btn_voltar.pack(side=tk.LEFT, padx=5, pady=5)

path_entry = tk.Entry(frame_navegacao, textvariable=diretorio_atual, font=fonte_path_entry_str, bd=2, relief=tk.SUNKEN)
path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
path_entry.bind("<Return>", navegar_pelo_entry)

btn_ir = tk.Button(frame_navegacao, text="Ir", command=navegar_pelo_entry,
                   font=fonte_botao_acao_str, fg=cor_botao_navegacao_fg_text, bg=cor_botao_navegacao_bg,
                   relief=tk.FLAT, activebackground=cor_azul_claro, activeforeground="white")
btn_ir.pack(side=tk.LEFT, padx=5, pady=5)

style = ttk.Style()
style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=fonte_treeview_str, rowheight=25)
style.configure("mystyle.Treeview.Heading", font=(fonte_treeview_str[0], int(fonte_treeview_str[1]), "bold")) # Fonte da treeview heading
style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

tree_frame = tk.Frame(janela)
tree_frame.place(relx=0.05, rely=0.26, relwidth=0.9, relheight=0.55)

tree = ttk.Treeview(tree_frame, columns=("path", "type"), displaycolumns=(), style="mystyle.Treeview")
tree.heading("#0", text="Nome", anchor='w') # Alinhar texto do cabeçalho à esquerda
tree.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=scrollbar.set)

tree.bind("<Double-1>", on_item_double_click)

frame_botoes_acao = tk.Frame(janela, bg=cor_azul_escuro)
frame_botoes_acao.place(relx=0.05, rely=0.83, relwidth=0.9, height=80)

botoes_info = [
    ("Criar Arquivo", criar_arquivo),
    ("Criar Pasta", criar_pasta),
    ("Apagar", apagar_item),
    ("Renomear", renomear_item),
    ("Mover", mover_item)
]

for i, (texto, comando) in enumerate(botoes_info):
    btn = tk.Button(frame_botoes_acao, text=texto, command=comando,
                    font=fonte_botao_acao_str, fg=cor_botao_acao_fg_text, bg=cor_botao_acao_bg,
                    relief=tk.FLAT, activebackground="#E0E0E0", activeforeground=cor_botao_acao_fg_text,
                    width=12, height=2)
    btn.pack(side=tk.LEFT, expand=True, padx=5, pady=10)

# --- Inicialização ---
janela.update_idletasks() # Garante que as dimensões da janela estão prontas
desenhar_gradiente() # Desenha o gradiente e o título
canvas_fundo.bind("<Configure>", desenhar_gradiente) # Bind para caso a janela fosse redimensionável
atualizar_lista_arquivos()

# Adiciona o protocolo para fechar a janela via 'X' e chamar a função de ir para inicio
# Isso pode ser um comportamento desejado ou não, dependendo do fluxo.
# Se o desejo é que o 'X' apenas feche o gerenciador, remova esta linha.
# Se o 'X' deve levar ao início, esta linha é útil.
# janela.protocol("WM_DELETE_WINDOW", ir_para_script_inicio)


janela.mainloop()