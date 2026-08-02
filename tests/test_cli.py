import contextlib
import io
import unittest

from public_agent_system.cli import main


class CliTests(unittest.TestCase):
    def test_list_command(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["list"])
        self.assertEqual(0, code)
        self.assertIn("001  System Orchestrator", output.getvalue())
        self.assertIn("012  Voice and Style Router", output.getvalue())

    def test_unknown_agent(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["show", "999"])
        self.assertEqual(2, code)


if __name__ == "__main__":
    unittest.main()

