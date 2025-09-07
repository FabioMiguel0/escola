# Sistema Escolar

Este projeto é um sistema escolar desenvolvido em Python utilizando a biblioteca Flet. O sistema permite a gestão de usuários, incluindo administradores, secretários, professores e alunos, com funcionalidades específicas para cada papel.

## Estrutura do Projeto

- **main.py**: Ponto de entrada da aplicação. Inicializa o aplicativo Flet, configura a página principal e gerencia a autenticação de usuários e o roteamento com base nos papéis dos usuários.
  
- **services/**: Contém serviços relacionados ao banco de dados e gerenciamento de usuários.
  - **db.py**: Funções para operações de banco de dados, incluindo criação de tabelas e inserção de dados iniciais.
  - **seed.py**: Responsável por popular o banco de dados com dados iniciais.
  - **user_service.py**: Funções relacionadas à gestão de usuários, incluindo autenticação e controle de acesso baseado em papéis.

- **UI/**: Contém as interfaces de usuário.
  - **login_view.py**: Interface de login para autenticação de usuários.
  - **shell.py**: Define a estrutura do shell da aplicação, incluindo navegação e layout.

- **view/**: Contém as diferentes visualizações da aplicação.
  - **dashboard_view.py**: Visualização do painel da aplicação.
  - **aluno_view.py**: Funcionalidades relacionadas aos alunos.
  - **professor_view.py**: Funcionalidades relacionadas aos professores.
  - **comunicado_view.py**: Visualização para anúncios.
  - **turma_view.py**: Funcionalidades relacionadas às turmas.
  - **disciplina_view.py**: Funcionalidades relacionadas às disciplinas.
  - **frequencia_view.py**: Funcionalidades relacionadas à frequência.
  - **nota_view.py**: Funcionalidades relacionadas às notas.
  - **documento_view.py**: Funcionalidades relacionadas a documentos.
  - **calendario_view.py**: Funcionalidades relacionadas ao calendário.
  - **users_view.py**: Funcionalidades para gerenciamento de usuários.
  - **student/**: Pacote para funcionalidades relacionadas aos alunos.
    - **grades_view.py**: Visualização para os alunos verem suas notas.
    - **subjects_view.py**: Visualização para os alunos verem suas disciplinas.
    - **performance_view.py**: Visualização para os alunos verem seu desempenho.
    - **report_card_view.py**: Visualização para os alunos verem seu boletim.
  - **teacher/**: Pacote para funcionalidades relacionadas aos professores.
    - **classes_view.py**: Visualização para os professores verem suas turmas.
    - **schedule_view.py**: Visualização para os professores verem seu horário.
    - **subjects_taught_view.py**: Visualização para os professores verem as disciplinas que irão lecionar.

- **models/**: Contém os modelos de dados utilizados na aplicação.
  - **models.py**: Modelos de dados.

- **requirements.txt**: Lista de dependências necessárias para o projeto.

## Como Executar

1. Clone o repositório.
2. Instale as dependências listadas em `requirements.txt`.
3. Execute o arquivo `main.py` para iniciar a aplicação.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.