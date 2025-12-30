import pytest
from app import app as flask_app

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the /health endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'status': 'healthy'}

def test_is_palindrome_positive(client):
    """Test with a number that is a palindrome."""
    response = client.get('/is_palindrome/12321')
    assert response.status_code == 200
    assert response.json == {
        'number': 12321,
        'is_palindrome': True,
        'status': 'success'
    }

def test_is_palindrome_negative(client):
    """Test with a number that is not a palindrome."""
    response = client.get('/is_palindrome/12345')
    assert response.status_code == 200
    assert response.json == {
        'number': 12345,
        'is_palindrome': False,
        'status': 'success'
    }

def test_is_palindrome_single_digit(client):
    """Test with a single digit number."""
    response = client.get('/is_palindrome/7')
    assert response.status_code == 200
    assert response.json['is_palindrome'] is True

def test_is_palindrome_with_zero(client):
    """Test with zero."""
    response = client.get('/is_palindrome/0')
    assert response.status_code == 200
    assert response.json['is_palindrome'] is True

def test_404_not_found(client):
    """Test a route that does not exist."""
    response = client.get('/nonexistent-route')
    assert response.status_code == 404
    assert response.json == {'error': 'Not Found'}
