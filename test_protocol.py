import unittest
from core.protocol import TimeMachineG2Protocol

class TestProtocol(unittest.TestCase):
    def setUp(self):
        self.protocol = TimeMachineG2Protocol()

    def test_build_command(self):
        cmd = self.protocol.build_command("START")
        self.assertTrue(cmd.startswith("S"))

    def test_parse_time(self):
        result = self.protocol.parse_response("TIME: 00:10.50")
        self.assertEqual(result["type"], "time")
        self.assertEqual(result["value"], "00:10.50")

if __name__ == "__main__":
    unittest.main()
