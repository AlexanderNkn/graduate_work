from typing import Callable
from flask import json, Flask
from werkzeug.exceptions import InternalServerError

from extensions import db


def rollback_transaction():
    db.session.rollback()


def register_500_error(app: Flask, sentry_event: Callable):
    @app.errorhandler(InternalServerError)
    def handle_exception(error):
        """Rollback session with exception then return JSON with sentry task id."""
        rollback_transaction()
        response = error.get_response()
        response.data = json.dumps({
            'status': 'error',
            'message': 'Something went wrong with server',
            'sentry': sentry_event(),
        })
        response.content_type = "application/json"
        return response
    return handle_exception
