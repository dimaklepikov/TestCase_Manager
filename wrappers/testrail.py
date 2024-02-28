"""Testrail context manager"""

from providers.testrail import TestRail

"""
this module aims to provide a context manager for TestRail
to use it for the test case creation from code

TBD: 
- If the CM should wrap method or class? Check the docs

Example of usage:
<<<Pytest>>>

TODO:
- Add the test case creation from the test function / class / module name (parse via inspect, etc...)


tr = TestRail(section="Test class / module name (by default)", suite="Package (by default) / Feature name ", project_id=3...)


tr.case - method should be retrieved from the test function name

with tr.step:
    tr.step("Click on the button", "Page should be redirected to the new page")
    element.click()
    assert new_page.is_displayed()
    
DOD:
After the test fucntion is executed, the  TestCase.create_case should be called with the constructed object

"""


class testrail(TestRail):
    """Testrail wrapper"""

    ...
