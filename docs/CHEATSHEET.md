# 图形识别系统 - 速查表 🚀

## 快速命令

### 安装和测试
```bash
# 安装依赖
pip install -r requirements.txt

# 测试系统
python test_system.py

# 运行演示
python demo.py
```

### 命令行使用
```bash
# 识别单张图片
python cli.py -i chart.png

# 批量处理
python cli.py -i screenshots/ -o output/

# 指定输出格式
python cli.py -i screenshots/ -f json csv

# GPU加速
python cli.py -i screenshots/ --gpu

# 调试模式
python cli.py -i screenshots/ --debug

# 查看帮助
python cli.py --help
```

## Python API

### 基础使用
```python
from chart_recognizer import chartRecognizer

# 初始化
recognizer = chartRecognizer()

# 识别单张
result = recognizer.recognize('chart.png')

# 批量处理
results = recognizer.batch_process('screenshots/', 'output/')
```

### 高级配置
```python
# GPU加速 + 调试模式
recognizer = chartRecognizer(use_gpu=True, debug=True)

# 自定义输出格式
results = recognizer.batch_process(
    input_dir='screenshots/',
    output_dir='output/',
    output_formats=['json', 'csv', 'excel']
)
```

### 数据处理
```python
import pandas as pd

# 转换为DataFrame
df = pd.DataFrame([c.to_dict() for c in result.data_points])

# 保存CSV
df.to_csv('data.csv', index=False)

# 计算技术指标
df['ma5'] = df['close'].rolling(5).mean()
```

## 常用代码片段

### 读取识别结果
```python
import json

# 读取JSON结果
with open('output/results.json', 'r') as f:
    data = json.load(f)

# 读取CSV结果
import pandas as pd
df = pd.read_csv('output/results.csv')
```

### 数据验证
```python
from utils import validate_DataPoint_data

is_valid, errors = validate_DataPoint_data(result.data_points)
if not is_valid:
    print("数据错误:", errors)
```

### 可视化
```python
from utils import visualize_chart

visualize_chart(result.data_points, 'chart.png', show=True)
```

### 生成报告
```python
from utils import generate_report

generate_report(results, 'report.html')
```

## 配置参数

### OCR配置
```python
# config.py
OCR_CONFIG = {
    'use_gpu': False,
    'lang': 'ch',  # 'ch' 或 'en'
}
```

### 图形元素检测配置
```python
DataPoint_DETECTION = {
    'min_DataPoint_width': 3,
    'min_DataPoint_height': 5,
}
```

### 置信度阈值
```python
CONFIDENCE_THRESHOLDS = {
    'high': 0.8,
    'medium': 0.5,
}
```

## 数据结构

### DataPoint (图形元素)
```python
{
    'date': '2024-01-01',
    'open': 100.5,
    'high': 105.2,
    'low': 98.3,
    'close': 103.7,
    'volume': None
}
```

### RecognitionResult (识别结果)
```python
{
    'image_name': 'chart.png',
    'symbol': '600000',
    'data_points': [...],
    'confidence': 0.95,
    'error': None
}
```

## 常见问题

### Q: 识别准确率低？
```python
# 1. 开启调试模式查看中间结果
recognizer = chartRecognizer(debug=True)

# 2. 检查图片质量
from utils import enhance_image_contrast
enhanced = enhance_image_contrast('chart.png')

# 3. 调整配置参数
# 编辑 config.py
```

### Q: 处理速度慢？
```bash
# 1. 使用GPU加速
python cli.py -i screenshots/ --gpu

# 2. 降低图片分辨率
python -c "from utils import resize_image; resize_image('large.png')"

# 3. 并行处理
# 参考 USAGE.md 中的并行处理示例
```

### Q: 内存不足？
```python
# 分批处理
from pathlib import Path

images = list(Path('screenshots/').glob('*.png'))
for i in range(0, len(images), 50):
    batch = images[i:i+50]
    # 处理batch
```

## 输出格式

### JSON
```json
{
  "image_name": "chart.png",
  "data_points": [
    {"date": "2024-01-01", "open": 100, "high": 105, "low": 98, "close": 103}
  ],
  "confidence": 0.95
}
```

### CSV
```csv
image,symbol,date,open,high,low,close,confidence
chart.png,600000,2024-01-01,100,105,98,103,0.95
```

## 工具函数速查

| 函数 | 用途 | 示例 |
|------|------|------|
| `visualize_chart()` | 可视化图形元素 | `visualize_chart(data_points, 'out.png')` |
| `validate_DataPoint_data()` | 验证数据 | `is_valid, errors = validate_DataPoint_data(data_points)` |
| `resize_image()` | 调整大小 | `resize_image('large.png', 1920, 1080)` |
| `enhance_image_contrast()` | 增强对比度 | `enhance_image_contrast('dark.png')` |
| `generate_report()` | 生成报告 | `generate_report(results, 'report.html')` |

## 性能参考

| 场景 | 速度 | 准确率 |
|------|------|--------|
| 标准图形 (CPU) | 2-5秒 | 95%+ |
| 标准图形 (GPU) | 1-2秒 | 95%+ |
| 带指标图表 | 3-6秒 | 85%+ |
| 低质量图片 | 5-10秒 | 70%+ |

## 文档快速链接

- 📖 [README](README.md) - 项目概览
- 🚀 [快速开始](QUICKSTART.md) - 5分钟上手
- 💾 [安装指南](INSTALL.md) - 详细安装
- 📘 [使用文档](USAGE.md) - 完整API
- 🏛️ [项目结构](PROJECT_STRUCTURE.md) - 架构说明
- 📊 [项目总结](SUMMARY.md) - 技术详解
- 📚 [文档索引](INDEX.md) - 所有文档

## 快速调试

```python
# 开启调试模式
recognizer = chartRecognizer(debug=True)
result = recognizer.recognize('chart.png')

# 查看生成的调试图片
# - debug_preprocessed.png (预处理结果)
# - debug_data_points.png (图形元素检测结果)

# 打印详细信息
print(f"置信度: {result.confidence}")
print(f"图形元素数量: {len(result.data_points)}")
if result.error:
    print(f"错误: {result.error}")
```

## 技术支持

- 📖 查看文档: [INDEX.md](INDEX.md)
- 🐛 报告问题: GitHub Issues
- 💬 讨论交流: GitHub Discussions
- 📧 联系作者: your-email@example.com

---

💡 **提示**: 将此文件保存为书签，随时查阅！

