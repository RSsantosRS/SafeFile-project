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
