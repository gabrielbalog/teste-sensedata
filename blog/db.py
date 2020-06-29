import sqlite3

import click
import requests
from math import ceil
from flask import current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


def init_db():
    import blog.models

    db.create_all()


def drop_db():
    db.drop_all()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    from blog.models import Person, Film, Planet, Starship, Vehicle

    init_db()
    click.echo("Initialized the database.")

    people = requests.get(f'https://swapi.dev/api/people/').json()
    total_pages = ceil(people['count'] / len(people['results']))

    for page in range(1,total_pages+1):
        people = requests.get(
            f'https://swapi.dev/api/people/?page={page}').json()

        for p in people['results']:

            # Manage all films before insert person
            films = []
            for film in p['films']:
                data = requests.get(film).json()
                f = Film.search_by_title(data['title']).first()
                if not f:
                    f = Film(
                        title=data['title']
                    )
                    f.save()

                films.append(f)

            # Manage the Homeworld before insert the data
            home_data = requests.get(p['homeworld']).json()
            planet = Planet.search_by_name(home_data['name']).first()
            if not planet:
                planet = Planet(
                    name=home_data['name']
                )
                planet.save()

            # Manage all the startships before insert person
            starships = []
            for starship in p['starships']:
                data = requests.get(starship).json()
                s = Starship.search_by_name(data['name']).first()
                if not s:
                    if data['hyperdrive_rating'] == 'unknown' \
                            or data['cost_in_credits'] == 'unknown':
                        score = 0
                    else:
                        score = float(data['hyperdrive_rating']) / \
                            float(data['cost_in_credits'])

                    s = Starship(
                        name=data['name'],
                        model=data['model'],
                        starship_class=data['starship_class'],
                        manufacturer=data['manufacturer'],
                        cost_in_credits=data['cost_in_credits'],
                        length=data['length'],
                        crew=data['crew'],
                        passengers=data['passengers'],
                        max_atmosphering_speed=data['max_atmosphering_speed'],
                        hyperdrive_rating=data['hyperdrive_rating'],
                        mglt=data['MGLT'],
                        cargo_capacity=data['cargo_capacity'],
                        consumables=data['consumables'],
                        created=data['created'],
                        edited=data['edited'],
                        score=score
                    )
                    s.save()

                starships.append(s)

            # Manage all the vehicles before insert person
            vehicles = []
            for vehicle in p['vehicles']:
                data = requests.get(vehicle).json()
                v = Vehicle.search_by_name(data['name']).first()
                if not v:
                    v = Vehicle(
                        name=data['name']
                    )
                    v.save()

                vehicles.append(v)

            person = Person(
                name=p['name'],
                birth_year=p['birth_year'],
                eye_color=p['eye_color'],
                gender=p['gender'],
                hair_color=p['hair_color'],
                height=p['height'],
                mass=p['mass'],
                skin_color=p['skin_color'],
                created=p['created'],
                edited=p['edited'],
                films=films,
                homeworld=planet,
                starships=starships,
                vehicles=vehicles
            )

            person.save()

    click.echo("Initial User Created.")


@click.command("drop-db")
@with_appcontext
def drop_db_command():
    """Clear the existing data and drop all tables."""
    drop_db()
    click.echo("Database Droped.")


def init_app(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(drop_db_command)
    db.init_app(app)
