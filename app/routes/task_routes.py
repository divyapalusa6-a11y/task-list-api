from .routes_utilities import validate_model, create_model, get_models_with_filters
from flask import Blueprint, jsonify, request, Response
import json
from urllib.request import Request, urlopen
from app.db import db
from app.models.task import Task
from datetime import datetime, timezone
import os

bp = Blueprint("tasks_bp", __name__,url_prefix="/tasks" )
SLACK_CHANNEL = "task-notifications-c26"

@bp.post("")
def create_task():
    # request_body = request.get_json()
    # return create_model(Task, request_body)
    request_body = request.get_json(silent=True)
    if not isinstance(request_body, dict):
        return {"message": "Invalid data"}, 400

    if "title" not in request_body:
        return {"message": "Invalid data"}, 400

    if "description" not in request_body:
        return {"message": "Invalid data"}, 400

    new_task = Task()
    new_task.title = request_body["title"]
    new_task.description = request_body["description"]

    db.session.add(new_task)
    db.session.commit()

    return new_task.to_dict(), 201

@bp.get("")
def get_all_tasks():
    return get_models_with_filters(Task, request.args)

@bp.get("/<id>")
def get_single_task(id):
    task = validate_model(Task, id)
    return task.to_dict()

@bp.put("/<id>")
def replace_task(id):
    task = validate_model(Task, id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    if "completed_at" in request_body:
        task.completed_at = request_body["completed_at"]
    else:
        task.completed_at = None
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.delete("/<id>")
def delete_task(id):
    task = validate_model(Task, id)
    db.session.delete(task)
    db.session.commit()
    return Response(status=204, mimetype="application/json")


@bp.route("/<int:task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return jsonify({
            "message": f"Task with id ({task_id}) not found."
        }), 404
    if task.completed_at is None:
        task.completed_at = datetime.now(timezone.utc)
        db.session.commit()
        slack_send_mark_complete(task_id)
    return "", 204


def slack_send_mark_complete(task_id):
    slack_token = os.environ.get('SLACK_BOT_TOKEN')
    url = 'https://slack.com/api/chat.postMessage'
    headers = {"Authorization": f"Bearer {slack_token}"}
    request_body = {
        "channel": "task-notifications-c26",
        "text": f"Someone just completed the task {task_id}"
    }
    slack_request = Request(
        url,
        data=json.dumps(request_body).encode("utf-8"),
        headers={**headers, "Content-Type": "application/json"},
        method="POST",
    )
    urlopen(slack_request)

@bp.route("/<int:task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = db.session.get(Task, task_id)

    if task is None:
        return jsonify({
            "message": f"Task with id ({task_id}) not found."
        }), 404
    if task.completed_at is not None:
        task.completed_at = None
        db.session.commit()
    return "", 204
