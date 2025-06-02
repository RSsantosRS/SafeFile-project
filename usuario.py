from dataclasses import dataclass

@dataclass
class Usuario:
    cpf: str
    senha: str
    nome: str
    email: str