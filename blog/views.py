import datetime
import functools

from flask import Blueprint, render_template, request

from blog.db import db
from blog.models import Film, Person, Planet, Starship, Vehicle

bp = Blueprint("website", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/people")
def people():
    page = request.args.get('page') or 1

    people = Person.query
    films = Film.query.order_by('title')
    starships = Starship.query.order_by('name')
    vehicles = Vehicle.query.order_by('name')
    planets = Planet.query.order_by('name')

    film_filter = request.args.get('film')
    if film_filter:
        people = people.filter(Person.films.any(Film.id == film_filter))

    starship_filter = request.args.get('starship')
    if starship_filter:
        people = people.filter(Person.starships.any(
            Starship.id == starship_filter))

    vehicle_filter = request.args.get('vehicle')
    if vehicle_filter:
        people = people.filter(Person.vehicles.any(
            Vehicle.id == vehicle_filter))

    planet_filter = request.args.get('planet')
    if planet_filter:
        people = people.filter(
            Person.homeworld.has(Planet.id == planet_filter))

    order_by = request.args.get('order')
    if order_by:
        people = people.order_by(order_by)

    people = people.paginate(int(page), 10, False)

    return render_template("people.html", people=people, films=films, starships=starships, vehicles=vehicles, planets=planets, args=request.args)


@bp.route("/starships")
def starship():
    starships = Starship.query.order_by(Starship.score.desc())
    return render_template("starship.html", starships=starships)
