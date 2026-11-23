# APS 3 – API de Eventos Acadêmicos

Continuação da APS 2. A API foi atualizada para persistir eventos, participantes e inscrições em banco SQLite, utilizando SQLAlchemy ORM, FastAPI, Pydantic e arquitetura MVC.

## 1. Funcionalidades

- CRUD completo de eventos e participantes.
- Inscrição de participantes em eventos e consulta dos inscritos.
- Persistência dos dados em SQLite, inclusive após reiniciar a aplicação.
- Validação com Pydantic.
- Integridade referencial, e-mail único e bloqueio de inscrição duplicada.
- Controle de capacidade e tratamento de erros HTTP.
- Relatórios de ocupação, eventos por categoria e participação por curso.

## 2. Tecnologias

Python 3.10 ou superior, FastAPI, SQLite, SQLAlchemy ORM 2.x, Pydantic 2 e Uvicorn.

## 3. Estrutura do projeto

```text
APS3_API_Eventos/
├── main.py
├── database.py
├── requirements.txt
├── README.md
├── eventos_academicos.db   # criado automaticamente ao executar
├── controller/
│   ├── evento_controller.py
│   ├── participante_controller.py
│   └── relatorio_controller.py
├── model/
│   ├── evento.py
│   ├── participante.py
│   └── inscricao.py
├── schema/
│   ├── evento_schema.py
│   ├── participante_schema.py
│   └── inscricao_schema.py
└── service/
    ├── evento_service.py
    ├── participante_service.py
    └── relatorio_service.py
```

## 4. Banco de dados e relacionamentos

O arquivo `database.py` configura a conexão com `sqlite:///./eventos_academicos.db`, cria a fábrica de sessões `SessionLocal` e disponibiliza `get_db()` para as rotas. As tabelas são criadas automaticamente por `Base.metadata.create_all()` quando a aplicação inicia.

- **eventos:** guarda os dados do evento.
- **participantes:** guarda nome, e-mail (único) e curso.
- **inscricoes:** relaciona evento e participante, registra a data/hora e possui uma restrição UNIQUE para impedir duas inscrições da mesma pessoa no mesmo evento.

Evento 1:N Inscrição e Participante 1:N Inscrição. As chaves estrangeiras estão ativadas no SQLite. Ao excluir evento ou participante, suas inscrições relacionadas são removidas em cascata. O banco fica na pasta do projeto; para reiniciar os dados, encerre a aplicação e remova o arquivo `eventos_academicos.db`.

## 5. Instalação

Abra o terminal na pasta do projeto.

Windows:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 6. Execução

```bash
uvicorn main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

## 7. Principais rotas

| Método | Rota | Função |
|---|---|---|
| POST | `/eventos` | Cadastrar evento |
| GET | `/eventos` | Listar eventos |
| GET | `/eventos/{id}` | Consultar evento |
| PUT | `/eventos/{id}` | Atualizar evento |
| DELETE | `/eventos/{id}` | Excluir evento |
| POST | `/participantes` | Cadastrar participante |
| GET | `/participantes` | Listar participantes |
| GET | `/participantes/{id}` | Consultar participante |
| PUT | `/participantes/{id}` | Atualizar participante |
| DELETE | `/participantes/{id}` | Excluir participante |
| POST | `/eventos/{evento_id}/inscricoes/{participante_id}` | Realizar inscrição |
| GET | `/eventos/{evento_id}/inscricoes` | Listar inscritos |

## 8. Relatórios

| Método | Rota | Informações retornadas |
|---|---|---|
| GET | `/relatorios/eventos/ocupacao` | Capacidade, inscritos, vagas restantes e percentual de ocupação de cada evento |
| GET | `/relatorios/eventos/categorias` | Total de eventos, capacidade e inscrições por categoria |
| GET | `/relatorios/participantes/cursos` | Participantes cadastrados e inscrições por curso |

Os relatórios são calculados dinamicamente com consultas SQLAlchemy (`COUNT`, `SUM`, `GROUP BY` e `OUTER JOIN`). O `OUTER JOIN` permite incluir eventos sem inscrições e participantes sem inscrições. A contagem distinta evita contar repetidamente o mesmo participante no relatório por curso. O percentual de ocupação é calculado como inscritos ÷ capacidade × 100.

## 9. Exemplos de utilização

### Cadastrar evento – POST `/eventos`

```json
{
  "titulo": "Workshop de Python",
  "descricao": "Introdução ao Python e FastAPI",
  "data": "2026-11-20",
  "horario": "19:00:00",
  "local": "Laboratório 01",
  "capacidade": 30,
  "categoria": "Workshop"
}
```

### Cadastrar participante – POST `/participantes`

```json
{
  "nome": "Maria Silva",
  "email": "maria@email.com",
  "curso": "Engenharia de Software"
}
```

### Inscrever participante

POST `/eventos/1/inscricoes/1`

A resposta contém o identificador da inscrição, os IDs do evento e participante e a data/hora registrada.

### Exemplo de relatório de ocupação

GET `/relatorios/eventos/ocupacao`

```json
[
  {
    "evento_id": 1,
    "titulo": "Workshop de Python",
    "capacidade": 30,
    "total_inscritos": 1,
    "vagas_disponiveis": 29,
    "percentual_ocupacao": 3.33
  }
]
```

O resultado acima é ilustrativo: os números dependem dos dados efetivamente cadastrados no banco.

## 10. Validações e tratamento de erros

- Título, descrição, nome, curso e local não podem ficar vazios.
- E-mail deve ter formato válido e ser único.
- Capacidade deve ser maior que zero.
- Data e horário devem possuir formato válido.
- Evento e participante precisam existir antes da inscrição.
- Inscrição duplicada é bloqueada.
- Não é possível ultrapassar a capacidade do evento.
- Não é possível reduzir a capacidade abaixo do total já inscrito.

Códigos utilizados: `201 Created`, `200 OK`, `204 No Content`, `404 Not Found`, `409 Conflict` e `422 Unprocessable Entity`. Falhas de integridade são tratadas sem expor detalhes técnicos do banco.

## 11. Roteiro de testes no Swagger

1. Execute a aplicação e abra `/docs`.
2. Cadastre dois eventos, preferencialmente com categorias e capacidades diferentes.
3. Cadastre participantes de pelo menos dois cursos.
4. Consulte os eventos e participantes para conferir os registros.
5. Atualize um evento e um participante.
6. Faça uma inscrição válida.
7. Tente repetir a mesma inscrição: deve retornar 409.
8. Tente inscrever em evento inexistente: deve retornar 404.
9. Preencha todas as vagas e tente outra inscrição: deve retornar 409.
10. Consulte os inscritos do evento.
11. Consulte os três relatórios e confira os totais.
12. Pare e reinicie o servidor. Consulte novamente os cadastros para comprovar a persistência.
13. Faça uma exclusão e consulte os relatórios novamente para verificar a atualização dos totais.

Para comprovar a persistência, não apague o arquivo `eventos_academicos.db` entre as execuções. Os relatórios podem retornar listas vazias quando ainda não houver registros.

## 12. Arquitetura MVC e responsabilidades

- **Controller:** recebe as requisições HTTP, injeta a sessão e chama os serviços.
- **Model:** representa as tabelas e os relacionamentos do banco com SQLAlchemy.
- **Schema:** valida entradas e define os formatos das respostas com Pydantic.
- **Service:** executa regras de negócio, operações de persistência e consultas dos relatórios.
- **Database:** configura conexão, sessões e acesso ao SQLite.

## 13. Repositório

Repositório no GitHub: https://github.com/leonardofigura-coder/APS3_Backend_Leonardo_Figura
