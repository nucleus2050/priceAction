# 多屏幕支持说明

## 🖥️ 概述

Screenshot 工具完全支持多显示器环境，可以：
- ✅ 检测所有显示器
- ✅ 获取每个显示器的详细信息
- ✅ 单独捕获任意显示器
- ✅ 捕获所有显示器（作为整体或分别）
- ✅ 捕获跨越多个显示器的区域

## 📦 依赖

### 基础功能（必需）
```bash
pip install Pillow
```

### 增强功能（可选）
```bash
pip install screeninfo
```

安装 `screeninfo` 后可以获得：
- 更准确的显示器信息
- 显示器名称
- 主显示器标识
- 精确的显示器位置

## 🎯 使用方法

### 1. 检测显示器

```python
from Screenshot import Screenshot

screenshot = Screenshot()

# 获取所有显示器信息
monitors = screenshot.get_monitors_info()

print(f"检测到 {len(monitors)} 个显示器")
for monitor in monitors:
    print(f"显示器{monitor['index']}: {monitor['width']}x{monitor['height']}")
    print(f"  位置: ({monitor['x']}, {monitor['y']})")
    if monitor.get('is_primary'):
        print(f"  这是主显示器")
```

**输出示例（双显示器）：**
```
检测到 2 个显示器
显示器0: 1920x1080
  位置: (0, 0)
  这是主显示器
显示器1: 1920x1080
  位置: (1920, 0)
```

### 2. 捕获单个显示器

```python
# 捕获主显示器（显示器0）
img = screenshot.capture_monitor(0, "monitor0.png")

# 捕获第二个显示器
img = screenshot.capture_monitor(1, "monitor1.png")

# 自动保存（自动生成文件名）
img = screenshot.capture_monitor(0)
```

### 3. 捕获所有显示器

#### 方式1：分别捕获每个显示器

```python
# 返回图像列表，每个显示器一张
images = screenshot.capture_all_monitors()

print(f"捕获了 {len(images)} 个显示器")
for i, img in enumerate(images):
    print(f"显示器{i}: {img.size}")
```

#### 方式2：作为一个整体捕获

```python
# 捕获所有显示器形成的虚拟大屏幕
img = screenshot.capture_fullscreen(all_screens=True)

print(f"总尺寸: {img.size}")  # 例如: (3840, 1080) 对于两个并排的1920x1080显示器
```

### 4. 捕获特定显示器上的区域

```python
# 获取第二个显示器的信息
monitors = screenshot.get_monitors_info()
monitor1 = monitors[1]

# 在第二个显示器的中心捕获800x600区域
x = monitor1['x'] + (monitor1['width'] - 800) // 2
y = monitor1['y'] + (monitor1['height'] - 600) // 2

img = screenshot.capture_region(x, y, 800, 600, "monitor1_center.png")
```

### 5. 捕获跨越多个显示器的区域

```python
# 假设显示器水平排列
monitor0 = monitors[0]
monitor1 = monitors[1]

# 从第一个显示器的右侧到第二个显示器的左侧
left = monitor0['x'] + monitor0['width'] - 500
top = 200
right = monitor1['x'] + 500
bottom = top + 800

img = screenshot.capture_bbox(left, top, right, bottom, "cross_monitors.png")
```

## 📐 坐标系统说明

### 单显示器
```
(0,0) ┌─────────────────┐
      │                 │
      │   1920 x 1080   │
      │                 │
      └─────────────────┘ (1920, 1080)
```

### 双显示器（水平排列）
```
主显示器                  第二显示器
(0,0) ┌────────────┐     ┌────────────┐
      │            │     │            │
      │ 1920x1080  │     │ 1920x1080  │
      │            │     │            │
      └────────────┘     └────────────┘
                   (1920,1080) (3840,1080)
```

### 双显示器（垂直排列）
```
      (0,0) ┌────────────┐
            │            │
            │ 1920x1080  │  主显示器
            │            │
            └────────────┘ (1920,1080)
      (0,1080)┌──────────┐
              │          │
              │1920x1080 │  第二显示器
              │          │
              └──────────┘ (1920,2160)
```

## 💡 实用示例

### 示例1：监控所有显示器

```python
import time

screenshot = Screenshot(save_dir="monitoring")

while True:
    # 每5秒捕获所有显示器
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    for i in range(len(screenshot.get_monitors_info())):
        screenshot.capture_monitor(i, f"monitor{i}_{timestamp}.png")
    
    time.sleep(5)
```

