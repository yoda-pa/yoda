from unittest import TestCase
from click.testing import CliRunner

import yoda


# noinspection PyUnusedLocal
class TestAlias(TestCase):
    """
        Test for the following commands:

        | Module: alias
        | Command: alias
    """

    def __init__(self, methodName="runTest"):
        super(TestAlias, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        result = self.runner.invoke(
            yoda.cli,
            ["alias"]
        )
        self.assertEqual(result.exit_code, 0)

        # Invalid alias
        result = self.runner.invoke(
            yoda.cli,
            ["alias", "new", "", ""],
        )
        self.assertIn("Aliasing failed - Invalid alias", result.output)

        result = self.runner.invoke(
            yoda.cli,
            ["alias", "new", "", "a"],
        )
        self.assertIn("Aliasing failed - Invalid command to alias", result.output)

        result = self.runner.invoke(
            yoda.cli,
            ["alias", "new", "alias", "a"],
        )
        self.assertIn("Aliasing failed - Cannot alias the alias command", result.output)

        result = self.runner.invoke(
            yoda.cli,
            ["alias", "new", "a", "a b"],
        )
        self.assertIn("Aliasing failed - Alias must not contain spaces", result.output)

        # New alias
        result = self.runner.invoke(
            yoda.cli,
            ["alias", "new", "a", "a"],
        )
        self.assertIn("Aliased a as a", result.output)

        # Try to create the same alias again
        result = self.runner.invoke(
            yoda.cli,
            ["alias", "new", "a", "a"],
        )
        self.assertIn("Aliasing failed - Alias name already exists. Use alias delete to remove it", result.output)

        # Alias show
        result = self.runner.invoke(
            yoda.cli,
            ["alias", "show"]
        )
        self.assertEqual(result.exit_code, 0)

        # Delete the 'a' alias
        result = self.runner.invoke(
            yoda.cli,
            ["alias", "delete", "a"]
        )
        self.assertEqual(result.exit_code, 0)

        # Try to delete it again
        result = self.runner.invoke(
            yoda.cli,
            ["alias", "delete", "a"]
        )
        self.assertIn("Alias delete failed - Could not find alias", result.output)
