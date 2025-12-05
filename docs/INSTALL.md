# 安装指南

## 环境要求

- Python 3.8+
- Windows / Linux / macOS
- （可选）NVIDIA GPU + CUDA 用于加速

## 快速安装

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd ph
```

### 2. 创建虚拟环境（推荐）

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 验证安装

```bash
python -c "from chart_recognizer import ChartRecognizer; print('安装成功!')"
```

## GPU加速安装（可选）

如果您有NVIDIA GPU并希望加速OCR识别：

```bash
# 安装GPU版本的PaddlePaddle
pip install paddlepaddle-gpu
```

## 常见问题

### Q1: PaddleOCR下载模型很慢？

**解决方案：** 设置国内镜像

```bash
# 方法1: 设置环境变量
export HUB_HOME=/path/to/your/cache  # Linux/macOS
set HUB_HOME=C:\path\to\cache        # Windows

# 方法2: 手动下载模型
# 下载地址: https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/doc/doc_ch/models_list.md
```

### Q2: OpenCV无法读取图片？

**解决方案：** 确保图片路径正确，不包含中文

```python
# 如果路径包含中文，使用以下方法读取
import cv2
import numpy as np

img = cv2.imdecode(np.fromfile(chinese_path, dtype=np.uint8), cv2.IMREAD_COLOR)
```

### Q3: 内存不足？

**解决方案：** 减小批处理数量，或降低图片分辨率

```python
# 分批处理
recognizer = ChartRecognizer()
for batch in split_images(all_images, batch_size=10):
    results = recognizer.batch_process(batch)
```

## 依赖说明

| 库 | 用途 | 是否必需 |
|----|------|---------|
| opencv-python | 图像处理核心 | ✅ 必需 |
| paddleocr | OCR文字识别 | ✅ 必需 |
| numpy | 数值计算 | ✅ 必需 |
| pandas | 数据处理 | ✅ 必需 |
| Pillow | 图片加载 | ✅ 必需 |
| matplotlib | 可视化 | ⚠️ 可选 |
| torch/transformers | 多模态模型 | ⚠️ 可选 |

## 下一步

安装完成后，请查看：
- [README.md](README.md) - 项目概览
- [example.py](example.py) - 使用示例
- [USAGE.md](USAGE.md) - 详细使用文档


