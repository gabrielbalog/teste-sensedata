from datetime import datetime

from blog.db import db

films = db.Table(
    "films",
    db.Column("film_id", db.Integer, db.ForeignKey(
        "film.id"), primary_key=True),
    db.Column("person_id", db.Integer, db.ForeignKey(
        "person.id"), primary_key=True),
)
starships = db.Table(
    "starships",
    db.Column("starship_id", db.Integer, db.ForeignKey(
        "starship.id"), primary_key=True),
    db.Column("person_id", db.Integer, db.ForeignKey(
        "person.id"), primary_key=True),
)
vehicles = db.Table(
    "vehicles",
    db.Column("vehicle_id", db.Integer, db.ForeignKey(
        "vehicle.id"), primary_key=True),
    db.Column("person_id", db.Integer, db.ForeignKey(
        "person.id"), primary_key=True),
)

films_starships = db.Table(
    "films_starships",
    db.Column("film_id", db.Integer, db.ForeignKey(
        "film.id"), primary_key=True),
    db.Column("starship_id", db.Integer, db.ForeignKey(
        "starship.id"), primary_key=True),
)


class CRUDMixin(object):
    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()


class Vehicle(db.Model, CRUDMixin):
    __endpoint__ = "vehicles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return self.name

    @classmethod
    def search_by_name(cls, name):
        return cls.query.filter_by(name=name)


class Starship(db.Model, CRUDMixin):
    __endpoint__ = "starships"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    starship_class = db.Column(db.String(100), nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)
    cost_in_credits = db.Column(db.String(100), nullable=False)
    length = db.Column(db.String(100), nullable=False)
    crew = db.Column(db.String(100), nullable=False)
    passengers = db.Column(db.String(100), nullable=False)
    max_atmosphering_speed = db.Column(db.String(100), nullable=False)
    hyperdrive_rating = db.Column(db.String(100), nullable=False)
    mglt = db.Column(db.String(100), nullable=False)
    cargo_capacity = db.Column(db.String(100), nullable=False)
    consumables = db.Column(db.String(100), nullable=False)
    created = db.Column(db.String(100), nullable=False)
    edited = db.Column(db.String(100), nullable=False)
    score = db.Column(db.String(100), nullable=False)

    films = db.relationship(
        "Film", secondary=films_starships, lazy="subquery", backref=db.backref("starships", lazy=True)
    )

    def __repr__(self):
        return self.name

    @classmethod
    def search_by_name(cls, name):
        return cls.query.filter_by(name=name)


class Planet(db.Model, CRUDMixin):
    __endpoint__ = "planets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return self.name

    @classmethod
    def search_by_name(cls, name):
        return cls.query.filter_by(name=name)


class Film(db.Model, CRUDMixin):
    __endpoint__ = "films"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return self.title

    @classmethod
    def search_by_title(cls, title):
        return cls.query.filter_by(title=title)


class Person(db.Model, CRUDMixin):
    __endpoint__ = "people"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_year = db.Column(db.String(100), nullable=False)
    eye_color = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    hair_color = db.Column(db.String(100), nullable=False)
    height = db.Column(db.String(100), nullable=False)
    mass = db.Column(db.String(100), nullable=False)
    skin_color = db.Column(db.String(100), nullable=False)
    created = db.Column(db.String(100), nullable=False)
    edited = db.Column(db.String(100), nullable=False)

    homeworld_id = db.Column(
        db.Integer, db.ForeignKey("planet.id"), nullable=False)
    homeworld = db.relationship(
        "Planet", backref=db.backref("people", lazy=True))

    films = db.relationship(
        "Film", secondary=films, lazy="subquery", backref=db.backref("people", lazy=True)
    )
    starships = db.relationship(
        "Starship", secondary=starships, lazy="subquery", backref=db.backref("people", lazy=True)
    )
    vehicles = db.relationship(
        "Vehicle", secondary=vehicles, lazy="subquery", backref=db.backref("people", lazy=True)
    )

    def __repr__(self):
        return self.name

    @classmethod
    def search_by_name(cls, name):
        return cls.query.filter_by(name=name)
