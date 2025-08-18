import threading
import time
import random

class SerialSimulator:
    def __init__(self):
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self._simulate_data, daemon=True).start()

    def _simulate_data(self):
        while self.running:
            value = round(random.uniform(20.0, 30.0), 2)
            print(f"[SerialSimulator] 温度数据: {value} °C")
            time.sleep(1)

    def stop(self):
        self.running = False

if __name__ == "__main__":
    sim = SerialSimulator()
    sim.start()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        sim.stop()
