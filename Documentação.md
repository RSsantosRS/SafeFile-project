# SafeFile-project
projeto acadêmico de um gerenciador de arquivos para a matéria de programação rápida em python, na universidade Estácio de sá.
## Gerenciador de Arquivos Pessoais e controlador de arquivos do Sistema
## Introdução
Este documento detalha o funcionamento de um sistema gerenciador de arquivos desenvolvido em Python. A aplicação oferece funcionalidades completas de CRUD (Criar, Ler, Atualizar, Deletar) tanto para arquivos pessoais quanto para arquivos do sistema, proporcionando uma interface intuitiva para a organização e manipulação de dados. Através de uma combinação de bibliotecas robustas, o sistema visa otimizar a gestão de arquivos, tornando o processo mais eficiente e seguro.

## Funcionalidades Principais
### Gerenciamento de Arquivos Pessoais:
Criação, leitura, atualização e exclusão de arquivos e pastas.
Organização personalizada de diretórios.
Visualização e acesso facilitado a documentos, imagens, vídeos, etc.
###Gerenciamento de Arquivos do Sistema:
Navegação e manipulação segura de arquivos e diretórios do sistema operacional.
Ferramentas para operações sensíveis, como exclusão ou modificação de arquivos de sistema (com as devidas precauções).
### Operações CRUD Abrangentes:
  Interface para criar novos arquivos e pastas.
Visualização detalhada do conteúdo de arquivos.
Edição e atualização de metadados ou conteúdo de arquivos.
Exclusão segura de arquivos e pastas.
### Segurança de Dados:
  Utilização de hashing para integridade e segurança de informações críticas.
### Interface Gráfica Amigável:
  Desenvolvida com Tkinter para uma experiência de usuário intuitiva e fácil navegação.
Bibliotecas Utilizadas
O sistema foi desenvolvido utilizando as seguintes bibliotecas Python:

## tkinter:
  Biblioteca padrão de Python para a criação de interfaces gráficas de usuário (GUIs). É utilizada para construir todos os elementos visuais do gerenciador de arquivos, como janelas, botões, campos de texto e listas, proporcionando a interação do usuário com a aplicação.
## subprocess:
  Permite a criação e gerenciamento de novos processos. É útil para executar comandos do sistema operacional diretamente do código Python, possibilitando a interação com programas externos ou a execução de comandos de shell para manipulação de arquivos em um nível mais baixo.
## sys:
  Fornece acesso a variáveis e funções que interagem fortemente com o interpretador Python. É frequentemente utilizada para manipular caminhos de módulos, argumentos de linha de comando e para interagir com o ambiente de execução do script.
## os:
  Oferece uma maneira portátil de interagir com o sistema operacional. É fundamental para operações de gerenciamento de arquivos e diretórios, como listar conteúdos de pastas, criar e remover diretórios, renomear arquivos e verificar a existência de caminhos.
## sqlite3:
  Módulo para trabalhar com o banco de dados SQLite. É empregado para armazenar informações estruturadas, como metadados de arquivos, configurações do usuário ou registros de operações, permitindo um gerenciamento eficiente e persistente de dados.
## hashlib:
  Módulo que implementa uma interface comum para muitos algoritmos de hash seguro e hash de mensagem. É utilizado para gerar hashes de arquivos ou dados, garantindo a integridade dos dados e, em alguns casos, para fins de segurança, como verificação de senhas ou integridade de downloads.
# Páginas do Código
app_documento.log
Este arquivo é um log de informações geradas pela aplicação. Ele registra eventos importantes, como a criação de tabelas no banco de dados. Por exemplo, há um registro indicando que a tabela Documento foi criada com sucesso.

# Arquivos e logs

## Banco_documento.py
Este módulo é responsável por toda a interação com o banco de dados SQLite, gerenciando tanto os documentos quanto os usuários.

