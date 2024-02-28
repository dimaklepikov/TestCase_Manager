from models.test_case import TestCase
from wrappers import testrail

"""
This file aims to implement the test case of Pytest test case creation and uploading to TR

TODO:
- Add tests with pure python
- Enhance other framework support
- Implement generation from code's content (low priority)
"""


def test_case_creation():
    test_case = TestCase("Test", "Test description")
    with testrail as tr:
        tr.create_case(test_case)
