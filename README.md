<h1 align='center'>
    M I C E B O T<br>
    <img src='https://raw.githubusercontent.com/micebot/assets/master/images/logo-256x256.png'>
</h1>
<br>
<div align='center'>
    <a href='https://github.com/psf/black'>
        <img src='https://img.shields.io/badge/code%20style-black-000000.svg'/>
    </a>
    <a href='https://github.com/micebot/server/issues'>
        <img src='https://badgen.net/github/open-issues/micebot/server'>
    </a>
    <a href='https://github.com/micebot/server/commits/development'>
        <img src='https://badgen.net/github/last-commit/micebot/server/development'>
    </a>
</div>
<br>

Bem-vindo(a)! Este repositório contém o _core_ de toda a aplicação, responsável por manter a persistência dos dados
e as regras da nossa integração entre Twitch e o nosso bot do Discord. A ideia por trás desse projeto é automatizar
o processo de entrega de premiações durante as lives do canal [@codigofalado][10].

Veja também os outros projetos:

- [Integração com a Twitch][11]
- [Bot do Discord][12]

## Documentação

Disponibilizamos um ambiente de testes que lhe permite visualizar, criar, editar
e remover produtos e/ou pedidos. Produtos, são basicamente os itens que podem ser
resgatados (as premiações). Pedidos, são as requisições criadas pelos moderadores
e/ou o streammer, para que seja entregue um produto a um determinado usuário via
sussurro na Twitch.

Nossa "documentação viva" com Swagger que está online e disponível
[**neste link**][14]. Para se autenticar, você pode utilizar um dos dois
usuários seguintes:

- Usuário I:

  - username: `ps_user`
  - password: `ps_pass`

- Usuário II:
  - username: `ds_user`
  - password: `ds_pass`

Uma vez autorizado, você pode consumir qualquer rota da nossa API.

Também temos a [documentação estática][15], utilizando Redoc.

<sub>**PS:** Pode ser que demore para carregar em um primeiro momento, isto porque
estamos utilizando os dynos gratuitos do Heroku que "desligam" a aplicação após
[30min de inatividade][16] (_isto é, sem nenhuma requisição nesse período_).</sub>

## Contribuindo

Para executar este projeto é necessário que você tenha o Python 3.8+ instalado, o [Poetry][17] e o Postgresql como
banco de dados. Nós preferimos utilizar um container Docker para a parte do BD. Recomendamos utilizar a configuração
[`poetry virtualenvs.in-project`][18] como `true` para que o ambiente virtual seja criado na raiz do projeto, não é
uma necessidade mas facilitará sua vida. **;)** Tendo tudo devidamente instalado e configurado:

1. Clone este repositório e instale as dependências:

```
git clone https://github.com/micebot/server.git
cd ./server

poetry install
```

2. Execute um container com a imagem do Postgresql 12 linkado à porta 5432:

```
docker run --name micebot_db -p 5432:5432 -e POSTGRES_DB=micebot -e POSTGRES_USER=micebot -e POSTGRES_PASSWORD=micebot -d postgres:12
```

3. Entre no _virtual env_, rode as migrações e execute a aplicação:

```
poetry shell
alembic upgrade head
uvicorn server:app --reload
```

## Workflows

| Branch          | Status                     |
| --------------- | -------------------------- |
| **Development** | [![pipeline status][1]][2] |
| **Master**      | [![pipeline status][5]][6] |

[1]: https://github.com/micebot/server/workflows/Continuous%20Integration%20&%20Deploy%20(Staging)/badge.svg
[2]: https://github.com/micebot/server/actions?query=workflow%3A%22Continuous+Integration+%26+Deploy+%28Staging%29%22
[5]: https://github.com/micebot/server/workflows/Continuous%20Integration%20&%20Deploy%20(Production)/badge.svg
[6]: https://github.com/micebot/server/actions?query=workflow%3A%22Continuous+Integration+%26+Deploy+%28Production%29%22
[9]: https://github.com/codigofalado/desafio333
[10]: https://www.twitch.tv/codigofalado
[11]: https://github.com/micebot/pubsub
[12]: https://github.com/micebot/discord
[14]: https://app-dev-micebot.herokuapp.com/docs
[15]: https://app-dev-micebot.herokuapp.com/redoc
[16]: https://devcenter.heroku.com/articles/free-dyno-hours
[17]: https://python-poetry.org/docs/#installation
[18]: https://python-poetry.org/docs/configuration/#virtualenvsin-project-boolean
