from creds import TR
from models.test_case import TestCase

from providers.base_provider import Provider
from lib.connection import Connection


class TRTestCase(TestCase):
    """
    Pre-built fields:

    "title": "My test case (steps)",
    "template_id": 2,
    "type_id": 1,
    "priority_id": 1,
    "estimate": "3m",
    "refs": "TR-1, TR-2",
    """

    def __init__(
        self,
        title,
        description=None,
        priority: str = None,
        template: str = None,
        test_type: str = None,
        estimate: str = None,
        refs: str = None,
    ):
        super().__init__(title, description)

        self.estimate = estimate
        self.priority = priority
        self.template = template
        self.type = test_type
        self.refs = refs


class TRConfiguration:
    """This object stores the configuration for the TestRail which is not siupposed to be changed"""

    def __init__(self, project_id: int, suite_name: str, section: str):
        """
        :param project_id:
        :param suite_name:
        :param section:
        """
        self.project_id: int = project_id
        self.suite_name: str = suite_name
        self.section: str = section
        self.custom_fields = {}


def set_by_name_or_default(source, name: str = None):
    """
    This method sets the entity by name or default

    :param name: str - name of the entity
    :param entity: dict - entity to be set
    :return: dict - entity
    """

    if name is None:
        for ent in source:
            if ent["is_default"]:
                return ent["id"]
            else:
                continue
    else:
        for ent in source:
            if ent["name"] == name:
                return ent["id"]


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
        ),
    ):
        self.connection = Connection(
            url="https://pluto.testrail.io/index.php?/api/v2/", credentials=credentials
        )
        self.configuration = configuration
        # TODO: Generate by the response
        self.case_fields = {}

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
        """
        Get section id by name

        :return: section id
        """
        for sec in self.connection.http(
            "GET",
            f"get_sections/{self.configuration.project_id}&suite_id={self._get_suite()}",
        ).json()["sections"]:

            if sec["name"] == self.configuration.section:
                return sec["id"]

    def _get_case_type_by_name(self, test_type: TRTestCase = None):
        """
        This method gets the case type by name
        :param test_type: if None, the default type will be returned
        :return: ID of the case type
        """
        return set_by_name_or_default(
            source=self.connection.http("GET", f"get_case_types").json(), name=test_type
        )

    def _get_priority_by_name(self, priority: TRTestCase = None):
        """
        This method gets the priority by name
        :param priority: if None, the default type will be returned
        :return: ID of the priority
        """
        return set_by_name_or_default(
            source=self.connection.http("GET", f"get_priorities").json(), name=priority
        )

    def _get_template_by_name(self, template: TRTestCase = None):
        """
        This method gets the template by name
        :param template: if None, the default type will be returned
        :return: ID of the template
        """
        return set_by_name_or_default(
            source=self.connection.http(
                "GET", f"get_templates/{self.configuration.project_id}"
            ).json(),
            name=template,
        )

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

        self.configuration.custom_fields = [
            case_fields[labels.index(field)]["system_name"]
            for field in fields
            if field in labels
        ]

    def create_case(self, test_case: TRTestCase):
        # TODO: Add the check for existing case (if the same name exists)
        # TODO: Add the object to update the case (if created)
        # TODO: Rename the method to CASE (low priority)

        # Create case: "https://support.testrail.com/hc/en-us/articles/15760060756116-Creating-test-cases#creating-test-cases-with-test-case-steps-template-0-1"

        payload = {
            "title": test_case.title,
            "template_id": self._get_template_by_name(test_case.template),
            "type_id": self._get_case_type_by_name(test_case.type),
            "priority_id": self._get_priority_by_name(test_case.priority),
            "estimate": test_case.estimate,
            "refs": test_case.refs,
        }

        # TODO: Move a level down, before the uploading test case

        # Add custom fields to payload
        for custom_field in self.configuration.custom_fields:
            payload[custom_field] = ""

        return self.connection.http(
            "POST", f"add_case/{self._get_section()}", json=payload
        ).json()


if __name__ == "__main__":
    tr = TestRail()
    # TODO: fetch from .yaml config for TR (high priority)
    tr.construct_custom_fields(["Preconditions", "Test Steps", "Expected Results"])

    tc = TRTestCase(
        title="My test case (steps)",
        template="Test Case (Steps)",
        test_type="Functional",
        priority="High",
        estimate="3m",
        refs="TR-1, TR-2",
    )

    tc.add_step("Click on the button", "Page should be redirected to the new page")
    tc.add_step("B", "Second step")

    tr.create_case(tc)

    # a = tr._get_template_by_name("Test Case (Steps)")
    b = 1
