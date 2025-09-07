# Models package
# Exporta classes de modelos de forma segura para evitar ImportError
__all__ = []

try:
    from .aluno import Aluno
    __all__.append("Aluno")
except Exception:
    # evita quebrar toda a importação do pacote se houver dependências circulares
    pass

try:
    from .professor import Professor
    __all__.append("Professor")
except Exception:
    pass

try:
    from .turma import Turma
    __all__.append("Turma")
except Exception:
    pass

try:
    from .disciplina import Disciplina
    __all__.append("Disciplina")
except Exception:
    pass

try:
    from .nota import Nota
    __all__.append("Nota")
except Exception:
    pass

try:
    from .frequencia import Frequencia
    __all__.append("Frequencia")
except Exception:
    pass

try:
    from .comunicado import Comunicado
    __all__.append("Comunicado")
except Exception:
    pass

try:
    from .calendario import Calendario
    __all__.append("Calendario")
except Exception:
    pass

try:
    from .documento import Documento
    __all__.append("Documento")
except Exception:
    pass
