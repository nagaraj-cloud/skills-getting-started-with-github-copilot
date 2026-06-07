"""
Tests for DELETE /activities/{activity_name}/participants endpoint

These tests follow the Arrange-Act-Assert (AAA) pattern.
"""

import pytest


class TestRemoveParticipant:
    """Tests for removing students from activities"""

    def test_remove_participant_successfully(self, client):
        """
        Test that a participant can be successfully removed from an activity
        
        Arrange: Sign up a student, then prepare to remove them
        Act: Send DELETE request to /activities/{activity_name}/participants with email
        Assert: Response status is 200 and contains success message
        """
        # Arrange
        activity_name = "Swimming Club"
        email = "removeme@mergington.edu"
        
        # First, sign up the student
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_remove_fails_for_nonexistent_participant(self, client):
        """
        Test that removal fails when participant is not enrolled in the activity
        
        Arrange: Prepare an email that is not enrolled in any activity
        Act: Send DELETE request for participant not in activity
        Assert: Response status is 400 and error message indicates participant not found
        """
        # Arrange
        activity_name = "Art Studio"
        email = "notamember@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower() or "participant" in data["detail"].lower()

    def test_remove_fails_with_invalid_activity(self, client):
        """
        Test that removal fails when activity doesn't exist
        
        Arrange: Prepare a nonexistent activity name and email
        Act: Send DELETE request for activity that doesn't exist
        Assert: Response status is 404 and error message indicates activity not found
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_remove_fails_without_email_parameter(self, client):
        """
        Test that removal fails when email query parameter is missing
        
        Arrange: Prepare a valid activity name but no email parameter
        Act: Send DELETE request without email query parameter
        Assert: Response status is 422 (validation error)
        """
        # Arrange
        activity_name = "Drama Club"

        # Act
        response = client.delete(f"/activities/{activity_name}/participants")

        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        # 422 validation error should indicate missing parameter
