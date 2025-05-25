from dataclasses import dataclass
from datetime import datetime

@dataclass
class Documento:
    nome_arquivo: str
    caminho: str
    tipo_arquivo: str
    data_criacao: datetime
    tamanho_mb: float