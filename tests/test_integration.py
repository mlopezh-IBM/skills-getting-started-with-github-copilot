"""
Integration tests for FastAPI activity management system endpoints.

Tests full HTTP endpoints and responses using the AAA pattern:
- Arrange: Set up TestClient and initial state
- Act: Make HTTP request to endpoint
- Assert: Verify response status code, headers, and body content
"""

import pytest


class TestRootEndpoint:
    """Tests for the root GET / endpoint."""

    def test_root_redirects_to_static_index(self, client, sample_activities):
        """
        Test that GET / redirects to the static index.html file.
        
        Arrange: Initialize TestClient (from fixture)
        Act: Make GET request to root endpoint
        Assert: Verify redirect response status and location header
        """
        # Arrange
        # (client and sample_activities from fixtures)
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307  # Temporary redirect
        assert "/static/index.html" in response.headers["location"]

    def test_root_redirect_follows_to_index(self, client, sample_activities):
        """
        Test that following the redirect from / leads to index.html.
        
        Arrange: Initialize TestClient
        Act: Make GET request with redirect following
        Assert: Verify we reach the static file
        """
        # Arrange
        # (client and sample_activities from fixtures)
        
        # Act
        response = client.get("/", follow_redirects=True)
        
        # Assert
        assert response.status_code == 200


class TestActivitiesEndpoint:
    """Tests for the GET /activities endpoint."""

    def test_get_all_activities_returns_200(self, client, sample_activities):
        """
        Test that GET /activities returns a successful response.
        
        Arrange: Initialize TestClient
        Act: Make GET request to /activities
        Assert: Verify status code is 200
        """
        # Arrange
        # (client and sample_activities from fixtures)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200

    def test_get_all_activities_returns_dict(self, client, sample_activities):
        """
        Test that GET /activities returns a dictionary of activities.
        
        Arrange: Initialize TestClient
        Act: Make GET request and parse JSON response
        Assert: Verify response is a dict with activities
        """
        # Arrange
        # (client and sample_activities from fixtures)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert isinstance(activities, dict)
        assert len(activities) > 0

    def test_get_activities_contains_known_activity(self, client, sample_activities):
        """
        Test that the activities response contains expected activities.
        
        Arrange: Initialize TestClient
        Act: Make GET request and check for specific activity
        Assert: Verify "Chess Club" is in response
        """
        # Arrange
        expected_activity = "Chess Club"
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert expected_activity in activities

    def test_get_activities_contains_all_fields(self, client, sample_activities):
        """
        Test that each activity has all required fields.
        
        Arrange: Initialize TestClient
        Act: Make GET request and examine an activity structure
        Assert: Verify all required fields are present
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        first_activity = activities["Chess Club"]
        
        # Assert
        assert all(field in first_activity for field in required_fields)

    def test_get_activities_participants_are_list(self, client, sample_activities):
        """
        Test that participants field is a list of email strings.
        
        Arrange: Initialize TestClient
        Act: Make GET request and examine participants
        Assert: Verify participants is a list with string emails
        """
        # Arrange
        # (client and sample_activities from fixtures)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        participants = activities["Chess Club"]["participants"]
        
        # Assert
        assert isinstance(participants, list)
        assert len(participants) > 0
        assert all(isinstance(p, str) for p in participants)


class TestSignupEndpoint:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_new_student_success(self, client, sample_activities):
        """
        Test successful signup of a new student to an activity.
        
        Arrange: Prepare new student email and activity name
        Act: Make POST request with valid activity and new email
        Assert: Verify status 200 and success message
        """
        # Arrange
        activity_name = "Chess Club"
        new_student = "newstudent123@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_student}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert new_student in response.json()["message"]

    def test_signup_student_appears_in_participants(self, client, sample_activities):
        """
        Test that a newly signed up student appears in the participants list.
        
        Arrange: Prepare new student email
        Act: Sign up student and fetch activities list
        Assert: Verify student is now in participants
        """
        # Arrange
        activity_name = "Programming Class"
        new_student = "alice@mergington.edu"
        
        # Act
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_student}
        )
        activities_response = client.get("/activities")
        activities = activities_response.json()
        
        # Assert
        assert signup_response.status_code == 200
        assert new_student in activities[activity_name]["participants"]

    def test_signup_nonexistent_activity_returns_404(self, client, sample_activities):
        """
        Test that signup to a non-existent activity returns 404.
        
        Arrange: Prepare fake activity name and valid email
        Act: Make POST request with invalid activity name
        Assert: Verify status 404 and "not found" message
        """
        # Arrange
        fake_activity = "Fake Activity That Doesnt Exist"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{fake_activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_signup_duplicate_student_returns_400(self, client, sample_activities):
        """
        Test that duplicate signup attempt returns 400.
        
        Arrange: Get an already-registered student
        Act: Make POST request with existing participant email
        Assert: Verify status 400 and duplicate signup message
        """
        # Arrange
        activity_name = "Soccer League"
        existing_student = "lucas@mergington.edu"  # Already signed up
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_student}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()

    def test_signup_increment_participant_count(self, client, sample_activities):
        """
        Test that signup increments the participant count.
        
        Arrange: Get initial participant count
        Act: Sign up new student and check updated count
        Assert: Verify participant count increased by 1
        """
        # Arrange
        activity_name = "Gym Class"
        new_student = "bobsmith@mergington.edu"
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_student}
        )
        updated_response = client.get("/activities")
        updated_count = len(updated_response.json()[activity_name]["participants"])
        
        # Assert
        assert signup_response.status_code == 200
        assert updated_count == initial_count + 1

    def test_signup_multiple_students_same_activity(self, client, sample_activities):
        """
        Test that multiple different students can sign up for same activity.
        
        Arrange: Prepare two new student emails
        Act: Sign up both students sequentially
        Assert: Verify both are successfully added
        """
        # Arrange
        activity_name = "Art Studio"
        student1 = "artist1@mergington.edu"
        student2 = "artist2@mergington.edu"
        
        # Act
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student1}
        )
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student2}
        )
        
        final_response = client.get("/activities")
        participants = final_response.json()[activity_name]["participants"]
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert student1 in participants
        assert student2 in participants

    def test_signup_empty_email_handling(self, client, sample_activities):
        """
        Test behavior when signup is attempted with empty email.
        
        Arrange: Prepare activity name with empty email
        Act: Make POST request with empty email parameter
        Assert: Verify response (can be handled as empty string)
        """
        # Arrange
        activity_name = "Debate Team"
        empty_email = ""
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": empty_email}
        )
        
        # Assert - endpoint should succeed but add empty string to list
        # (This demonstrates a potential edge case to handle)
        assert response.status_code == 200


class TestErrorHandling:
    """Tests for error handling and edge cases."""

    def test_activity_name_with_special_characters(self, client, sample_activities):
        """
        Test signup with activity name containing special characters.
        
        Arrange: Use URL-encoded activity name
        Act: Make POST request with special chars in path
        Assert: Verify appropriate error response
        """
        # Arrange
        special_activity = "Chess%20Club%20Advanced"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{special_activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404

    def test_response_content_type_json(self, client, sample_activities):
        """
        Test that responses have correct content type.
        
        Arrange: Initialize TestClient
        Act: Make requests to various endpoints
        Assert: Verify content-type is application/json
        """
        # Arrange
        # (client and sample_activities from fixtures)
        
        # Act
        activities_response = client.get("/activities")
        
        # Assert
        assert "application/json" in activities_response.headers["content-type"]
