# Project Context for py-qa

This document provides an overview of the py-qa project structure and key components to help Qwen Code understand the codebase for future interactions.

## Project Type

This is a Python code project that implements a web-based test runner framework using Flask. It allows users to define, organize, and execute tests through a web UI, with support for different environments.

## Project Overview

The py-qa project is a Python-based test execution framework with a web interface. Key features include:

1.  A core testing framework (`core/framework.py`) for defining and running tests using decorators
2.  A test runner (`core/runner.py`) that manages environments and executes tests
3.  A Flask-based web UI (`ui/app.py`) for selecting and running tests
4.  Support for grouping tests and skipping tests
5.  Environment configuration management via JSON files
6.  Real-time test execution with Server-Sent Events (SSE)

## Key Components

### Core Framework (`core/framework.py`)

*   **Framework Class**: The central class that manages test registration, execution, and results
*   **Decorators**:
    *   `@test(name)`: Registers a function as a test case
    *   `@group(name)`: Associates a test with a group
    *   `@skip`: Marks a test to be skipped during execution
*   **Test Execution**: Handles running individual tests or groups of tests, with error handling and timing

### Test Runner (`core/runner.py`)

*   **TestRunner Class**: Manages environment configurations and coordinates test execution
*   **Environment Management**: Loads environments from JSON/YAML files and sets the current environment for tests
*   **Test Execution Methods**: Provides methods to run all tests, specific tests, or groups of tests

### Web UI (`ui/app.py`)

*   **Flask Application**: The main web server that serves the UI and handles test execution requests
*   **Routes**:
    *   `/`: Displays the main test selection page
    *   `/run-tests`: Handles form submission for test execution
    *   `/start-test-execution`: Initiates test execution and returns an execution ID
    *   `/execute-tests/<execution_id>`: Streams test execution results using SSE
*   **Templates**: Uses Jinja2 templates for rendering HTML (in `ui/templates/`)

### Configuration (`configs/environments.json`)

*   Defines different environments (development, staging, production, qa) with their respective configurations (baseUrl, timeout)

### Tests (`tests/`)

*   Contains test definitions, with sample tests in `tests/sample_tests.py`
*   Tests are defined using the framework's decorators and can access environment configurations

## Building and Running

1.  Install dependencies (assuming Python 3.x is installed):
    *   Flask
    *   requests
    *   PyYAML (for YAML support in test runner)
    ```bash
    pip install flask requests pyyaml
    ```
2.  Run the application:
    ```bash
    python main.py
    ```
3.  Access the web UI at `http://localhost:5000`

## Development Conventions

*   Tests are defined using decorators from the core framework
*   Test functions can optionally accept an `env` parameter to access environment configurations
*   Tests are organized into groups for better management
*   Environment configurations are stored in JSON files
*   The web UI uses Tailwind CSS for styling