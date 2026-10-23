import pytest  # type: ignore[reportMissingImports]
from app import create_app
from app.db import db
from flask import request_finished  # type: ignore[reportMissingImports]
try:
    from importlib import import_module

    load_dotenv = import_module("dotenv").load_dotenv
except ImportError:
    load_dotenv = None
import os
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime

if load_dotenv is not None:
    load_dotenv()

@pytest.fixture
def app():
    # create the app with a test configuration
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# This fixture gets called in every test that
# references "one_task"
# This fixture creates a task and saves it in the database
@pytest.fixture
def one_task(app):
    new_task = Task()
    new_task.title = "Go on my daily walk 🏞"
    new_task.description = "Notice something new every day"
    new_task.completed_at = None
    db.session.add(new_task)
    db.session.commit()
    return new_task

# This fixture gets called in every test that
# references "three_tasks"
# This fixture creates three tasks and saves
# them in the database
@pytest.fixture
def three_tasks(app):
    tasks = []
    for title in [
        "Water the garden 🌷",
        "Answer forgotten email 📧",
        "Pay my outstanding tickets 😭",
    ]:
        task = Task()
        task.title = title
        task.description = ""
        task.completed_at = None
        tasks.append(task)

    db.session.add_all(tasks)
    db.session.commit()

@pytest.fixture
def completed_task(app):
    new_task = Task()
    new_task.title = "Go on my daily walk 🏞"
    new_task.description = "Notice something new every day"
    new_task.completed_at = datetime.now()
    db.session.add(new_task)
    db.session.commit()
    return new_task

# This fixture gets called in every test that
# references "one_goal"
# This fixture creates a goal and saves it in the database
@pytest.fixture
def one_goal(app):
    new_goal = Goal()
    new_goal.title = "Build a habit of going outside daily"
    db.session.add(new_goal)
    db.session.commit()


# This fixture gets called in every test that
# references "one_task_belongs_to_one_goal"
# This fixture creates a task and a goal
# It associates the goal and task, so that the
# goal has this task, and the task belongs to one goal
@pytest.fixture
def one_task_belongs_to_one_goal(app, one_goal, one_task):
    task_query = db.select(Task).where(Task.id == 1)
    goal_query = db.select(Goal).where(Goal.id == 1)
    task = db.session.scalar(task_query)
    goal = db.session.scalar(goal_query)
    goal.tasks.append(task)
    db.session.commit()