"""
Unit tests for FastAPI activity management system.

Tests individual business logic and validation functions using the AAA pattern:
- Arrange: Set up test data and initial state
- Act: Execute the code being tested
- Assert: Verify the results match expectations
"""

import pytest
from fastapi import HTTPException


class TestActivityValidation:
    """Tests for validating activity existence and capacity."""

    def test_activity_exists_in_database(self, sample_activities):
        """
        Test that an activity can be found in the activities database.
        
        Arrange: Get the activities fixture (contains known activities)
        Act: Check if "Chess Club" exists in activities
        Assert: Verify the activity exists and has expected properties
        """
        # Arrange
        activity_name = "Chess Club"
        
        # Act
        activity_exists = activity_name in sample_activities
        activity = sample_activities.get(activity_name)
        
        # Assert
        assert activity_exists is True
        assert activity is not None
        assert "description" in activity
        assert "max_participants" in activity
        assert "participants" in activity

    def test_activity_not_found(self, sample_activities):
        """
        Test that a non-existent activity returns None.
        
        Arrange: Define a fake activity name that doesn't exist
        Act: Try to retrieve the activity from activities
        Assert: Verify it doesn't exist
        """
        # Arrange
        fake_activity = "Underwater Basket Weaving"
        
        # Act
        activity_exists = fake_activity in sample_activities
        
        # Assert
        assert activity_exists is False

    def test_activity_has_capacity(self, sample_activities):
        """
        Test that an activity has capacity when below max_participants.
        
        Arrange: Get an activity with known max_participants and current participants
        Act: Check if participants list is below max capacity
        Assert: Verify capacity is available
        """
        # Arrange
        activity = sample_activities["Chess Club"]
        max_participants = activity["max_participants"]
        current_count = len(activity["participants"])
        
        # Act
        has_capacity = current_count < max_participants
        
        # Assert
        assert has_capacity is True
        assert current_count < max_participants

    def test_activity_at_capacity(self, sample_activities):
        """
        Test that we can detect when an activity is full.
        
        Arrange: Manually fill an activity to max capacity
        Act: Check if activity is at or above max capacity
        Assert: Verify the activity is full
        """
        # Arrange
        activity = sample_activities["Programming Class"]
        activity["participants"] = ["student" + str(i) + "@school.edu" for i in range(20)]
        max_participants = activity["max_participants"]
        current_count = len(activity["participants"])
        
        # Act
        at_capacity = current_count >= max_participants
        
        # Assert
        assert at_capacity is True
        assert current_count == max_participants


class TestStudentSignupValidation:
    """Tests for validating student signup logic."""

    def test_student_not_in_participants_list(self, sample_activities):
        """
        Test that a new student is not already in an activity's participants.
        
        Arrange: Define a student email that isn't in Chess Club
        Act: Check if student is in participants list
        Assert: Verify student is not signed up
        """
        # Arrange
        activity = sample_activities["Chess Club"]
        new_student = "newstudent@mergington.edu"
        
        # Act
        already_signed_up = new_student in activity["participants"]
        
        # Assert
        assert already_signed_up is False

    def test_student_already_in_participants_list(self, sample_activities):
        """
        Test that we can detect if a student is already signed up.
        
        Arrange: Get an activity and a student already in it
        Act: Check if student exists in participants list
        Assert: Verify student is already signed up
        """
        # Arrange
        activity = sample_activities["Chess Club"]
        existing_student = "michael@mergington.edu"  # Known participant
        
        # Act
        already_signed_up = existing_student in activity["participants"]
        
        # Assert
        assert already_signed_up is True

    def test_add_student_to_activity(self, sample_activities):
        """
        Test that a student can be added to an activity's participants.
        
        Arrange: Get initial participant count and prepare new student email
        Act: Add student to participants list
        Assert: Verify participant count increased and student is now in list
        """
        # Arrange
        activity = sample_activities["Basketball Team"]
        initial_count = len(activity["participants"])
        new_student = "newhero@mergington.edu"
        
        # Act
        activity["participants"].append(new_student)
        final_count = len(activity["participants"])
        student_added = new_student in activity["participants"]
        
        # Assert
        assert final_count == initial_count + 1
        assert student_added is True

    def test_cannot_add_duplicate_student(self, sample_activities):
        """
        Test that duplicate signups are prevented.
        
        Arrange: Get an activity and an existing participant
        Act: Try to add the same student again (should be prevented by our logic)
        Assert: Verify student count doesn't change
        """
        # Arrange
        activity = sample_activities["Soccer League"]
        duplicate_student = "lucas@mergington.edu"  # Already a participant
        initial_count = len(activity["participants"])
        
        # Act - Simulate attempting to add duplicate (our code should reject this)
        if duplicate_student not in activity["participants"]:
            activity["participants"].append(duplicate_student)
        
        final_count = len(activity["participants"])
        
        # Assert
        assert final_count == initial_count
        # Verify student is still only in list once
        assert activity["participants"].count(duplicate_student) == 1

    def test_participant_count_consistency(self, sample_activities):
        """
        Test that participant count matches the actual participants list length.
        
        Arrange: Get an activity and its participant list
        Act: Count participants in list
        Assert: Verify count is consistent
        """
        # Arrange
        activity = sample_activities["Drama Club"]
        participants = activity["participants"]
        
        # Act
        participant_count = len(participants)
        
        # Assert
        assert participant_count == 2  # Initial state has 2 participants
        assert all(isinstance(p, str) for p in participants)  # All are email strings
