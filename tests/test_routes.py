import pytest
from app import create_app


@pytest.fixture
def client():
    """
    Creates a test client for the Flask app.
    The test client simulates HTTP requests without
    running a real server.
    """
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_returns_200(client):
    """Test that the home endpoint returns HTTP 200."""
    response = client.get('/')
    assert response.status_code == 200


def test_home_returns_json(client):
    """Test that the home endpoint returns valid JSON."""
    response = client.get('/')
    data = response.get_json()
    assert data['status'] == 'running'


def test_health_check_returns_200(client):
    """Test that the health endpoint returns HTTP 200."""
    response = client.get('/health')
    assert response.status_code == 200


def test_health_check_status_healthy(client):
    """Test that the health endpoint reports healthy status."""
    response = client.get('/health')
    data = response.get_json()
    assert data['status'] == 'healthy'