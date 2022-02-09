import contextlib

import pytest

from auth import create_app
from auth.extensions import db

from . import config


@pytest.fixture
def app():
    return create_app(config=config)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def session():
    yield db.session
    _clear_all_tables(db)


def _clear_all_tables(db):
    meta = db.metadata
    with contextlib.closing(db.engine.connect()) as con:
        trans = con.begin()
        for table in reversed(meta.sorted_tables):
            con.execute(table.delete())
        trans.commit()
