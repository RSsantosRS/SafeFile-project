from datetime import datetime
from banco_documento import BancoDocumento
from documento import Documento

if __name__ == "__main__":
    # Instancia o banco e conecta
    banco = BancoDocumento()
    banco.conectar()                                                                                                                                    
    banco.criar_tabela_documento()
    banco.criar_tabela_usuario()
    banco.fechar_conexao() 