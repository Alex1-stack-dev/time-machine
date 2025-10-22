class TimeMachineG2Protocol:
    """
    Implements advanced protocol: parses device messages and builds commands.
    """
    def __init__(self):
        self.commands = {
            "START": "S",
            "STOP": "T",
            "RESET": "R",
            "SPLIT": "L",
        }

    def build_command(self, action, *args):
        if action in self.commands:
            cmd = self.commands[action]
            if args:
                cmd += " " + " ".join(str(a) for a in args)
            return f"{cmd}\r\n"
        raise ValueError(f"Unknown command: {action}")

    def parse_response(self, line):
        """
        Parses advanced device protocol:
        - TIME:00:12.34
        - SPLIT:00:12.34
        - EVENT:STARTED
        - ERROR:...
        - STATE:RUNNING
        """
        if line.startswith("TIME:"):
            return {"type": "time", "value": line.split(":", 1)[1].strip()}
        elif line.startswith("SPLIT:"):
            return {"type": "split", "value": line.split(":", 1)[1].strip()}
        elif line.startswith("EVENT:"):
            return {"type": "event", "value": line.split(":", 1)[1].strip()}
        elif line.startswith("ERROR:"):
            return {"type": "error", "value": line.split(":", 1)[1].strip()}
        elif line.startswith("STATE:"):
            return {"type": "state", "value": line.split(":", 1)[1].strip()}
        # Add more parsing as your manual requires
        return {"type": "raw", "value": line}
