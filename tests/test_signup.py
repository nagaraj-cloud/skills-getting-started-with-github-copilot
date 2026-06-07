"""
Tests for POST /activities/{activity_name}/signup endpoint

These tests follow the Arrange-Act-Assert (AAA) pattern.
"""

import pytest


class TestSignupForActivity:
    """Tests for signing up students for activities"""

    def test_signup_successfully_adds_student(self, client):
        """
        Test that a student can successfully sign up for an activity
        
        Arrange: Prepare a valid activity name and new student email
        Act: Send POST request to /activities/{activity_name}/signup with email
        Assert: Response status is 200 and contains success message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_prevents_duplicate_signup(self, client):
        """
        Test that a student cannot sign up twice for the same activity
        
        Arrange: Student signs up for an activity once
        Act: Attempt to sign up the same student for the same activity again
        Assert: Response status is 400 and error message indicates duplicate signup
        """
        # Arrange
        activity_name = "Programming Class"
        email = "student@mergington.edu"
        
        # First signup
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response1.status_code == 200

        # Act
        # Attempt duplicate signup
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response2.status_code == 400
        data = response2.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_signup_fails_with_invalid_activity(self, client):
        """
        Test that signup fails when activity doesn't exist
        
        Arrange: Prepare a nonexistent activity name and email
        Act: Send POST request for activity that doesn't exist
        Assert: Response status is 404 and error message indicates activity not found
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_signup_fails_without_email_parameter(self, client):
        """
        Test that signup fails when email query parameter is missing
        
        Arrange: Prepare a valid activity name but no email parameter
        Act: Send POST request without email query parameter
        Assert: Response status is 422 (validation error)
        """
        # Arrange
        activity_name = "Chess Club"

        # Act
        response = client.post(f"/activities/{activity_name}/signup")

        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        # 422 validation error should indicate missing parameter
