from flask import abort, make_response  # type: ignore
from ..db import db
import json
from werkzeug.exceptions import HTTPException
from app.db import db


class JSONHTTPException(HTTPException):
    def __init__(self, code, message):
        super().__init__(description=message)
        self.code = code
        self.message = message

    def get_body(self, environ=None, scope=None):
        return json.dumps({
            "message": self.message
        })

    def get_headers(self, environ=None, scope=None):
        return [("Content-Type", "application/json")]

def validate_model(cls, id):
    try:
        id = int(id)
    except (ValueError, TypeError):
        raise JSONHTTPException(
            400,
            f"{cls.__name__} id ({id}) is invalid."
        )
    query = db.select(cls).where(cls.id == id)
    model = db.session.scalar(query)
    if model is None:
        raise JSONHTTPException(
            404,
            f"{cls.__name__} with id ({id}) not found"
        )
    return model

def create_model(cls, model_data):
    # Check if request data is valid
    if not isinstance(model_data, dict):
        raise JSONHTTPException(400, "Invalid data.")
    # Check if title is missing or empty
    if not model_data.get("title"):
        raise JSONHTTPException(400, "Invalid data.")
    # Check required description for Task
    if cls.__name__ == "Task" and model_data.get("description") is None:
        raise JSONHTTPException(400, "Invalid data.")
    try:
        model = cls.from_dict(model_data)
        db.session.add(model)
        db.session.commit()
    except (KeyError, TypeError, ValueError):
        db.session.rollback()
        raise JSONHTTPException(400, "Invalid data.")
    except Exception:
        db.session.rollback()
        raise
    return model.to_dict(), 201

def get_models_with_filters(cls, filters=None):
    query = db.select(cls)
    if filters:
        for attribute, value in filters.items():
            if attribute == "sort" and value.lower() == "asc":
                query = query.order_by(cls.title.asc())
            elif attribute == "sort" and value.lower() == "desc":
                query = query.order_by(cls.title.desc())
            elif hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))
    models = db.session.scalars(query)
    models_response = [model.to_dict() for model in models]
    return models_response



