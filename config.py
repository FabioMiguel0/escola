# Configurações do Sistema Escolar

# Configurações do Banco de Dados
DB_NAME = "sistema_escolar.db"

# Configurações da Interface
APP_TITLE = "EduGestão"
APP_VERSION = "1.0.0"

# Configurações de Tema
THEME_COLORS = {
    "primary": "#1976D2",
    "secondary": "#424242",
    "background": "#F5F5F5",
    "surface": "#FFFFFF",
    "error": "#D32F2F",
    "success": "#388E3C",
    "warning": "#F57C00",
    "info": "#1976D2"
}

# Configurações de Usuários
DEFAULT_USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "secretaria": {"password": "sec123", "role": "secretaria"},
    "prof": {"password": "prof123", "role": "professor"},
    "aluno": {"password": "aluno123", "role": "aluno"},
    "responsavel": {"password": "resp123", "role": "responsavel"},
    "suporte": {"password": "sup123", "role": "suporte"}
}

# Configurações de Validação
VALIDATION_RULES = {
    "nome_min_length": 2,
    "nome_max_length": 100,
    "email_pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    "matricula_pattern": r"^[A-Z]\d{3}$",
    "telefone_pattern": r"^\(\d{2}\) \d{4,5}-\d{4}$"
}

# Configurações de Paginação
PAGINATION = {
    "items_per_page": 10,
    "max_pages_display": 5
}

# Configurações de Log
LOG_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "sistema_escolar.log"
}
