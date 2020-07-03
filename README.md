<h1 align='center'>
    <img src='https://raw.githubusercontent.com/micebot/assets/master/images/logo-256x256.png'>
    <br>
    MiceBot
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

> Este é, ainda, um trabalho em progresso. 🧀
>
**MiceBot** é uma aplicação desenvolvida durante o [#desafio333][9] com objetivo
de tornar automatizado todo o processo de entrega de cupons de e-books sorteados
durante as lives do canal [@codigofalado][10].

Este repositório contém o "_core_" da aplicação, isto é, onde todas as regras
são centralizadas. Disponibilizamos uma API que permite a integração com outras
aplicações da organização [**@micebot**][13]: utilizada pelo [pubsub][11] e o
nosso [bot do Discord][12].

## Documentação

Você pode visualizar a documentação [neste link][15].

Também disponibilizamos uma URL com a "documentação viva" para que você possa
testar nosso endpoint e as rotas da aplicação [neste outro link][14]. Este
ambiente é isolado para testes. 💣 As credências para autenticação são:

- Usuário I:
    - username: `ps_user`
    - password: `ps_pass`

- Usuário II (Alternativo):
  - username: `ds_user`
  - password: `ds_pass`

 

## Development status

| Branch | Pipeline | Coverage | 
| ------ | ----- | ----- |
| **Development** | [![pipeline status][1]][2] | [![coverage report][3]][4] |
| **Master** | [![pipeline status][5]][6] | [![coverage report][7]][8] |

[1]:https://gitlab.com/micebot/server-ci/badges/development/pipeline.svg
[2]:https://gitlab.com/micebot/server-ci/-/pipelines?page=1&scope=all&ref=development
[3]:https://gitlab.com/micebot/server-ci/badges/development/coverage.svg
[4]:https://gitlab.com/micebot/server-ci/-/commits/development
[5]:https://gitlab.com/micebot/server-ci/badges/master/pipeline.svg
[6]:https://gitlab.com/micebot/server-ci/-/pipelines?page=1&scope=all&ref=master
[7]:https://gitlab.com/micebot/server-ci/badges/master/coverage.svg
[8]:https://gitlab.com/micebot/server-ci/-/commits/master
[9]:https://github.com/codigofalado/desafio333
[10]:https://www.twitch.tv/codigofalado
[11]:https://github.com/micebot/pubsub
[12]:https://github.com/micebot/discord
[13]:https://github.com/micebot/
[14]:https://micebot-server-dev.herokuapp.com/docs
[15]:https://micebot-server-dev.herokuapp.com/redoc