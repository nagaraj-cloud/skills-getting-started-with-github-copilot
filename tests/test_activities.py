"""
Tests for GET /activities endpoint

These tests follow the Arrange-Act-Assert (AAA) pattern.
"""

import pytest


class TestGetActivities:
    """Tests for retrieving all activities"""

    def test_get_all_activities_returns_success(self, client):
        """
        Test that GET /activities returns all activities successfully
        
        Arrange: Create TestClient
        Act: Send GET request to /activities
        Assert: Response status is 200 and contains activities data
        """
        # Arrange
        # (client fixture is automatically provided)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) > 0
        # Verify some expected activities exist
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Basketball Team" in activities

    def test_activities_have_required_fields(self, client):
        """
        Test that each activity has all required fields
        
        Arrange: Get all activities
        Act: Parse response and inspect structure
        Assert: Each activity has description, schedule, max_participants, participants
        """
        # Arrange
        # (client fixture is automatically provided)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        required_fields = {"description", "schedule", "max_participants", "participants"}
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data, dict), f"Activity {activity_name} should be a dict"
            assert required_fields.issubset(activity_data.keys()), \
                f"Activity {activity_name} missing required fields"

    def test_participants_list_is_valid(self, client):
        """
        Test that participants field contains a list of emails
        
        Arrange: Get all activities
        Act: Inspect participants field for each activity
        Assert: participants is a list
        """
        # Arrange
        # (client fixture is automatically provided)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            participants = activity_data.get("participants")
            assert isinstance(participants, list), \
                f"Activity {activity_name} participants should be a list, got {type(participants)}"
            # If there are participants, they should be strings (email-like)
            for participant in participants:
                assert isinstance(participant, str), \
                    f"Participant {participant} in {activity_name} should be a string"
