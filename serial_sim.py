import threading
import time
import random
from typing import Callable, Optional


class SerialSimulator:
    """
    简易“串口设备”模拟器：
    - 每隔 interval 秒输出一次温度（temp_min ~ temp_max）
    - on_data 可选回调：on_data(message: str, value: float)
    """
    def __init__(
        self,
        interval: float = 1.0,
        temp_min: float = 20.0,
        temp_max: float = 30.0,
        on_data: Optional[Callable[[str, float], None]] = None,
    ):
        self.interval = interval
        self.temp_min = temp_min
        self.temp_max = temp_max
        self._on_data = on_data

        self._stop = threading.Event()
        self._th: Optional[threading.Thread] = None

    def set_range(self, temp_min: float, temp_max: float):
            """设置温度范围，并检查合法性"""
            if temp_max <= temp_min:
                raise ValueError("温度上限必须大于下限")
            self.temp_min = temp_min
            self.temp_max = temp_max

    def start(self) -> None:
        """启动后台线程"""
        if self._th and self._th.is_alive():
            return
        self._stop.clear()
        self._th = threading.Thread(target=self._simulate_data, daemon=True)
        self._th.start()

    def _simulate_data(self) -> None:
        """后台产出数据"""
        while not self._stop.is_set():
            value = round(random.uniform(self.temp_min, self.temp_max), 2)
            line = f"温度数据: {value:.2f} °C"
            print(f"[SerialSimulator] {line}")
            if self._on_data:
                try:
                    self._on_data(line, value)
                except Exception as e:
                    print(f"[SerialSimulator] on_data 回调异常: {e}")
            time.sleep(self.interval)

    def stop(self) -> None:
        """请求停止并等待线程退出"""
        self._stop.set()
        if self._th and self._th.is_alive():
            self._th.join(timeout=2.0)
            self._th = None


if __name__ == "__main__":
    # 单文件自运行测试：Ctrl+C 停止
    sim = SerialSimulator()
    sim.start()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        sim.stop()
