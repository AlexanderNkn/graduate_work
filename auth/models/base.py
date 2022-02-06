import datetime

from flask_sqlalchemy import SQLAlchemy
from db.postgres import db as db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.datetime.now())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)
