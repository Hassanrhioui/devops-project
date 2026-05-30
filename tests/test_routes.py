import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200


def test_home_returns_html(client):
    response = client.get('/')
    assert b'Hassan' in response.data


def test_health_check_returns_200(client):
    response = client.get('/health')
    assert response.status_code == 200


def test_health_check_has_status(client):
    response = client.get('/health')
    data = response.get_json()
    assert data['status'] == 'healthy'


def test_health_check_has_uptime(client):
    response = client.get('/health')
    data = response.get_json()
    assert 'uptime' in data


def test_status_endpoint(client):
    response = client.get('/status')
    assert response.status_code == 200
    data = response.get_json()
    assert data['ok'] is True