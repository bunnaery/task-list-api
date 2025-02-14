from flask import Blueprint, jsonify, request
from sqlalchemy import desc, asc
from app import db
from app.models.task import Task
from datetime import datetime, timezone
import requests
import os


task_bp = Blueprint("task", __name__, url_prefix="/tasks")


@task_bp.route("", methods=["GET"])
def get_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    elif sort_query == "desc":
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()

    response = []
    for task in tasks:
        response.append(task.to_dict())

    return jsonify(response), 200


@task_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return {"task": task.to_dict()}, 200


@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        return {"details": "Invalid data"}, 400
    
    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201


@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": task.to_dict()}, 200


@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = Task.query.get_or_404(task_id)

    task.completed_at = str(datetime.now(timezone.utc))

    slack_bot = requests.post('https://slack.com/api/chat.postMessage', 
                        data={
                            'channel': 'C05N61M2JHG',
                            'text': f'Task "{task.title}" was marked complete!'},
                        headers={'Authorization': os.environ.get("SLACK_API_TOKEN")})
    
    db.session.commit()

    return {"task": task.to_dict()}, 200


@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get_or_404(task_id)

    task.completed_at = None

    db.session.commit()

    return {"task": task.to_dict()}, 200


@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": (f'Task {task.task_id} "{task.title}" '
                        'successfully deleted')}, 200