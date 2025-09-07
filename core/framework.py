from typing import Optional, List, Dict, Any
import time
import inspect


class Framework:

    def __init__(self):
        self.tests = []
        self.groups = {}
        self.results = []
        self.environment = {}

    def set_environment(self, env_config: Dict[str, Any]):
        """Set the environment configuration."""
        self.environment = env_config

    def test(self, name: Optional[str]):
        def decorator(func):
            test_name = name or func.__name__
            group_name = getattr(func, '_group', 'Ungrouped')

            test_case = {
                'name': test_name,
                'function': func,
                'group': group_name,
                'skipped': getattr(func, '_skip', False)
            }
            self.tests.append(test_case)
            if group_name not in self.groups:
                self.groups[group_name] = []
            self.groups[group_name].append(test_case)

            return func
        return decorator

    def group(self, name: str):
        """Decorator to associate a test with a group."""
        def decorator(func):
            func._group = name
            return func
        return decorator

    def skip(self, func):
        """Decorator to skip a test."""
        func._skip = True
        return func

    def run_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single test case."""
        start_time = time.time()
        result = {
            'name': test_case['name'],
            'group': test_case['group'],
            'status': 'pending',
            'execution_time': 0,
            'error': None,
            'response': None
        }

        try:
            if test_case['skipped']:
                result['status'] = 'skipped'
            else:
                # Execute the test function with environment
                test_func = test_case['function']
                sig = inspect.signature(test_func)

                # Pass environment if the function expects it
                if 'env' in sig.parameters:
                    test_func(self.environment)
                else:
                    test_func()

                result['status'] = 'passed'
        except Exception as e:
            result['status'] = 'failed'
            result['error'] = str(e)
        finally:
            end_time = time.time()
            result['execution_time'] = round((end_time - start_time) * 1000, 2)  # in milliseconds

        return result

    def run_tests(self, test_names: List[str] = []) -> List[Dict[str, Any]]:
        """Run specified tests or all tests if none specified."""
        results = []

        # Filter tests if specific names provided
        tests_to_run = self.tests
        if test_names:
            tests_to_run = [t for t in self.tests if t['name'] in test_names]

        for test_case in tests_to_run:
            result = self.run_test(test_case)
            results.append(result)
            self.results.append(result)

        return results

    def run_group(self, group_name: str) -> List[Dict[str, Any]]:
        """Run all tests in a group."""
        if group_name in self.groups:
            results = []
            for test_case in self.groups[group_name]:
                result = self.run_test(test_case)
                results.append(result)
                self.results.append(result)
            return results
        else:
            raise ValueError(f"Group '{group_name}' not found")

    def get_all_tests(self) -> List[Dict[str, Any]]:
        """Get all registered tests."""
        return self.tests

    def get_groups(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all groups with their tests."""
        return self.groups

    def get_results(self) -> List[Dict[str, Any]]:
        """Get all test results."""
        return self.results

    def clear_results(self):
        """Clear all test results."""
        self.results = []



test_framework = Framework()

test = test_framework.test
group = test_framework.group
skip = test_framework.skip
