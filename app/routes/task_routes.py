from flask import Blueprint, jsonify, request, Response
import requests
from app.db import db
from app.models.task import Task
from datetime import datetime, timezone
import os


tasks_bp = Blueprint("tasks_bp", __name__,url_prefix="/tasks" )
SLACK_CHANNEL = "task-notifications-c26"
def get_task_or_404(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return None
    return task
def not_found_response(task_id):
    return {
        "message": f"Task with id ({task_id})not found."
    }, 404


#@tasks_bp.route("/tasks", methods=["GET"])
#def get_tasks():
    #tasks = db.session.scalars(db.select(Task)).all()
    #return jsonify([task.to_dict() for task in tasks])

@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    sort_order = request.args.get("sort", "asc")

    if sort_order == "desc":
        sort_column = Task.title.desc()
    else:
        sort_column = Task.title.asc()

    tasks = db.session.scalars(
        db.select(Task).order_by(sort_column)).all()
    return jsonify([task.to_dict() for task in tasks]), 200


@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if request_body is None:
        return jsonify({"message": "Invalid data"}), 400

    try:
        task = Task.from_dict(request_body)
    except KeyError:
        return jsonify({"message": "Invalid data"}), 400

    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201


@tasks_bp.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    task = get_task_or_404(task_id)
    if task is None:
        return not_found_response(task_id)

    return jsonify(task.to_dict())


@tasks_bp.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = get_task_or_404(task_id)
    if task is None:
        return not_found_response(task_id)

    request_body = request.get_json()

    if request_body is None:
        return jsonify({"message": "Invalid data"}), 400

    if "title" not in request_body and "description" not in request_body:
        return jsonify({"message": "Invalid data"}), 400

    if "title" in request_body:
        task.title = request_body["title"]
    if "description" in request_body:
        task.description = request_body["description"]

    db.session.commit()
    return jsonify({}), 204


@tasks_bp.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = get_task_or_404(task_id)
    if task is None:
        return not_found_response(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({}), 204


@tasks_bp.route("/<int:task_id>/mark_complete", methods=["PATCH"])
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
    requests.post(url, headers=headers, json=request_body)

@tasks_bp.route("/<int:task_id>/mark_incomplete", methods=["PATCH"])
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
