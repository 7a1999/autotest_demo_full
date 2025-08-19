# reporter.py
import os
import re
from datetime import datetime
from typing import Optional


class Reporter:
    """
    轻量日志器（带自动纠正文件名）：
    - log(msg):  追加一行带时间戳的日志，可选同步打印到控制台
    - save(dir): 保存为 .txt 文件，返回保存路径
    - 文件名规则：
        * 未传 filename -> 自动生成 test_report_YYYY-MM-DD_HH-MM-SS.txt
        * 传了 filename -> 统一/纠正为 .txt；过滤 Windows 非法字符
        * 若发生更名：打印提示，并记录 self.renamed_from
    """

    def __init__(
        self,
        filename: Optional[str] = None,
        ensure_txt: bool = True,
        auto_print: bool = True,
    ):
        """
        :param filename: 自定义文件名（可不带后缀或带任意后缀）
        :param ensure_txt: 是否强制改为/补上 .txt 后缀
        :param auto_print: 调用 log() 时是否同步 print 到控制台
        """
        renamed_from = None

        # 1) 默认文件名（未传 filename 时）
        if filename is None:
            ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"test_report_{ts}.txt"

        original = filename  # 记录用户原始输入（用于提示）

        # 2) 过滤 Windows 非法字符：\ / : * ? " < > |
        filename = re.sub(r'[\\/:*?"<>|]', "_", filename)

        # 3) 统一/纠正后缀为 .txt
        if ensure_txt:
            # 是否“看起来有后缀”（仅检查结尾的 .xxx）
            if re.search(r"\.[A-Za-z0-9]+$", filename):
                # 有后缀：一律替换成 .txt（实现自动纠正/统一大小写）
                new_name = re.sub(r"\.[A-Za-z0-9]+$", ".txt", filename)
                if new_name != original:
                    renamed_from = original
                filename = new_name
            else:
                # 无后缀：补上 .txt
                filename = filename + ".txt"
                if original != filename:
                    renamed_from = original

        self.filename: str = filename
        self.lines: list[str] = []
        self.renamed_from: Optional[str] = renamed_from
        self.auto_print: bool = auto_print

        # 4) 若发生更名，打印提示
        if self.renamed_from:
            print(f"⚠ 已自动更正文件名：'{self.renamed_from}' → '{self.filename}'")

    def log(self, msg: str) -> None:
        """写一行带时间戳的日志；根据 auto_print 决定是否 print 出来"""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] {msg}"
        self.lines.append(line)
        if self.auto_print:
            print(line)

    def save(self, dir: Optional[str] = None) -> str:
        """
        保存日志为文本文件。
        :param dir: 可选保存目录（不存在会自动创建）。不传则保存到当前目录。
        :return: 实际保存的绝对路径
        """
        if dir:
            os.makedirs(dir, exist_ok=True)
            path = os.path.join(dir, self.filename)
        else:
            path = self.filename

        with open(path, "w", encoding="utf-8", newline="\n") as f:
            # 逐行写出；若没有任何日志也创建空文件
            for line in self.lines:
                f.write(line + "\n")

        return os.path.abspath(path)
