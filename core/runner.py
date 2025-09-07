"""
Test runner module to execute tests and handle environments.
"""
import json
import yaml
from typing import Dict, Any
from core.framework import test_framework


class TestRunner:
    """Test runner to execute tests and manage environments."""
    
    def __init__(self):
        self.environments = {}
    
    def load_environments(self, config_file: str):
        """Load environment configurations from JSON or YAML file."""
        try:
            with open(config_file, 'r') as f:
                if config_file.endswith('.json'):
                    self.environments = json.load(f)
                elif config_file.endswith(('.yml', '.yaml')):
                    self.environments = yaml.safe_load(f)
                else:
                    raise ValueError("Unsupported configuration file format")
        except FileNotFoundError:
            print(f"Configuration file {config_file} not found. Using empty environments.")
            self.environments = {}
    
    def get_environments(self) -> Dict[str, Any]:
        """Get all available environments."""
        return self.environments
    
    def set_environment(self, env_name: str):
        """Set the current environment for test execution."""
        if env_name in self.environments:
            test_framework.set_environment(self.environments[env_name])
            return True
        return False
    
    def run_all_tests(self):
        """Run all registered tests."""
        return test_framework.run_tests()
    
    def run_test_by_name(self, test_name: str):
        """Run a specific test by name."""
        return test_framework.run_tests([test_name])
    
    def run_group(self, group_name: str):
        """Run all tests in a group."""
        return test_framework.run_group(group_name)
    
    def get_test_summary(self):
        """Get a summary of test execution results."""
        results = test_framework.get_results()
        summary = {
            'total': len(results),
            'passed': len([r for r in results if r['status'] == 'passed']),
            'failed': len([r for r in results if r['status'] == 'failed']),
            'skipped': len([r for r in results if r['status'] == 'skipped']),
            'pending': len([r for r in results if r['status'] == 'pending'])
        }
        return summary


# Create a global instance
test_runner = TestRunner()