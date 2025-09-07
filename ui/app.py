"""Flask Entrypoint"""
from flask import Flask, render_template, request, redirect, url_for, Response
from core.framework import test_framework
from core.runner import test_runner
from tests import *
import json
import time


app = Flask(__name__, template_folder='templates', static_folder='status')
test_runner.load_environments('configs/environments.json')


@app.route("/")
def index():
    tests = test_framework.get_all_tests()
    groups = test_framework.get_groups()
    environments = test_runner.get_environments()
    return render_template("index.html", tests=tests, groups=groups, environments=environments)


@app.route("/run-tests", methods=["POST"])
def run_tests():
    selected_tests = request.form.getlist("selected_tests")
    environment = request.form.get("environment")

    # Set the environment
    test_runner.set_environment(environment)

    # Get test details for display
    all_tests = test_framework.get_all_tests()
    selected_test_details = [test for test in all_tests if test['name'] in selected_tests]

    return render_template("test_execution.html",
                         selected_tests=selected_test_details,
                         environment=environment,
                         total_tests=len(selected_test_details))


# Store test execution data in a global variable (in a real application, you'd use a proper session or database)
test_execution_data = {}

@app.route("/start-test-execution", methods=["POST"])
def start_test_execution():
    selected_tests = request.form.getlist("selected_tests")
    environment = request.form.get("environment")

    # Store the test execution data
    import uuid
    execution_id = str(uuid.uuid4())
    test_execution_data[execution_id] = {
        'selected_tests': selected_tests,
        'environment': environment
    }

    # Return the execution ID
    return json.dumps({'execution_id': execution_id})

@app.route("/execute-tests/<execution_id>")
def execute_tests(execution_id):
    def generate():
        # Check if execution data exists
        if execution_id not in test_execution_data:
            yield 'data: {"error": "Invalid execution ID"}\n\n'
            return

        # Get execution data
        exec_data = test_execution_data[execution_id]
        selected_tests = exec_data['selected_tests']
        environment = exec_data['environment']

        # Set the environment
        test_runner.set_environment(environment)

        # Clear previous results
        test_framework.clear_results()

        # Get all tests
        all_tests = test_framework.get_all_tests()

        # Filter to only selected tests
        tests_to_run = [test for test in all_tests if test['name'] in selected_tests]

        # Run each test and yield results
        for i, test in enumerate(tests_to_run):
            result = test_framework.run_test(test)

            # Yield the result as JSON
            yield f"data: {json.dumps({'index': i, 'result': result})}\n\n"

            # Small delay to simulate real-time execution
            time.sleep(0.5)

        # Send completion signal
        yield 'data: {"completed": true}\n\n'

        # Clean up execution data
        if execution_id in test_execution_data:
            del test_execution_data[execution_id]

    return Response(generate(), mimetype='text/event-stream')
