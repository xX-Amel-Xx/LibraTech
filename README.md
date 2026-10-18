# LibraTech — Sistema de Gerenciamento de Biblioteca

O LibraTech é uma aplicação web desenvolvida para facilitar o gerenciamento de uma biblioteca, permitindo organizar livros, gerenciar empréstimos e devoluções e consultar o histórico de movimentações.

O projeto foi desenvolvido como prática de programação web, integração com banco de dados e criação de interfaces utilizando Python, Flask, HTML e CSS.

## Funcionalidades

- Cadastro e gerenciamento de livros.
- Registro de empréstimos.
- Registro de devoluções.
- Consulta de livros disponíveis.
- Histórico de empréstimos.
- Validações para evitar operações incompatíveis com os relacionamentos entre os registros.
- Interface personalizada com páginas específicas para as funcionalidades do sistema.

## Tecnologias utilizadas

- **Python:** lógica da aplicação.
- **Flask:** desenvolvimento web e gerenciamento de rotas.
- **Flask-SQLAlchemy:** integração entre a aplicação e o banco de dados.
- **SQLite:** armazenamento de dados.
- **HTML5:** estrutura das páginas.
- **CSS3:** estilização e identidade visual.
- **Git e GitHub:** versionamento e hospedagem do código-fonte.

## Estrutura do projeto

```text
LibraTech/
├── static/
│   ├── css/
│   └── img/
├── templates/
├── app.py
├── models.py
├── .gitignore
└── README.md
```

A estrutura representa os principais arquivos e diretórios do projeto. Os subdiretórios de `static/` podem variar conforme a organização dos arquivos.

## Como executar o projeto

### 1. Clone o repositório

```bash
git clone <URL_DO_REPOSITORIO>
```

### 2. Acesse a pasta do projeto

```bash
cd LibraTech
```

### 3. Crie um ambiente virtual

```bash
python -m venv venv
```

### 4. Ative o ambiente virtual

No Windows:

```bash
venv\Scripts\activate
```

### 5. Instale as dependências

Caso o projeto tenha um arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

Se ainda não tiver esse arquivo, instale as dependências utilizadas pela aplicação, como Flask e Flask-SQLAlchemy.

### 6. Execute a aplicação

```bash
python app.py
```

Depois, acesse o endereço local indicado no terminal, normalmente `http://127.0.0.1:5000`.

A configuração do banco de dados e a criação das tabelas devem seguir o que está definido nos arquivos da aplicação.

## Objetivo do projeto

O LibraTech foi desenvolvido para colocar em prática conhecimentos de desenvolvimento web, organização de código, manipulação de dados, integração com banco de dados e construção de interfaces.

O projeto também contribui para o desenvolvimento de habilidades de resolução de problemas, validação de operações e manutenção de aplicações.

## Principais Telas do Projeto

### Tela inicial

![Tela Inicial](Docs/Tela%20inicial.png)

### Tela de empréstimos

![Tela de empréstimos](Docs/Tela%20emprestimos.png)

### Tela de histórico

![Tela de histórico de empréstimos](Docs/Tela%20hist%C3%B3rico.png)
## Autora

**Amanda Meireles**

Projeto desenvolvido para fins de aprendizado e construção de portfólio.