Configuração de Log: Configura o sistema de log para registrar informações e erros em app_documento.log.
BancoDocumento Classe:
Inicialização (__init__): Define o nome do arquivo do banco de dados (banco_documento.sqlite) e inicializa a conexão como None.
conectar(): Estabelece a conexão com o banco de dados SQLite.
criar_tabela_documento(): Cria a tabela Documento se ela não existir, com colunas para nome do arquivo, caminho, tipo, data de criação e tamanho em MB. Registra no log que a tabela foi criada com sucesso.
criar_tabela_usuario(): Cria a tabela Usuario se ela não existir, com colunas para CPF (chave primária), senha (hashed), nome e email. Registra no log que a tabela foi criada com sucesso.
inserir_usuario(usuario: Usuario): Insere um novo usuário na tabela Usuario, fazendo o hash da senha antes de armazená-la. Registra no log o sucesso ou erro da inserção, incluindo casos de CPF duplicado.
verificar_login(email: str, senha: str): Busca um usuário pelo email e retorna o nome e a senha (hashed) para verificação.
atualizar_documento(documento: Documento): Atualiza os dados de um documento existente na tabela Documento com base no nome_arquivo.
apagar_documento(nome_arquivo: str): Remove um documento da tabela Documento usando o nome_arquivo como critério.
buscar_todos_documentos(): Retorna uma lista de todos os documentos registrados no banco de dados.
buscar_documento_por_nome(nome_arquivo: str): Busca e retorna um objeto Documento específico com base no nome_arquivo.
fechar_conexao(): Encerra a conexão com o banco de dados.
## Cadastro.py
Este script gerencia a interface gráfica e a lógica para o cadastro de novos usuários no sistema SafeFile.

Constantes: Define textos de placeholder e cores para o campo de CPF.
Funções de Navegação:
ir_para_inicio_da_tela_cadastro(): Redireciona o usuário para a tela inicial (inicio.py) após o cadastro, destruindo a janela de cadastro atual.
Lógica do Banco de Dados:
cadastrar_usuario(nome, email, senha, cpf): Utiliza a classe BancoDocumento para conectar ao banco e inserir um novo usuário, tratando possíveis erros como CPF duplicado.
gerar_hash_senha(senha): Gera um hash SHA-256 da senha fornecida para armazenamento seguro.
Lógica do Cadastro:
processar_cadastro(): Coleta os dados dos campos de entrada, valida-os (como verificar se o CPF contém apenas números), gera o hash da senha e tenta cadastrar o usuário no banco de dados. Em caso de sucesso, redireciona para a tela de login.
Placeholder do CPF:
on_cpf_focus_in(event) e on_cpf_focus_out(event): Implementam a funcionalidade de placeholder para o campo CPF, removendo o texto padrão quando o campo é focado e inserindo-o de volta se o campo ficar vazio.
Janela Principal (tk.Tk()):
Configura a janela de cadastro, definindo título, dimensões e a impossibilidade de redimensionamento.
Define paleta de cores e fontes para diversos elementos da interface.
canvas_fundo: Cria um canvas para desenhar um gradiente de fundo que se ajusta ao tamanho da janela.
desenhar_titulo() e desenhar_gradiente(event=None): Funções para desenhar o título "SafeFile" e o gradiente de cor no canvas.
adicionar_label_entry(texto, y_label, y_entry): Função auxiliar para criar e posicionar labels e campos de entrada.
Cria os campos de entrada para Nome Completo, Email, Senha (ocultando caracteres) e CPF (com placeholder).
Botões: Adiciona botões "Cadastrar" e "Voltar", configurando suas aparências e comandos associados.
Loop Principal: Inicia o loop principal do Tkinter para exibir a janela.
## Documento.py
Este módulo define a estrutura de dados para um documento no sistema SafeFile.

Documento Classe: Uma dataclass que encapsula os atributos de um documento, incluindo:
nome_arquivo (str): O nome do arquivo.
caminho (str): O caminho completo do arquivo no sistema de arquivos.
tipo_arquivo (str): O tipo ou extensão do arquivo.
data_criacao (datetime): A data e hora de criação do documento.
tamanho_mb (float): O tamanho do arquivo em megabytes.
gerar_tabela.py
Este script é responsável por inicializar o banco de dados e criar a tabela Documento.

