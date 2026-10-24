import json
import pytest
from werkzeug.exceptions import HTTPException
from app.models.goal import Goal
from app.models.task import Task
from app.routes.routes_utilities import create_model, validate_model

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_route_utilities_validate_model_with_task(client, three_tasks):
    #Act
    task_1 = validate_model(Task, 1)
    task_2 = validate_model(Task, 2)
    task_3 = validate_model(Task, 3)

    #Assert
    assert task_1.id == 1
    assert task_1.title == "Water the garden 🌷"
    assert task_1.description == ""
    assert task_1.completed_at is None

    assert task_2.id == 2
    assert task_2.title == "Answer forgotten email 📧"

    assert task_3.id == 3
    assert task_3.title == "Pay my outstanding tickets 😭"

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_route_utilities_validate_model_with_task_invalid_id(client, three_tasks):
    #Act & Assert
    # Calling `validate_model` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException) as e:
        result_task = validate_model(Task, "One")
    response = e.value.get_response()
    assert response.status_code == 400
    response_body = json.loads(e.value.get_body())
    assert response_body == {
        "message": "Task id (One) is invalid."
    }
    
def test_route_utilities_validate_model_with_task_missing_id(
    client, three_tasks):
    with pytest.raises(HTTPException) as e:
        validate_model(Task, 4)
    response = e.value.get_response()
    assert response.status_code == 404
    response_body = json.loads(e.value.get_body())
    assert response_body == {
        "message": "Task with id (4) not found"
    }
#@pytest.mark.skip(reason="No way to test this feature yet")
def test_route_utilities_validate_model_with_goal(client, one_goal):
    #Act
    goal_1 = validate_model(Goal, 1)

    #Assert
    assert goal_1.id == 1
    assert goal_1.title == "Build a habit of going outside daily"

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_route_utilities_validate_model_with_goal_invalid_id(client, one_goal):
    #Act & Assert
    with pytest.raises(HTTPException) as e:
        result_task = validate_model(Goal, "One")
    response = e.value.get_response()
    assert response.status_code == 400
    assert json.loads(e.value.get_body()) == {"message": "Goal id (One) is invalid."}
    
#@pytest.mark.skip(reason="No way to test this feature yet")
def test_route_utilities_validate_model_with_goal_missing_id(client, one_goal):
    #Act & Assert
    with pytest.raises(HTTPException) as e:
        result_task = validate_model(Goal, 4)
    response = e.value.get_response()
    assert response.status_code == 404
    response_body = json.loads(e.value.get_body())
    assert response_body == {
        "message": "Goal with id (4) not found"
    }
#@pytest.mark.skip(reason="No way to test this feature yet")
def test_route_utilities_create_model_with_task(client):
    #Arrange
    request_body = {
        "title": "Make the bed",
        "description": "",
        "completed_at": None
    }
    #Act
    response = create_model(Task, request_body)
    #Assert
    response_body = response[0]
    assert isinstance(response_body["id"], int)
    assert response_body["id"] > 0
    assert response_body["title"] == "Make the bed"
    assert response_body["description"] == ""
    assert response_body["is_complete"] is False
    assert response[1] == 201
    
#@pytest.mark.skip(reason="No way to test this feature yet")
def test_route_utilities_create_model_with_task_missing_title(client):
    #Arrange
    request_body = {}
    #Act
    with pytest.raises(HTTPException) as e:
        create_model(Task, request_body)
    response = e.value.get_response()
    assert response.status_code == 400
    response_body = json.loads(e.value.get_body())
    assert response_body == {
        "message": "Invalid data."
    }
#@pytest.mark.skip(reason="No way to test this feature yet")
def test_route_utilities_create_model_with_goal(client):
    #Arrange
    request_body = {
        "title": "Seize the Day!"
    }

    #Act
    response = create_model(Goal, request_body)

    #Assert
    response_body = response[0]
    assert response_body["id"] == 1
    assert response_body["title"] == "Seize the Day!"
    assert response[1] == 201

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_route_utilities_create_model_with_goal_missing_title(client):
    #Arrange
    request_body = {
    }
    #Act
    with pytest.raises(HTTPException) as e:
        create_model(Goal, request_body)
    response = e.value.get_response()
    assert response.status_code == 400

    response_body = json.loads(e.value.get_body())
    assert response_body == {"message": "Invalid data."}