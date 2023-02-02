# -*- encoding: utf-8 -*-


from typing import List, Optional
from paja_reitit import db
from sqlalchemy.orm import Mapped, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from paja_reitit.route.util import get_name, get_date_ago

class Route(db.Model):
    __tablename__ = 'route'

    id            = db.Column(db.Integer, primary_key=True)
    grade         = db.Column(db.String(4))
    created_at    = db.Column(db.DateTime, default=datetime.now())
    deleted       = db.Column(db.Boolean, default=False)
    
    color_id      = db.Column(db.Integer, db.ForeignKey('color.id'))
    color: Mapped[Optional["Color"]] = db.relationship()
    
    setter_id     = db.Column(db.Integer, db.ForeignKey('routesetter.id'))
    setter: Mapped[Optional["Routesetter"]] = db.relationship(back_populates="routes")
    
    sector_id     = db.Column(db.Integer, db.ForeignKey('sector.id'))
    sector: Mapped[Optional["Sector"]] = db.relationship(back_populates="routes")
    

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
        return str(self.id)
    
    @hybrid_property
    def name(self):
        return get_name(self)

    @hybrid_property
    def date_ago(self):
        return get_date_ago(self)
    
    @classmethod
    def find_by_grade(cls, grade: str) -> "Route":
        return cls.query.filter_by(grade=grade).first()

    @classmethod
    def find_by_creator(cls, creator: str) -> "Route":
        return cls.query.filter_by(creator=creator).first()

    @classmethod
    def find_by_sector(cls, sector_id: str) -> Query["Route"]:
        return cls.query.filter_by(sector_id=sector_id)
    
    @classmethod
    def find_by_id(cls, _id: int) -> "Route":
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def get_all_on_wall(cls, sort=True) -> Query["Route"]:
        routes = cls.query.filter_by(deleted=False)
        if sort:
            routes = routes.order_by(cls.created_at.desc())
        return routes
    
    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
          
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise SQLAlchemyError(error, 422) # InvalidUsage
    
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
