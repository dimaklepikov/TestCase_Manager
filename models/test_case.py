""""""


class TestCase:
    # TODO: Add mutual interface for all providers

    def __init__(self, title, description, **kwargs):
        self.title = title
        self.description = description

        # TBD - section exists in testrail
        self.section = kwargs.get("section", "")
        self.preconditions = kwargs.get("preconditions", "")
        # Holder for steps
        self.steps = {}

    def __str__(self):
        return f"Test case: {self.title}"

    def add_preconditions(self, preconditions: str):
        # TBD: the way to use it
        """
        Preconditions are used to define the state of the system before the test case is executed.

        In Pytest, fixutres are reponsible for the preconditions.

        TODO: Research other test runners / frameworks on the pre-condition support

        :param preconditions:
        :return:
        """
        ...

    def add_step(self, step_number: int, step: str, expected_result: str):
        step_number = str(step_number)
        self.steps.update(
            {
                "description": f"{step_number}{step}",
                "expected_result": f"{step_number}{expected_result}",
            }
        )
