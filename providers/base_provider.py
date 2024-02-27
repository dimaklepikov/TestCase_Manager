"""Base module for all providers"""


class Provider:
    """Base class for all providers"""

    def __get_project_by_name(self, project_name):
        """Get project by name

        Args:
            project_name: Project name

        Returns:
            Project object
        """
        ...

    def test_case(self):
        # TODO: Add check for existing test case
        # TODO: Create test case if not exists
        ...
