"""
Sample tests using httpbin for demonstration.
"""
from core.framework import test, group, skip
import requests
import json


@test('Should perform GET request')
@group('HTTP Methods')
def test_get_request(env):
    """Test GET request to httpbin."""
    url = f"{env['baseUrl']}/get"
    response = requests.get(url, timeout=env.get('timeout', 30))
    assert response.status_code == 200
    data = response.json()
    assert 'url' in data


@test('Should perform POST request')
@group('HTTP Methods')
def test_post_request(env):
    """Test POST request to httpbin."""
    url = f"{env['baseUrl']}/post"
    payload = {'key': 'value', 'test': 'data'}
    response = requests.post(url, json=payload, timeout=env.get('timeout', 30))
    assert response.status_code == 200
    data = response.json()
    assert 'json' in data
    assert data['json']['key'] == 'value'


@test('Should perform PUT request')
@group('HTTP Methods')
def test_put_request(env):
    """Test PUT request to httpbin."""
    url = f"{env['baseUrl']}/put"
    payload = {'key': 'updated_value', 'test': 'updated_data'}
    response = requests.put(url, json=payload, timeout=env.get('timeout', 30))
    assert response.status_code == 200
    data = response.json()
    assert 'json' in data
    assert data['json']['key'] == 'updated_value'


@test('Should handle 200 status code')
@group('Status Codes')
def test_status_200(env):
    """Test handling of 200 status code."""
    url = f"{env['baseUrl']}/status/200"
    response = requests.get(url, timeout=env.get('timeout', 30))
    assert response.status_code == 200


@test('Should handle 404 status code')
@group('Status Codes')
def test_status_404(env):
    """Test handling of 404 status code."""
    url = f"{env['baseUrl']}/status/404"
    response = requests.get(url, timeout=env.get('timeout', 30))
    assert response.status_code == 404


@test('Should return request headers')
@group('Request Inspection')
def test_request_headers(env):
    """Test request headers inspection."""
    url = f"{env['baseUrl']}/headers"
    headers = {'X-Test-Header': 'test-value'}
    response = requests.get(url, headers=headers, timeout=env.get('timeout', 30))
    assert response.status_code == 200
    data = response.json()
    assert 'headers' in data
    # Check if our custom header is in the response


@test('Should handle basic auth')
@skip
@group('Authentication')
def test_basic_auth(env):
    """Test basic authentication (skipped for demo)."""
    # This would be skipped in actual execution
    pass


@test('Should return JSON response')
@group('Response Formats')
def test_json_response(env):
    """Test JSON response handling."""
    url = f"{env['baseUrl']}/json"
    response = requests.get(url, timeout=env.get('timeout', 30))
    assert response.status_code == 200
    assert response.headers['Content-Type'].startswith('application/json')
    data = response.json()
    assert 'slideshow' in data


@test('Should return XML response')
@group('Response Formats')
def test_xml_response(env):
    """Test XML response handling."""
    url = f"{env['baseUrl']}/xml"
    response = requests.get(url, timeout=env.get('timeout', 30))
    assert response.status_code == 200
    assert 'xml' in response.headers['Content-Type'] or 'text/xml' in response.headers['Content-Type']


@test('Should handle query parameters')
@group('Query Parameters')
def test_query_parameters(env):
    """Test query parameter handling."""
    url = f"{env['baseUrl']}/get"
    params = {'key1': 'value1', 'key2': 'value2'}
    response = requests.get(url, params=params, timeout=env.get('timeout', 30))
    assert response.status_code == 200
    data = response.json()
    assert 'args' in data
    assert data['args']['key1'] == 'value1'
    assert data['args']['key2'] == 'value2'


if __name__ == "__main__":
    # For direct execution of tests
    print("Sample tests defined. Run through the web UI or test runner.")