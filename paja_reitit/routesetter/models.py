# -*- encoding: utf-8 -*-

from typing import List
from paja_reitit import db
from sqlalchemy.orm import Mapped
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.exc import SQLAlchemyError


class Routesetter(db.Model):

    __tablename__ = 'routesetter'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))

    routes: Mapped[List["Route"]] = db.relationship(back_populates="setter")

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.name)

    @hybrid_property
    def routes_set(self):
        return len(self.routes)

    @classmethod
    def find_by_id(cls, setter_id: str) -> 'Routesetter':
        return cls.query.filter_by(id=setter_id).first()

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise SQLAlchemyError(error, 422)  # InvalidUsage

    def delete_from_db(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise SQLAlchemyError(error, 422)
        return
