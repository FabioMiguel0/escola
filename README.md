# Sistema Escolar

Sistema de gestão escolar desenvolvido com Flet (Python).

## Funcionalidades

- Gestão de alunos, professores e turmas
- Dashboard com estatísticas (apenas para administradores)
- Sistema de login com diferentes roles
- Interface responsiva para mobile, tablet e desktop

## Roles de Usuário

- **Admin**: Acesso completo ao sistema
- **Secretaria**: Gestão de alunos e turmas
- **Professor**: Acesso às suas turmas e notas
- **Aluno**: Visualização do próprio perfil

## Deploy no Render

1. Faça upload do código para um repositório Git (GitHub, GitLab, etc.)
2. No Render, crie um novo Web Service
3. Conecte o repositório
4. Use as configurações:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Environment**: Python 3

## Desenvolvimento Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar localmente
python main.py
```

## Credenciais de Teste

- **Admin**: usuário: `admin`, senha: qualquer
- **Professor**: usuário: `professor`, senha: qualquer  
- **Aluno**: usuário: `aluno`, senha: qualquer