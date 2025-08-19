from datetime import datetime
from typing import Optional


class Reporter:
    """
    轻量日志器：
    - log()：带时间戳打印并缓存
    - save()：保存为 .txt（默认自动补 .txt）
    - 默认文件名：test_report_YYYY-MM-DD_HH-MM-SS.txt
    """
    def __init__(self, filename: Optional[str] = None, ensure_txt: bool = True):
        if filename is None:
            ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"test_report_{ts}.txt"
        elif ensure_txt and not filename.lower().endswith(".txt"):
            filename += ".txt"

        self.filename = filename
        self.lines = []

    def log(self, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {message}"
        print(line)
        self.lines.append(line)

    def save(self, filename: Optional[str] = None) -> str:
        path = filename or self.filename
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.lines))
        return path
