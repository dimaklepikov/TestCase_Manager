from creds import TR
from models.test_case import TestCase

from providers.base_provider import Provider
from lib.connection import Connection


class TestRail(Provider):
    # TODO: Add TestRail specific methods
    # TODO: Add id/name dispatching during initiation (high priority)
    # TODO: Add async support (low priority)

    def __init__(self, credentials: dict = TR):
        self.connection = Connection(
            url="https://pluto.testrail.io/index.php?/api/v2/",
            credentials=credentials
        )
        self.project_id: int = 3
        self.suite_name: str = "[TestCaseManager] Mock"
        self.section: str = "Test Section"

    def _get_suite(self):
        # TODO: ADD check by ID (Add for provider class)
        # TODO: Add suit creation feature (low priority)
        for suite in self.connection.http("GET", f"get_suites/{self.project_id}").json():
            if suite["name"] == self.suite_name:
                return suite["id"]
        return None

    def _get_section(self):
        for sec in self.connection.http(
                "GET",
                f"get_sections/{self.project_id}&suite_id={self._get_suite()}"
        ).json()["sections"]:
            if sec["name"] == self.section:
                return sec["id"]

    def create_case(self, test_case: TestCase):
        # TODO: Add object creation from TestCase instance
        # TODO: Add the check for existing case (if the same name exists)
        # TODO: Add the object to update the case (if created)
        # TODO: Rename the method to CASE (low priority)
        payload = {
            "title": test_case.title
        }

        return self.connection.http("POST", f"add_case/{self._get_section()}", json=payload).json()


if __name__ == "__main__":
    tr = TestRail()
    a = tr.create_case(TestCase("Test", "Test description"))
    b = 1
