from dataclasses import dataclass
from typing import Optional

@dataclass
class Aluno:
    """Modelo mínimo de Aluno usado pelo restante do projeto."""
    id: Optional[int] = None
    nome: str = ""
    matricula: Optional[str] = None
    turma_id: Optional[int] = None

