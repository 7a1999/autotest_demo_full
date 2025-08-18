from serial_sim import SerialSimulator
from reporter import Reporter
import time

def main():
    sim = SerialSimulator()
    reporter = Reporter()
    reporter.log("测试开始")
    sim.start()

    try:
        for i in range(5):
            reporter.log(f"执行测试步骤 {i+1}：检查模拟数据输出")
            time.sleep(1.2)
    finally:
        sim.stop()
        reporter.log("测试结束")
        reporter.save()

if __name__ == "__main__":
    main()