### 示例2：比较显示器内容

```python
# 同时捕获两个显示器
images = screenshot.capture_all_monitors()

if len(images) >= 2:
    img1 = images[0]
    img2 = images[1]
    
    # 创建并排比较图
    from PIL import Image
    
    total_width = img1.width + img2.width
    max_height = max(img1.height, img2.height)
    
    comparison = Image.new('RGB', (total_width, max_height))
    comparison.paste(img1, (0, 0))
    comparison.paste(img2, (img1.width, 0))
    
    comparison.save("comparison.png")
```

### 示例3：扩展桌面截图

```python
# 获取跨所有显示器的完整桌面
monitors = screenshot.get_monitors_info()

# 计算虚拟桌面边界
min_x = min(m['x'] for m in monitors)
min_y = min(m['y'] for m in monitors)
max_x = max(m['x'] + m['width'] for m in monitors)
max_y = max(m['y'] + m['height'] for m in monitors)

print(f"虚拟桌面尺寸: {max_x - min_x}x{max_y - min_y}")

# 捕获整个虚拟桌面
img = screenshot.capture_bbox(min_x, min_y, max_x, max_y, "full_desktop.png")
```

## ⚙️ 配置建议

### 获取更详细的显示器信息

```python
# 安装 screeninfo 后
monitors = screenshot.get_monitors_info()

for monitor in monitors:
    print(f"\n显示器 {monitor['index']}")
    print(f"  名称: {monitor.get('name', 'Unknown')}")
    print(f"  尺寸: {monitor['width']}x{monitor['height']}")
    print(f"  位置: ({monitor['x']}, {monitor['y']})")
    print(f"  主显示器: {'是' if monitor.get('is_primary') else '否'}")
```

### 性能优化

```python
# 对于频繁截图，缓存显示器信息
monitors = screenshot.get_monitors_info()  # 只调用一次

for i in range(100):
    # 使用缓存的信息
    monitor = monitors[0]
    img = screenshot.capture_monitor(0)
    # 处理图像...
```

## 🔍 故障排除

### 问题1: 只能看到一个显示器

**解决方案：**
```bash
pip install screeninfo
```

### 问题2: 坐标不准确

**检查显示器布局：**
```python
monitors = screenshot.get_monitors_info()
for m in monitors:
    print(f"显示器{m['index']}: ({m['x']}, {m['y']}) {m['width']}x{m['height']}")
```

### 问题3: 跨显示器截图失败

**确保坐标在有效范围内：**
```python
# 计算虚拟屏幕总范围
monitors = screenshot.get_monitors_info()
min_x = min(m['x'] for m in monitors)
max_x = max(m['x'] + m['width'] for m in monitors)
min_y = min(m['y'] for m in monitors)
max_y = max(m['y'] + m['height'] for m in monitors)

print(f"有效X范围: {min_x} 到 {max_x}")
print(f"有效Y范围: {min_y} 到 {max_y}")
```

## 📝 注意事项

1. **显示器索引**: 从0开始，0通常是主显示器
2. **坐标系统**: 多显示器形成一个大的虚拟坐标空间
3. **负坐标**: 某些配置下显示器可能有负坐标
4. **动态检测**: 连接/断开显示器后需要重新获取信息
5. **权限**: Windows/macOS 可能需要屏幕录制权限

## 🎯 最佳实践

1. **始终检查显示器数量**
   ```python
   monitors = screenshot.get_monitors_info()
   if len(monitors) > 1:
       # 多显示器逻辑
   else:
       # 单显示器逻辑
   ```

2. **使用显示器信息计算坐标**
   ```python
   monitor = monitors[1]
   center_x = monitor['x'] + monitor['width'] // 2
   center_y = monitor['y'] + monitor['height'] // 2
   ```

3. **处理不同分辨率**
   ```python
   for monitor in monitors:
       # 根据显示器分辨率调整捕获区域
       if monitor['width'] >= 1920:
           # 高分辨率逻辑
       else:
           # 低分辨率逻辑
   ```

## 📚 完整示例

运行多屏幕完整示例：
```bash
python src/Screenshot/multi_monitor_example.py
```

这将演示所有多屏幕功能，包括：
- 显示器检测和信息显示
- 单独捕获每个显示器
- 整体捕获所有显示器
- 跨显示器区域截图
- 显示器布局可视化

## 🔗 相关资源

- [主文档](README.md)
- [基础示例](example.py)
- [多屏幕示例](multi_monitor_example.py)

