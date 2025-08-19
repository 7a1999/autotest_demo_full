import threading, time, random
from typing import Callable, Optional

class SerialSimulator:
    def __init__(
        self,
        interval: float = 1.0,
        temp_min: float = 20.0,
        temp_max: float = 30.0,
        on_data: Optional[Callable[[str, float], None]] = None,
    ):
        self.interval = interval
        self._on_data = on_data

        # 用私有属性+property 封装
        self._temp_min: float = 0.0
        self._temp_max: float = 0.0
        self.set_range(temp_min, temp_max)   # ✅ 构造时一次性校验并设置

        self._stop = threading.Event()
        self._th: Optional[threading.Thread] = None

    # ---------- 可随时修改的属性（带校验） ----------
    @property
    def temp_min(self) -> float:
        return self._temp_min

    @temp_min.setter
    def temp_min(self, value: float) -> None:
        if value >= self._temp_max:
            raise ValueError("温度下限必须小于当前上限")
        self._temp_min = float(value)

    @property
    def temp_max(self) -> float:
        return self._temp_max

    @temp_max.setter
    def temp_max(self, value: float) -> None:
        if value <= self._temp_min:
            raise ValueError("温度上限必须大于当前下限")
        self._temp_max = float(value)

    def set_range(self, temp_min: float, temp_max: float) -> None:
        """一次性修改上下限，避免分步赋值的临时非法状态。"""
        if temp_max <= temp_min:
            raise ValueError("温度上限必须大于下限")
        self._temp_min = float(temp_min)
        self._temp_max = float(temp_max)

    # ---------- 其余逻辑不变 ----------
    def start(self) -> None:
        # 运行前再保险校验一次
        if self._temp_max <= self._temp_min:
            raise ValueError("温度上限必须大于下限")
        if self._th and self._th.is_alive():
            return
        self._stop.clear()
        self._th = threading.Thread(target=self._simulate_data, daemon=True)
        self._th.start()

    def _simulate_data(self) -> None:
        while not self._stop.is_set():
            value = round(random.uniform(self._temp_min, self._temp_max), 2)
            line = f"温度数据: {value:.2f} °C"
            print(f"[SerialSimulator] {line}")
            if self._on_data:
                try:
                    self._on_data(line, value)
                except Exception as e:
                    print(f"[SerialSimulator] on_data 回调异常: {e}")
            time.sleep(self.interval)

    def stop(self) -> None:
        self._stop.set()
        if self._th and self._th.is_alive():
            self._th.join(timeout=2.0)
            self._th = None
