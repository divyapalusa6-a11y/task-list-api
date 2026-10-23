from flask import abort, make_response
from ..db import db
from sqlalchemy import asc, desc
def validate_model(cls, id):
    try:
        id = int(id)
    except ValueError:
        invalid = {"message": f"{cls.__name__} id ({id}) is invalid."}
        abort(make_response(invalid, 400))

    query = db.select(cls).where(cls.id == id)
    model = db.session.scalar(query)
    if not model:    
        not_found = {"message": f"{cls.__name__} with id ({id}) not found."}
        abort(make_response(not_found, 404))

    return model

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError as e:
        response = {"message": f"Invalid request: missing {e.args[0]}"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

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



