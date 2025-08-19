from serial_sim import SerialSimulator
from reporter import Reporter
import time
import sys

def main():
    reporter = Reporter(filename='yrz_testNo4.atatat')  # 默认自动带时间戳的.txt 文件
    values = []

    def on_data(msg: str, value: float):
        # 设备数据也写入报告
        reporter.log(f"[设备] {msg}")
        values.append(value)

    reporter.log("测试开始")

    # —— 创建模拟器：加入友好错误提示 —— #
    try:
        sim = SerialSimulator(
            on_data=on_data,
            interval=1.0,
            temp_max=100.0,
            temp_min=50.0,   # 故意写错时，会在这里抛 ValueError
        )
    except ValueError as e:
        reporter.log(f"❌ 配置错误：{e}")
        txt_path = reporter.save()
        print(f"\n已保存 TXT 报告: {txt_path}")
        sys.exit(1)  # 非零退出码

    sim.start()

    try:
        for i in range(5):
            reporter.log(f"执行测试步骤 {i + 1}：检查模拟数据输出")
            time.sleep(1.2)
    finally:
        sim.stop()

        # —— 简单断言与统计 —— #
        if not values:
            reporter.log("[FAIL] 未收到任何温度数据")
        else:
            n = len(values)
            vmin, vmax = min(values), max(values)
            avg = sum(values) / n
            in_range = all(20.0 <= v <= 30.0 for v in values)
            if in_range:
                reporter.log(f"[PASS] 采样 {n} 条，范围 [{vmin:.2f}, {vmax:.2f}] °C，均值 {avg:.2f} °C")
            else:
                bad = [f"{v:.2f}" for v in values if not (20.0 <= v <= 30.0)]
                reporter.log(f"[FAIL] 存在超范围值: {', '.join(bad)}")

        reporter.log("测试结束")
        txt_path = reporter.save()
        print(f"\n已保存 TXT 报告: {txt_path}")

if __name__ == "__main__":
    main()