Execução Principal (if __name__ == "__main__":):
Cria uma instância de BancoDocumento.
Conecta ao banco de dados.
Chama o método criar_tabela_documento() para garantir que a tabela Documento exista.
Fecha a conexão com o banco de dados.
É um script utilitário para setup inicial do banco de dados.
## Gerenciador.py
Este script implementa a interface gráfica principal do gerenciador de arquivos, permitindo ao usuário navegar, criar, apagar, renomear e mover arquivos e pastas.

Configurações da Janela Principal: Define o título da janela, dimensões fixas e outras configurações básicas do Tkinter.
Cores e Fontes: Estabelece um esquema de cores e estilos de fonte para uma interface consistente.
Variável Global: diretorio_atual (StringVar) mantém o caminho do diretório que está sendo exibido no momento.
Canvas para o Gradiente de Fundo:
canvas_fundo: Cria um canvas para o fundo da janela.
desenhar_titulo_no_canvas(): Desenha o título "SafeFile" no canvas.
desenhar_gradiente(event=None): Função para criar um efeito de gradiente de cor no fundo da janela, ajustando-se ao tamanho do canvas.
Funções de Navegação:
ir_para_script_inicio(): Redireciona o usuário para a tela inicial (inicio.py), fechando a janela atual.
Botão "Voltar ao Início": Um botão posicionado no canto superior direito para fácil retorno à tela inicial.
Funções de Gerenciamento de Arquivos:
atualizar_lista_arquivos(): Limpa e preenche o Treeview com os conteúdos do diretorio_atual, incluindo arquivos e pastas. Trata erros de acesso e caminhos inválidos.
on_item_double_click(event): Lida com o duplo clique em itens da lista: se for uma pasta, navega para ela; se for um arquivo, tenta abri-lo com o programa padrão do sistema operacional.
navegar_pelo_entry(event=None): Permite ao usuário digitar um caminho diretamente na caixa de texto e navegar para ele.
voltar_diretorio(): Navega para o diretório pai do diretorio_atual.
criar_arquivo(): Solicita um nome de arquivo ao usuário e tenta criar um arquivo vazio no diretorio_atual.
criar_pasta(): Solicita um nome de pasta ao usuário e tenta criar uma nova pasta no diretorio_atual.
apagar_item(): Exclui o arquivo ou pasta selecionado após confirmação do usuário.
renomear_item(): Solicita um novo nome para o item selecionado e o renomeia.
mover_item(): Abre uma caixa de diálogo para que o usuário selecione um novo diretório e move o item selecionado para lá.
Widgets da Interface:
frame_navegacao: Contém o botão "Voltar", o campo de entrada para o caminho e o botão "Ir".
Treeview (tree): O widget principal que exibe a lista de arquivos e pastas. Utiliza um estilo personalizado.
scrollbar: Barra de rolagem para o Treeview.
frame_botoes_acao: Contém os botões para as operações de CRUD (Criar Arquivo, Criar Pasta, Apagar, Renomear, Mover).
Inicialização: Chama funções para desenhar o gradiente e atualizar a lista de arquivos na inicialização da janela.
Loop Principal: Inicia o loop principal do Tkinter.
## Inicio.py
Este script é a tela de menu principal do aplicativo SafeFile, oferecendo opções para login e cadastro.

