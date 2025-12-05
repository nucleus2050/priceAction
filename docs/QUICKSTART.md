# 快速开始指南

## 5分钟上手

### 步骤1: 安装依赖 (2分钟)

```bash
# Windows
pip install -r requirements.txt

# Linux/macOS (如果提示权限问题)
pip install --user -r requirements.txt
```

### 步骤2: 测试系统 (1分钟)

```bash
python test_system.py
```

如果看到 "🎉 所有测试通过！系统已就绪。" 说明安装成功！

### 步骤3: 准备图片 (1分钟)

创建一个文件夹并放入图形截图：

```bash
mkdir screenshots
# 将您的图形截图复制到 screenshots/ 文件夹
```

### 步骤4: 开始识别 (1分钟)

```bash
# 识别单张图片
python cli.py -i screenshots/chart.png

# 批量识别整个文件夹
python cli.py -i screenshots/ -o output/
```

## 常用命令

### 基础识别

```bash
# 最简单的用法
python cli.py -i your_image.png
```

### 批量处理

```bash
# 处理整个文件夹，输出所有格式
python cli.py -i screenshots/ -o output/

# 只输出JSON格式
python cli.py -i screenshots/ -o output/ -f json

# 只输出CSV格式
python cli.py -i screenshots/ -o output/ -f csv
```

### 高级选项

```bash
# 使用GPU加速（需要GPU和CUDA）
python cli.py -i screenshots/ -o output/ --gpu

# 开启调试模式（保存中间处理图片）
python cli.py -i screenshots/ -o output/ --debug
```

## Python代码使用

### 最简单的例子

```python
from chart_recognizer import chartRecognizer

# 创建识别器
recognizer = chartRecognizer()

# 识别图片
result = recognizer.recognize('chart.png')

# 打印结果
print(f"识别到 {len(result.data_points)} 根图形元素")
for DataPoint in result.data_points[:3]:  # 打印前3根
    print(f"{DataPoint.date}: 开={DataPoint.open} 收={DataPoint.close}")
```

### 批量处理

```python
from chart_recognizer import chartRecognizer

recognizer = chartRecognizer()

# 批量处理，自动保存结果
results = recognizer.batch_process(
    input_dir='screenshots',
    output_dir='output'
)

# 查看统计
success = sum(1 for r in results if r.confidence > 0.8)
print(f"成功识别: {success}/{len(results)}")
```

### 导出为DataFrame

```python
import pandas as pd
from chart_recognizer import chartRecognizer

recognizer = chartRecognizer()
result = recognizer.recognize('chart.png')

# 转换为pandas DataFrame
df = pd.DataFrame([c.to_dict() for c in result.data_points])

# 数据分析
print(df.describe())
print(f"平均收盘价: {df['close'].mean():.2f}")

# 保存为CSV
df.to_csv('chart_data.csv', index=False)
```

## 常见场景

### 场景1: 从交易软件截图提取数据

```python
from chart_recognizer import chartRecognizer

recognizer = chartRecognizer()
result = recognizer.recognize('tonghuashun_screenshot.png')

# 导出为JSON
import json
with open('stock_data.json', 'w', encoding='utf-8') as f:
    json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)
```

### 场景2: 批量处理多个股票的图形

```bash
# 文件夹结构
screenshots/
├── stock_600000.png
├── stock_600001.png
└── stock_600002.png

# 批量处理
python cli.py -i screenshots/ -o output/

# 结果会保存在
output/
├── results.json
├── results.csv
└── results.xlsx
```

### 场景3: 集成到量化交易系统

```python
from chart_recognizer import chartRecognizer
import pandas as pd

def load_chart_from_image(image_path):
    """从图片加载图形元素数据"""
    recognizer = chartRecognizer()
    result = recognizer.recognize(image_path)
    
    if result.confidence < 0.8:
        print(f"警告: 识别质量较低 ({result.confidence})")
    
    # 转换为DataFrame
    df = pd.DataFrame([c.to_dict() for c in result.data_points])
    df['date'] = pd.to_datetime(df['date'])
    return df

# 使用
df = load_chart_from_image('chart.png')

# 计算技术指标
df['ma5'] = df['close'].rolling(5).mean()
df['ma10'] = df['close'].rolling(10).mean()

print(df.tail())
```

## 输出说明

### JSON格式

```json
{
  "image_name": "chart.png",
  "symbol": "600000",
  "data_points": [
    {
      "date": "2024-01-01",
      "open": 100.5,
      "high": 105.2,
      "low": 98.3,
      "close": 103.7,
      "volume": null
    }
  ],
  "confidence": 0.95,
  "error": null
}
```

### CSV格式

```csv
image,symbol,date,open,high,low,close,volume,confidence
chart.png,600000,2024-01-01,100.5,105.2,98.3,103.7,,0.95
```

## 故障排除

### 问题1: "无法识别图片"

**原因**: 图片格式不支持或文件损坏

**解决**:
```python
# 检查图片是否能正常读取
import cv2
img = cv2.imread('your_image.png')
if img is None:
    print("图片无法读取，请检查路径和格式")
```

### 问题2: "识别到的图形元素数量不对"

**原因**: 图片质量差或包含干扰元素

**解决**:
```bash
# 开启调试模式查看中间结果
python cli.py -i your_image.png --debug

# 查看生成的 debug_*.png 文件
```

### 问题3: "价格数据不准确"

**原因**: 坐标轴刻度识别错误

**解决**:
- 确保图片中坐标轴清晰可见
- 尝试裁剪图片，只保留图形主体
- 提高图片分辨率

### 问题4: "处理速度太慢"

**解决**:
```bash
# 1. 使用GPU加速
python cli.py -i screenshots/ --gpu

# 2. 降低图片分辨率
python -c "from utils import resize_image; resize_image('large.png')"

# 3. 使用并行处理（参考USAGE.md）
```

## 进阶用法

查看详细文档：
- [USAGE.md](USAGE.md) - 完整使用文档
- [example.py](example.py) - 更多代码示例
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 项目架构

## 获取帮助

```bash
# 查看命令行帮助
python cli.py --help

# 运行示例
python example.py

# 运行测试
python test_system.py
```

## 下一步

1. ✅ 系统已安装并测试
2. 📸 准备您的图形截图
3. 🚀 开始批量识别
4. 📊 分析提取的数据
5. 🔧 集成到您的系统

祝您使用愉快！如有问题，请查看 [USAGE.md](USAGE.md) 或提交 Issue。

