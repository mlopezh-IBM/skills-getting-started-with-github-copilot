"""
Pytest configuration and shared fixtures for FastAPI tests.

Fixtures provided:
- client: TestClient instance for making requests to the FastAPI app
- sample_activities: Fixture that resets activities to initial state before each test
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """
    Fixture: Provides a TestClient instance for testing the FastAPI app.
    
    Arrange: Initialize the TestClient with the FastAPI app instance.
    """
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """
    Fixture: Resets activities to initial state before each test.
    
    Arrange: Clear any modifications to activities and restore original data.
    This ensures tests are isolated and don't affect each other.
    """
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team for intramural and tournament play",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu", "isabella@mergington.edu"]
        },
        "Soccer League": {
            "description": "Join the soccer league and compete against other schools",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["lucas@mergington.edu", "ava@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and mixed media techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["grace@mergington.edu", "noah@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in theatrical productions and develop acting skills",
            "schedule": "Tuesdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["chloe@mergington.edu", "ethan@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation and public speaking skills through competitive debate",
            "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["mia@mergington.edu", "jackson@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore various scientific disciplines",
            "schedule": "Wednesdays and Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 18,
            "participants": ["harper@mergington.edu", "alexander@mergington.edu"]
        }
    }
    
    # Clear existing activities and restore original state
    activities.clear()
    activities.update(original_activities)
    
    # Yield for test execution
    yield activities
    
    # Cleanup: Reset activities after test completes
    activities.clear()
    activities.update(original_activities)
