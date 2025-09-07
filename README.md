# py-qa

A Python-based test execution framework with a web interface for organizing and running API tests.

## Overview

py-qa is a web-based testing framework that allows you to define, organize, and execute tests through an intuitive web UI. It's particularly useful for API testing with support for different environments (development, staging, production, etc.).

Key features:
- Web-based interface for test selection and execution
- Test organization by groups
- Environment configuration management
- Real-time test execution results
- Dark/light theme toggle

## Project Structure

```
py-qa/
├── main.py              # Application entry point
├── core/                # Core framework components
│   ├── framework.py     # Test definition and execution framework
│   └── runner.py        # Test runner with environment management
├── ui/                  # Web interface components
│   ├── app.py           # Flask application
│   ├── templates/       # HTML templates
│   └── static/          # Static assets (CSS, JS, images)
├── configs/             # Configuration files
│   └── environments.json # Environment configurations
├── tests/               # Test definitions
│   └── sample_tests.py  # Example test cases
└── requirements.txt     # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd py-qa
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the Flask application:
   ```bash
   python main.py
   ```

2. Open your web browser and navigate to `http://localhost:5000`

## Writing Tests

Tests are defined using decorators from the core framework. Here's an example:

```python
from core.framework import test, group

@test('Should perform GET request')
@group('HTTP Methods')
def test_get_request(env):
    """Test GET request to httpbin."""
    url = f"{env['baseUrl']}/get"
    response = requests.get(url, timeout=env.get('timeout', 30))
    assert response.status_code == 200
```

Key decorators:
- `@test(name)`: Registers a function as a test case
- `@group(name)`: Associates a test with a group
- `@skip`: Marks a test to be skipped during execution

Test functions can optionally accept an `env` parameter to access environment configurations defined in `configs/environments.json`.

## Environments

Environment configurations are defined in `configs/environments.json`. You can add, modify, or remove environments as needed:

```json
{
  "development": {
    "baseUrl": "https://httpbin.org",
    "timeout": 30
  },
  "staging": {
    "baseUrl": "https://httpbin.org",
    "timeout": 30
  }
}
```

## Web Interface

The web interface provides:
1. Test organization by groups with expandable sections
2. Checkbox selection for individual tests or entire groups
3. Environment selection dropdown
4. Dark/light theme toggle
5. Real-time test execution results

To run tests:
1. Select the desired environment
2. Check the tests or groups you want to run
3. Click "Run Selected Tests"

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.