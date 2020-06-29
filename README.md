# Test Sensedata

This repo provide a website that display data from swapi.dev

There's some rules to follow when developing the website. These rules are:
- Primeira página: Uma tabela com os dados dos personagens do Start Wars com as seguintes features:
    - Suportar paginação de 10 em 10 registros.
    - Ordenação por Nome, Gênero, Peso e Altura dos personagens.
    - Opcao em tela para filtrar po Film, Startship, Vehicles e Planets
- Segunda página: Tabela com dados das startships disponíveis: Uma página contendo uma tabela com o score de cada uma das starships fornecidas.
    - Esse score deverá ser composto pelo hyperdrive_rating dividido pelo cost_in_credits da nave.
    - Exibir as naves numa tabela ordenada em ordem decrescente da melhor nave para a pior.

And in the techinal side, these are the requisites:

- Desenvolver utilizando Flask
- Deploy em docker (pontos adicionais se já hospedar em um server pra testarmos)
- Disponibilizar o código num repositório Git pra avaliarmos.


## Basic Configuration

It's necessary Python 3.6+, and recomended virtualenv, or venv package.

First create a folder, and inside folder clone this repo thus create the virtualenv:

``` bash
# Create the folder
mkdir flask-project
cd flask-project

# Clone the repo
git clone https://github.com/gabrielbalog/test-sensedata

# Create the virtualenv
python3 -m venv venv
source venv/bin/activate

# Install the packages
pip install -r requirements.txt
```
Next it's needed to declare some environment variables to run flask properly:

``` bash
export FLASK_APP=blog
export FLASK_ENV=development
export SQLALCHEMY_DATABASE_URI="postgresql://flask:flask123@localhost/flask"
export SECRET_KEY="dev"
```

Now it's just call flask with the command run:

``` bash
flask run
```

You should be able to access http://127.0.0.1:5000/, and see the index page.

## Initializing the Database

For default the project it's configured to run on a SQLite file, so before access any page, run:

``` bash
flask init-db
```

It'll automatically create the database and add the tables and data.

## Running with Docker

There is a Dockerfile within the project if there is a need and desire to upload the system through the docker. For this it is unnecessary to uncomment the web part of the docker-compose:

That done, just go up the docker-compose normally.

## Choices made for this project

The first decision I made was related to the data structure. Between taking all the data directly from the API or putting it in a database, I opted for the second option.

Simply because you don't want to retrieve the data at the end user's request time.

Use of SQLAlchemy was mainly due to my familiarity with the extension, although I have my criticisms, it is still well used in conjunction with Flask.

Obtaining the API data was done in its creation precisely to remove the overhead of other actions in the system. Another point is that I only take data from People, and not from other endpoints. This was done mainly by not using the data, so I just preferred to take the data related to the People data and insert it into the database.

The frontend was done quickly with bootstrap, but I didn't put much emphasis on it because I didn't want to spend days doing it, although I recognize that there are improvements.

The folder structure was removed to aggregate everything in one place, but I used project conventions that will grow in the future.

Not using Alpine as base Python image, in fact a have trouble in the past working, or trying, with alpine and python this article just reinforced my choice: https://pythonspeed.com/articles/alpine-docker-python/