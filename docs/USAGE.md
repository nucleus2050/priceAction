# 使用文档

## 基础使用

### 命令行使用

最简单的方式是使用命令行工具：

```bash
# 识别单张图片
python cli.py -i chart.png

# 批量处理
python cli.py -i screenshots/ -o output/

# 指定输出格式
python cli.py -i screenshots/ -o output/ -f json csv

# GPU加速
python cli.py -i screenshots/ -o output/ --gpu

# 调试模式
python cli.py -i screenshots/ -o output/ --debug
```

### Python API使用

#### 1. 基础识别

```python
from chart_recognizer import chartRecognizer

# 初始化
recognizer = chartRecognizer()

# 识别单张图片
result = recognizer.recognize('chart.png')

# 查看结果
print(f"识别到 {len(result.data_points)} 根图形元素")
print(f"置信度: {result.confidence}")

for DataPoint in result.data_points:
    print(f"{DataPoint.date}: O={DataPoint.open} H={DataPoint.high} "
          f"L={DataPoint.low} C={DataPoint.close}")
```

#### 2. 批量处理

```python
from chart_recognizer import chartRecognizer

recognizer = chartRecognizer()

# 批量处理，输出多种格式
results = recognizer.batch_process(
    input_dir='screenshots',
    output_dir='output',
    output_formats=['json', 'csv', 'excel']
)

# 筛选高质量结果
good_results = [r for r in results if r.confidence > 0.8]
print(f"高质量结果: {len(good_results)} / {len(results)}")
```

#### 3. 高级配置

```python
from chart_recognizer import chartRecognizer

# 开启GPU加速和调试模式
recognizer = chartRecognizer(
    use_gpu=True,      # GPU加速
    debug=True         # 保存中间处理图片
)

result = recognizer.recognize('chart.png')
```

## 输出格式说明

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

| image | symbol | date | open | high | low | close | volume | confidence |
|-------|--------|------|------|------|-----|-------|--------|------------|
| chart.png | 600000 | 2024-01-01 | 100.5 | 105.2 | 98.3 | 103.7 | null | 0.95 |

### Excel格式

与CSV格式相同，但保存为 `.xlsx` 文件，支持多个工作表。

## 数据处理示例

### 与pandas结合

```python
import pandas as pd
from chart_recognizer import chartRecognizer

recognizer = chartRecognizer()
result = recognizer.recognize('chart.png')

# 转换为DataFrame
df = pd.DataFrame([c.to_dict() for c in result.data_points])

# 数据分析
df['date'] = pd.to_datetime(df['date'])
df['change'] = (df['close'] - df['open']) / df['open'] * 100

print(df.describe())
```

### 计算技术指标

```python
def calculate_ma(closes, period=5):
    """计算移动平均线"""
    if len(closes) < period:
        return None
    return sum(closes[-period:]) / period

result = recognizer.recognize('chart.png')
closes = [c.close for c in result.data_points]

ma5 = calculate_ma(closes, 5)
ma10 = calculate_ma(closes, 10)
print(f"MA5: {ma5:.2f}, MA10: {ma10:.2f}")
```

### 与TA-Lib集成

```python
import talib
import numpy as np

result = recognizer.recognize('chart.png')

# 提取OHLC数据
opens = np.array([c.open for c in result.data_points])
highs = np.array([c.high for c in result.data_points])
lows = np.array([c.low for c in result.data_points])
closes = np.array([c.close for c in result.data_points])

# 计算技术指标
macd, signal, hist = talib.MACD(closes)
rsi = talib.RSI(closes)

print(f"当前RSI: {rsi[-1]:.2f}")
```

## 批处理优化

### 大批量处理

```python
from pathlib import Path
from chart_recognizer import chartRecognizer
import json

def batch_process_large(input_dir, output_dir, batch_size=50):
    """分批处理大量图片"""
    recognizer = chartRecognizer()
    
    # 获取所有图片
    images = list(Path(input_dir).glob('*.png'))
    
    # 分批处理
    for i in range(0, len(images), batch_size):
        batch = images[i:i+batch_size]
        print(f"处理批次 {i//batch_size + 1}: {len(batch)} 张")
        
        results = []
        for img in batch:
            result = recognizer.recognize(str(img))
            results.append(result)
        
        # 保存批次结果
        output_file = Path(output_dir) / f'batch_{i//batch_size + 1}.json'
        with open(output_file, 'w') as f:
            json.dump([r.to_dict() for r in results], f)

# 使用
batch_process_large('large_dataset/', 'output/', batch_size=50)
```

### 并行处理

```python
from concurrent.futures import ThreadPoolExecutor
from chart_recognizer import chartRecognizer
from pathlib import Path

def parallel_process(input_dir, output_dir, workers=4):
    """并行处理图片"""
    recognizer = chartRecognizer()
    images = list(Path(input_dir).glob('*.png'))
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(
            lambda img: recognizer.recognize(str(img)),
            images
        ))
    
    # 保存结果
    recognizer._export_results(results, Path(output_dir), ['json', 'csv'])
    return results

# 使用
results = parallel_process('screenshots/', 'output/', workers=4)
```

## 常见场景

### 场景1: 交易软件截图识别

```python
recognizer = chartRecognizer(debug=False)

# 处理来自不同交易软件的截图
result = recognizer.recognize('tonghuashun_screenshot.png')
```

### 场景2: PDF中的图形提取

```python
from pdf2image import convert_from_path
from chart_recognizer import chartRecognizer

# 先将PDF转为图片
images = convert_from_path('report.pdf')

recognizer = chartRecognizer()
results = []

for i, image in enumerate(images):
    # 保存临时图片
    temp_file = f'temp_page_{i}.png'
    image.save(temp_file)
    
    # 识别
    result = recognizer.recognize(temp_file)
    results.append(result)
```

### 场景3: 实时监控与识别

```python
import time
from pathlib import Path
from chart_recognizer import chartRecognizer

def monitor_folder(watch_dir, output_dir, interval=5):
    """监控文件夹，自动识别新图片"""
    recognizer = chartRecognizer()
    processed = set()
    
    while True:
        files = set(Path(watch_dir).glob('*.png'))
        new_files = files - processed
        
        for file in new_files:
            print(f"发现新图片: {file.name}")
            result = recognizer.recognize(str(file))
            
            # 保存结果
            output_file = Path(output_dir) / f'{file.stem}_result.json'
            with open(output_file, 'w') as f:
                json.dump(result.to_dict(), f, indent=2)
            
            processed.add(file)
        
        time.sleep(interval)

# 使用
monitor_folder('watch/', 'output/', interval=5)
```

## 性能优化建议

1. **使用GPU**: 如有NVIDIA GPU，设置 `use_gpu=True`
2. **预处理图片**: 统一图片大小和格式
3. **批量处理**: 使用 `batch_process()` 而非循环调用
4. **并行处理**: 对于大批量，使用多线程/多进程
5. **图片质量**: 确保截图清晰，分辨率 > 800x600

## 故障排除

### 问题：识别准确率低

**解决方案：**
1. 检查图片质量（清晰度、分辨率）
2. 确保坐标轴可见
3. 开启 `debug=True` 查看中间处理结果
4. 尝试调整图片对比度

### 问题：无法识别特定格式的图形

**解决方案：**
1. 提供样本图片，可能需要针对性优化
2. 检查颜色方案（红涨绿跌 vs 绿涨红跌）
3. 联系开发者添加支持

### 问题：处理速度慢

**解决方案：**
1. 启用GPU加速
2. 降低图片分辨率
3. 使用并行处理
4. 分批处理大数据集

## 更多示例

完整示例代码请参考 [example.py](example.py)

