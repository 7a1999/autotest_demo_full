from datetime import datetime

class Reporter:
    def __init__(self, filename="test_report.txt"):
        self.filename = filename
        self.lines = []

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {message}"
        print(line)
        self.lines.append(line)

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write("\n".join(self.lines))
