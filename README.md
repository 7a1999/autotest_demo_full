

一个 Python 自动化测试项目示例，适用于初学者入门自动化测试开发（后续在AI基础上增加更多功能）。

## 功能简介
- 模拟串口通信（`serial_sim.py`）
- 自动执行测试并记录日志（`app.py`、`reporter.py`）
- 生成测试报告（`test_report.txt`）

## 使用方法
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
python app.py



yrz   ^_^.
新增了一些功能：
1.生产报告自动补全txt后缀，防止忘记补充后缀生产文件无法读取（后续打算继续优化例如直接生成doc，xlm等文件便于进一步统计一分析）
2.interval/temp_min/temp_max构造参数可调，便于模拟不同频率/量程的设备
3.步骤日志和设备数据都写入报告数据更清晰
4.温度进行校验
5.模拟器支持数据回溯
