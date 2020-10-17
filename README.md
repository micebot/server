<div align='center'>
    <img src='https://raw.githubusercontent.com/micebot/assets/master/images/logo-256x256.png'>
</div>
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
<div align='center'>
    <a href='https://github.com/micebot/server/actions?query=workflow%3A%22Deploy+to+staging%22'>
        <img src='https://github.com/micebot/server/workflows/Deploy%20to%20staging/badge.svg'/>
    </a>
    <a href='https://github.com/micebot/server/actions?query=workflow%3A%22Deploy+to+production%22'>
        <img src='https://github.com/micebot/server/workflows/Deploy%20to%20production/badge.svg'/>
    </a>
    <a href='https://codecov.io/gh/micebot/server/branch/development'>
        <img src='https://codecov.io/gh/micebot/server/branch/development/graph/badge.svg'>
    </a>
</div>

Este repositório contém o _core_ de toda a aplicação, responsável por manter a persistência dos dados e as regras do nosso [bot da Twitch][1] e o nosso [bot do Discord][2]. A ideia por trás desse projeto é automatizar o processo de entrega de premiações (inicialmente, somente e-books) durante as lives do canal [@codigofalado][3].

# Documentação

Disponibilizamos um ambiente de testes muito semelhante ao que é utilizado em produção. Nele você pode visualizar, criar, editar e remover produtos e/ou pedidos. Produtos, são basicamente os itens que podem ser resgatados (as premiações). Pedidos, são as requisições criadas pelos moderadores e/ou o streammer, para que seja entregue um produto a um determinado usuário via
sussurro na Twitch:

## Ambiente de testes (staging)

Acesse o ambiente [**neste link**](https://app-dev-micebot.herokuapp.com/docs) e utilize uma das seguintes contas:

- Usuário I:

  - username: `ps_user`
  - password: `ps_pass`

- Usuário II:
  - username: `ds_user`
  - password: `ds_pass`

Uma vez autorizado, você pode consumir qualquer rota da nossa API. Também temos a [documentação estática](https://app-dev-micebot.herokuapp.com/redoc), utilizando Redoc, caso tenha interesse.

# Contribuindo

Para executar este projeto é necessário que você tenha o Python 3.8+ instalado, [Poetry][4] e Docker. Também recomendamos utilizar a configuração [`poetry config virtualenvs.in-project true`][5] para que o ambiente virtual seja criado na raiz do projeto, não é uma necessidade mas facilitará sua vida. **;)** Tendo tudo devidamente instalado e configurado:

1. Clone este repositório e instale as dependências:

```
git clone https://github.com/micebot/server.git
cd ./server

poetry install
```

2. Execute o script `sh scripts/db-docker-container.sh` para criar um novo container com a imagem do Postgresql 12 linkado à porta 5432. Se tiver problemas para executar o script, pode executar manualmente:

```
docker run \
    --name micebot \
    -p 5432:5432 \
    -e POSTGRES_DB=micebot \
    -e POSTGRES_USER=micebot \
    -e POSTGRES_PASSWORD=micebot \
    -d postgres:12
```

3. Entre no _virtual env_, rode as migrações e execute a aplicação:

```
poetry shell
alembic upgrade head
uvicorn server:app --reload
```

[1]: https://github.com/micebot/pubsub
[2]: https://github.com/micebot/discord
[3]: https://www.twitch.tv/codigofalado
[4]: https://python-poetry.org/docs/#installation
[5]: https://python-poetry.org/docs/configuration/#virtualenvsin-project-boolean
