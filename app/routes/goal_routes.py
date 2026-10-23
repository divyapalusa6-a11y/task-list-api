from ..routes.routes_utilities import validate_model, create_model, get_models_with_filters
from flask import abort, Blueprint, make_response, request , Response
from ..models.goal import Goal
from ..models.task import Task
from ..db import db
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.post("")
def create_goal():    
    request_body = request.get_json()    
    return create_model(Goal, request_body)

@goals_bp.post("/<id>/tasks")
def create_task_with_goal_id(id): 
    goal = validate_model(Goal, id)    
    request_body = request.get_json()    
    task_ids = request_body.get("task_ids", [])    
    tasks_to_add = []    
    for task_id in task_ids:        
        task = validate_model(Task, task_id)        
        tasks_to_add.append(task)    
        goal.tasks = tasks_to_add    
        db.session.commit()    
        response_body = {        
            "id": goal.id,        
            "task_ids": [task.id for task in goal.tasks]    
            }    
        return create_model(Task, response_body, status=200)
    
@goals_bp.get("")
def get_all_goals():    
    return get_models_with_filters(Goal, request.args)

@goals_bp.get("/<id>")
def get_goal(id):   
    goal = validate_model(Goal, id)    
    return goal.to_dict()

@goals_bp.get("/<id>/tasks")

def get_all_goal_tasks(id):    
    goal = validate_model(Goal, id)    
    tasks = [task.to_dict() for task in goal.tasks]    
    response_body = {        
        "id": goal.id,        
        "title": goal.title,       
        "tasks": tasks   
        }
    return Response(response_body ,status=200, mimetype="application/json")  
@goals_bp.put("/<id>")
def replace_goal(id):    
    goal = validate_model(Goal, id)     
    request_body = request.get_json()    
    goal.title = request_body["title"]     
    db.session.commit()    
    return Response(status=204, mimetype="application/json")

@goals_bp.delete("/<id>")
def delete_goal(id):    
    goal = validate_model(Goal, id)    
    db.session.delete(goal)    
    db.session.commit()    
    return Response(status=204, mimetype="application/json")