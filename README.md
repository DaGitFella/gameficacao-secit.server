# Gamificação SECIT API

Sistema Web que visa auxiliar o transcorrer da gamificação do evento SECIT (Semana de Ciência e Tecnologia), que ocorre
anualmente no IFRN campus Natal - Zona-Norte, RN, Brasil.

## Principais funções

- Gerenciar evento (o que inclui conquistas, selos, atividades e brindes)
- Atribuir participação nas atividades do evento aos participantes individualmente ou por meio do processamento de
  planilhas
- Verificar quais brindes um participante pode retirar

## Stack utilizada

Optamos pela arquitetura SPA + API REST.

- Angular (SPA; Typescript)
- Django Rest Framework (API REST; Python)
- MySQL
- Bootstrap

## Participantes

### Como alunos:

- Davi Lucas da Silva Bezerra (SPA)
- Isaque Victor do Nascimento Dantas (API REST)
- Lucas Henrique Correia Carvalho (UX/UI)

### Como orientadores

- Alba Sandyra Lopes (orientadora)
- Miguel Kodyluke (co-orientador)
- Arthur Santiago (co-orientador)

## Observações

Quanto ao CRUD dos eventos, não foi possível usar o método `bulk_create`, do DRF (Django Rest Framework) porque,
conforme a [documentação oficial](https://docs.djangoproject.com/en/5.1/ref/models/querysets/), ele não retorna as
chaves primárias dos objetos salvos dado o contexto deste projeto.

> If the model’s primary key is an AutoField and ignore_conflicts is False, the primary key attribute can only be
> retrieved on certain databases (currently PostgreSQL, MariaDB, and SQLite 3.35+). On other databases, it will not be
> set.