## Funções de Navegação:
ir_para_inicio(): Redireciona para a própria tela de início (recarrega).
ir_para_login(): Fecha a janela atual e abre o script login.py.
ir_para_cadastro(): Fecha a janela atual e abre o script cadastro.py.
Configurações da Janela Principal:
Define o título ("SafeFile - Menu Principal"), dimensões fixas (800x600) e desativa o redimensionamento.
Cores e Fontes: Define um conjunto de cores e estilos de fonte para os elementos da interface, como título e botões.
Canvas para o Gradiente de Fundo:
canvas_fundo: Um widget Canvas que ocupa toda a janela para desenhar o gradiente de fundo.
desenhar_titulo_no_canvas(): Desenha o texto "SafeFile" com a fonte e cor definidas no canvas.
desenhar_gradiente(event=None): Esta função é responsável por criar o efeito de gradiente horizontal no fundo da janela, desenhando linhas finas com cores interpoladas. É chamada na inicialização e também quando a janela é redimensionada (embora a janela seja fixa, o bind está presente).
## Botões:
"Login": Botão principal para acessar a tela de login.
"Primeira vez? Cadastre-se": Botão secundário para navegar até a tela de cadastro.
"Voltar para o Início": Botão secundário que, neste contexto, recarrega a própria tela inicial.
Os botões são estilizados com cores e fontes específicas e posicionados centralizadamente na tela.
Loop Principal: janela.mainloop() inicia o loop de eventos do Tkinter, mantendo a janela aberta e responsiva às interações do usuário.
## Login.py
Este script é responsável pela interface e lógica de autenticação de usuários no sistema SafeFile.

Função de Hashing de Senha:
gerar_hash_senha(senha): Utiliza hashlib.sha256 para criar um hash seguro da senha fornecida, garantindo que as senhas não sejam armazenadas em texto simples.
Função de Processamento de Login:
processar_login():
Obtém o email e a senha digitados pelo usuário.
Verifica se os campos estão preenchidos.
Conecta ao banco de dados usando BancoDocumento.
Chama banco.verificar_login(email, senha) para buscar o usuário e a senha hashed no banco.
Compara a senha digitada (após hashing) com a senha armazenada no banco.
Em caso de login bem-sucedido, exibe uma mensagem de boas-vindas e tenta abrir o script gerenciador.py, fechando a janela de login.
Em caso de falha (senha incorreta, email não encontrado, erros de banco de dados), exibe mensagens de erro apropriadas.
## Funções de Navegação:
ir_para_cadastro_desta_tela(): Fecha a janela de login e abre a tela de cadastro (cadastro.py).
ir_para_inicio_da_tela_login(): Fecha a janela de login e abre a tela inicial (inicio.py).
Configurações da Janela Principal (janela_login):
Define o título da janela ("SafeFile - Login"), suas dimensões fixas (800x600) e desabilita o redimensionamento.
Cores e Fontes: Define um conjunto de cores e estilos de fonte para os elementos visuais, como título, labels, campos de entrada e botões.
Canvas para o Gradiente de Fundo:
canvas_fundo: Um widget Canvas que ocupa toda a janela para desenhar o gradiente de fundo.
desenhar_titulo_no_canvas(): Desenha o texto "SafeFile" no canvas.
desenhar_gradiente(event=None): Responsável por criar o efeito de gradiente de cor no fundo da janela, garantindo que ele seja desenhado corretamente na inicialização.
Campos de Login:
Labels e Entry widgets para "Email" e "Senha". O campo de senha oculta os caracteres digitados (show="*").
Os campos são posicionados centralizadamente com largura e altura definidas.
## Botões:
"Login": Botão principal que aciona a função processar_login.
"Primeira vez? Cadastre-se": Botão que redireciona para a tela de cadastro.
"Voltar para o Início": Botão que redireciona para a tela inicial.
Todos os botões são estilizados com cores, fontes e efeitos de hover.
Loop Principal: janela_login.mainloop() inicia o loop de eventos do Tkinter.
README.md
Este é o arquivo README do projeto, que fornece uma breve descrição do SafeFile.

## Descrição: Indica que o SafeFile é um "projeto acadêmico de um gerenciador de arquivos para a matéria de programação rápida em python, na universidade Estácio de Sá".
## Usuario.py
Este módulo define a estrutura de dados para um usuário no sistema SafeFile.

Usuario Classe: Uma dataclass que encapsula os atributos de um usuário, incluindo:
cpf (str): O Cadastro de Pessoa Física do usuário.
senha (str): A senha do usuário (será armazenada como hash).
nome (str): O nome completo do usuário.
email (str): O endereço de email do usuário.
