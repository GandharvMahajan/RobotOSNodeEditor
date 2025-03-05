#!/usr/bin/env python3
# Test runner for the PysideNodeApp application
import unittest
import sys
from PySide6.QtWidgets import QApplication

# Create QApplication instance for the tests
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

# Import test modules
from tests.test_base_node import TestBaseNode
from tests.test_port import TestPort
from tests.test_connection import TestConnection
from tests.test_scene import TestNodeScene
from tests.test_view import TestNodeView
from tests.test_specific_nodes import TestSpecificNodes
from tests.test_run_stop_button import TestRunStopButton

def run_tests():
    """Run all tests and return the result"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestBaseNode))
    test_suite.addTest(unittest.makeSuite(TestPort))
    test_suite.addTest(unittest.makeSuite(TestConnection))
    test_suite.addTest(unittest.makeSuite(TestNodeScene))
    test_suite.addTest(unittest.makeSuite(TestNodeView))
    test_suite.addTest(unittest.makeSuite(TestSpecificNodes))
    test_suite.addTest(unittest.makeSuite(TestRunStopButton))
    
    # Run tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    return result

if __name__ == '__main__':
    result = run_tests()
    
    # Exit with appropriate code
    sys.exit(not result.wasSuccessful()) 