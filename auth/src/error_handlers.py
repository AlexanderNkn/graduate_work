from typing import Callable
from flask import json, jsonify, Flask
from werkzeug.exceptions import InternalServerError, TooManyRequests

from extensions import db, jwt, jwt_redis_blocklist


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


def register_429_error(app: Flask):
    @app.errorhandler(TooManyRequests)
    def handle_exception(error):
        """Returns JSON response instead standard HTML."""
        response = error.get_response()
        response.data = json.dumps({
            'status': 'error',
            'message': 'Too Many Requests. Try again later.',
        })
        response.content_type = "application/json"
        return response
    return handle_exception


def register_jwt_errors(config):

    # Callback function to check if a JWT exists in the redis blocklist
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token_in_redis = jwt_redis_blocklist.get(jti)
        return token_in_redis is not None

    @jwt.expired_token_loader
    def _expired_token_callback(_expired_jwt_header, _expired_jwt_data):
        return jsonify({config.JWT_ERROR_MESSAGE_KEY: "Token has expired", "status": "error"}), 401

    @jwt.invalid_token_loader
    def _invalid_token_callback(error_string):
        return jsonify({config.JWT_ERROR_MESSAGE_KEY: error_string, "status": "error"}), 422

    @jwt.unauthorized_loader
    def _unauthorized_callback(error_string):
        return jsonify({config.JWT_ERROR_MESSAGE_KEY: error_string, "status": "error"}), 401

    @jwt.needs_fresh_token_loader
    def _needs_fresh_token_callback(jwt_header, jwt_data):
        return jsonify({config.error_msg_key: "Fresh token required", "status": "error"}), 401

    @jwt.revoked_token_loader
    def _revoked_token_callback(jwt_header, jwt_data):
        return jsonify({config.JWT_ERROR_MESSAGE_KEY: "Token has been revoked", "status": "error"}), 401
