from app.models.goal import Goal
from app.db import db

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_goal_to_dict():
    #Arrange
    new_goal = Goal()
    new_goal.title = "Seize the Day!"
    new_goal.id = 1
    
    #Act
    goal_dict = new_goal.to_dict()

    #Assert
    assert goal_dict["id"] == 1
    assert goal_dict["title"] == "Seize the Day!"

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_goal_to_dict_no_id():
    #Arrange
    new_goal = Goal()
    new_goal.title = "Seize the Day!"
    
    #Act
    goal_dict = new_goal.to_dict()

    #Assert
    assert goal_dict["id"] is None
    assert goal_dict["title"] == "Seize the Day!"

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_goal_to_dict_no_title():
    #Arrange
    new_goal = Goal()
    new_goal.title = "Seize the Day!"
    new_goal.id = 1
    setattr(new_goal, "title", None)
    
    #Act
    goal_dict = new_goal.to_dict()

    #Assert
    assert goal_dict["id"] == 1
    assert goal_dict["title"] is None

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_goal_from_dict():
    #Arrange
    goal_dict =  {
        "title": "Seize the Day!",
    }
    #Act
    goal_obj =  Goal.from_dict(goal_dict)

    #Assert
    assert goal_obj.title == "Seize the Day!"

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_goal_from_dict_no_title():
    #Arrange
    goal_dict =  {
    }
    #Act & Assert
    try:
        Goal.from_dict(goal_dict)
    except KeyError as error:
        assert error.args == ("title",)
    else:
        assert False, "Expected Goal.from_dict to raise KeyError for missing title"

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goals_no_saved_goals(client):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert response_body == []

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goals_one_saved_goal(client, one_goal):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Build a habit of going outside daily"
        }
    ]

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goal(client, one_goal):
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Build a habit of going outside daily"
    }

#@pytest.mark.skip(reason="test to be completed by student")
def test_get_goal_not_found(client):
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()
    assert response.status_code == 404
    assert response_body == {"message": "Goal with id (1) not found"}

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_goal(client):
    # Act
    response = client.post("/goals", json={
        "title": "My New Goal"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "title": "My New Goal"
    }

#@pytest.mark.skip(reason="test to be completed by student")
def test_update_goal(client, one_goal):
    response = client.put("/goals/1", json={
        "title": "Updated Goal Title"
    })

    assert response.status_code == 204
    query = db.select(Goal).where(Goal.id == 1)
    goal = db.session.scalar(query)
    assert goal.title == "Updated Goal Title"

#@pytest.mark.skip(reason="test to be completed by student")
def test_update_goal_not_found(client):
    response = client.put("/goals/1", json={
        "title": "Updated Goal Title"
    })
    response_body = response.get_json()
    assert response.status_code == 404
    assert response_body == {"message": "Goal with id (1) not found"}

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_goal(client, one_goal):
    # Act
    response = client.delete("/goals/1")
    # Assert
    assert response.status_code == 204
    # Check that the goal was deleted
    response = client.get("/goals/1")
    assert response.status_code == 404
    response_body = response.get_json()
    assert "message" in response_body

#@pytest.mark.skip(reason="test to be completed by student")
def test_delete_goal_not_found(client):
    response = client.delete("/goals/1", json={
        "title": "Updated Goal Title"
    })
    response_body = response.get_json()
    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Goal with id (1) not found"}

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_goal_missing_title(client):
    # Act
    response = client.post("/goals", json={})
    response_body = response.get_json()
    
    # Assert
    assert db.session.scalars(db.select(Goal)).all() == []
    assert response.status_code == 400
    assert "message" in response_body
    assert response_body == {
        "message": "Invalid request: missing title"
    }
