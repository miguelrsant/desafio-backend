# API para gerenciamento de tarefas (To-Do)

API REST para gerenciamento de tarefas desenvolvida como solução para um desafio técnico utilizando **Python**, **Django REST Framework**, **PostgreSQL** e **Docker**.

O projeto implementa todos os requisitos obrigatórios descritos no desafio técnico e também contempla os diferenciais sugeridos, além de algumas melhorias voltadas à organização do código, qualidade da aplicação e experiência de desenvolvimento.

---

## Sumário

- [Tecnologias](#tecnologias)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Decisões de arquitetura](#decisões-de-arquitetura)
- [Como executar o projeto](#como-executar-o-projeto)
  - [Pré-requisitos](#pré-requisitos)
  - [Instalação](#instalação)

- [Endpoints da API](#endpoints-da-api)
  - [Autenticação](#autenticação)
    - [Criar usuário](#criar-usuário)
    - [Login](#login)

  - [Tarefas](#tarefas)
    - [Listar tarefas](#listar-tarefas)
    - [Criar tarefa](#criar-tarefa)
    - [Atualizar tarefa](#atualizar-tarefa)
    - [Excluir tarefa](#excluir-tarefa)

- [Executando os testes](#executando-os-testes)
- [Diferenciais implementados](#diferenciais-implementados)

# Tecnologias

- Python
- Django
- Django REST Framework
- PostgreSQL
- Docker
- Docker Compose
- JWT (Simple JWT)
- Pytest
- Pytest-Django
- Pytest-Cov
- Ruff
- Black

---

# Estrutura do projeto

```text
config/      Configurações do projeto Django
users/       Autenticação, gerenciamento de usuários e testes das usuários
tasks/       CRUD, filtros, regras de negócio e testes das tarefas
```

---

# Decisões de arquitetura

Algumas decisões foram tomadas para manter o projeto organizado e de fácil manutenção.

- Separação da aplicação por domínio (`users` e `tasks`);
- Validações centralizadas nos Serializers;
- Soft Delete para preservar o histórico das tarefas;
- Autenticação utilizando JWT;
- Isolamento das tarefas por usuário autenticado;
- Organização dos filtros em um módulo específico;
- Testes automatizados cobrindo os principais fluxos da aplicação.

---

# Como executar o projeto

## Pré-requisitos

Antes de iniciar, é necessário possuir instalado:

- Python 3.12 ou superior;
- Docker e Docker Compose.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/miguelrsant/desafio-backend
cd desafio-backend
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

O projeto possui um arquivo `.env` versionado apenas como **exemplo**, contendo a configuração utilizada durante o desenvolvimento.

Inicie o banco de dados:

```bash
docker compose up -d
```

Execute as migrações:

```bash
python manage.py migrate
```

Inicie a aplicação:

```bash
python manage.py runserver
```

A API estará disponível em:

```text
http://localhost:8000
```

## Endpoints da API

### Autenticação

#### Criar usuário

```http
POST /users/register
```

Cria um novo usuário.

**Exemplo de requisição**

```json
{
  "username": "usuario",
  "password": "12345678"
}
```

---

#### Login

```http
POST /users/login
```

Autentica um usuário e retorna um token JWT.

**Exemplo de requisição**

```json
{
  "username": "usuario",
  "password": "12345678"
}
```

---

### Tarefas

> Todos os endpoints abaixo exigem autenticação via JWT.

#### Listar tarefas

```http
GET /tasks
```

Filtros disponíveis:

| Parâmetro | Descrição                                              |
| --------- | ------------------------------------------------------ |
| `title`   | Filtra tarefas pelo título.                            |
| `status`  | Filtra tarefas pelo status (`PENDING` ou `COMPLETED`). |

Exemplo:

```http
GET /tasks?title=Estudar&status=PENDING
```

---

#### Criar tarefa

```http
POST /tasks
```

**Exemplo de requisição**

```json
{
  "title": "Django",
  "description": "Finalizar desafio técnico",
  "status": "PENDING"
}
```

---

#### Atualizar tarefa

```http
PUT /tasks/{id}
```

Atualiza uma tarefa existente.

**Exemplo de requisição**

```json
{
  "title": "Django REST",
  "description": "Finalizar desafio técnico",
  "status": "COMPLETED"
}
```

---

#### Excluir tarefa

```http
DELETE /tasks/{id}
```

Realiza a exclusão lógica (Soft Delete) da tarefa. Ela deixa de ser retornada pela API, mas permanece armazenada no banco de dados para preservação do histórico.

---

# Executando os testes

Executar todos os testes:

```bash
pytest
```

Executar os testes com relatório de cobertura:

```bash
pytest --cov=. --cov-report=term-missing
```

---

# Diferenciais implementados

Além dos requisitos obrigatórios, foram implementadas funcionalidades e melhorias para tornar a aplicação mais organizada, segura e próxima de um ambiente de desenvolvimento real.

- Autenticação utilizando JWT;
- Testes automatizados com Pytest;
- Cobertura de testes com `pytest-cov`;
- Filtros por título e status;
- Exclusão lógica (Soft Delete);
- Isolamento de tarefas por usuário autenticado;
- Padronização das respostas da API;
- Organização do projeto por domínio (`users` e `tasks`);
- Código formatado utilizando Black;
- Análise estática de código com Ruff;
- Banco de dados executado através do Docker Compose.
