from creds import TR
from models.test_case import TestCase

from providers.base_provider import Provider
from lib.connection import Connection


class TRConfiguration:
    """This object stores the configuration for the TestRail which is not siupposed to be changed"""

    def __init__(self, project_id: int, suite_name: str, section: str):
        """
        Required fields
            "title": "My test case (steps)",
            "template_id": 2,
            "type_id": 1,
            "priority_id": 1,
            "estimate": "3m",
            "refs": "TR-1, TR-2",
        :param project_id:
        :param suite_name:
        :param section:
        """
        self.project_id: int = project_id
        self.suite_name: str = suite_name
        self.section: str = section
        self.custom_fields = {}


class TestRail(Provider):
    # TODO: Implement persistent checks on id's of created entities by code (Sqllite) (high priority)
    # TODO: Add id/name dispatching during initiation (high priority)
    # TODO: Add TestRail specific methods
    # TODO: Add async calls support (low priority)

    def __init__(
            self,
            credentials: dict = TR,
            configuration: TRConfiguration = TRConfiguration(
                project_id=3, suite_name="[TestCaseManager] Mock", section="Test Section"
            )
    ):
        self.connection = Connection(
            url="https://pluto.testrail.io/index.php?/api/v2/", credentials=credentials
        )
        self.configuration = configuration
        # TODO: Generate by the response
        self.case_fields = {}

        self.test_case = TestCase("Test", "Test description")

    def _get_suite(self):
        # TODO: ADD check by ID (Add for provider class)
        # TODO: Add suit creation feature (low priority)
        for suite in self.connection.http(
                "GET", f"get_suites/{self.configuration.project_id}"
        ).json():
            if suite["name"] == self.configuration.suite_name:
                return suite["id"]
        return None

    def _get_section(self):
        for sec in self.connection.http(
                "GET",
                f"get_sections/{self.configuration.project_id}&suite_id={self._get_suite()}"
        ).json()["sections"]:

            if sec["name"] == self.configuration.section:
                return sec["id"]

    def create_case(self, test_case: TestCase):
        # TODO: Add object creation from TestCase instance
        # TODO: Add the check for existing case (if the same name exists)
        # TODO: Add the object to update the case (if created)
        # TODO: Rename the method to CASE (low priority)

        # Create case: "https://support.testrail.com/hc/en-us/articles/15760060756116-Creating-test-cases#creating-test-cases-with-test-case-steps-template-0-1"

        payload = {"title": test_case.title}

        return self.connection.http(
            "POST", f"add_case/{self._get_section()}", json=payload
        ).json()

    # def get_case_fields(self):
    #     return self.connection.http(
    #         "GET", f"get_case_fields"
    #     ).json()

    def construct_custom_fields(self, fields: list = None) -> dict:
        """
        This method constructs the custom fields for the test case

        :arg fields: list - list of fields (equal to UI TR names to be added to the test case)

        TBD:
        :return: dict - custom fields for the TR test case
        """
        # Define the labels (real names) list of TR custom fields
        case_fields = self.connection.http("GET", f"get_case_fields").json()

        labels = [case["label"] for case in case_fields]

        self.configuration.custom_fields = {
            field: case_fields[labels.index(field)]["system_name"]
            for field in fields
            if field in labels
        }
        # return {
        #     field: case_fields[labels.index(field)]["system_name"]
        #     for field in fields
        #     if field in labels
        # }


if __name__ == "__main__":
    tr = TestRail()
    a = tr.construct_custom_fields(["Preconditions", "Automation Type"])
    # a = tr.create_case(TestCase("Test", "Test description"))
    b = 1
