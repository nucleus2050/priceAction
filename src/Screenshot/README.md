# Screenshot - 屏幕截图工具包

简单易用的 Python 屏幕截图工具，支持全屏截图和指定区域截图。

## ✨ 特性

- 🖥️ **全屏截图** - 捕获整个屏幕
- 📐 **区域截图** - 指定位置和大小截取区域
- 🎯 **边界框截图** - 使用坐标直接指定区域
- 🖼️ **多屏幕支持** - 完整支持多显示器环境
- 💾 **自动保存** - 自动生成文件名或指定保存路径
- 🚀 **快速方法** - 提供静态方法快速截图
- 📏 **屏幕信息** - 获取屏幕尺寸和显示器信息

## 📦 安装依赖

```bash
pip install Pillow
```

## 🚀 快速开始

### 基础使用

```python
from Screenshot import Screenshot

# 创建截图工具
screenshot = Screenshot()

# 全屏截图
img = screenshot.capture_fullscreen("fullscreen.png")

# 区域截图（x, y, width, height）
img = screenshot.capture_region(100, 100, 800, 600, "region.png")

# 使用边界框（left, top, right, bottom）
img = screenshot.capture_bbox(100, 100, 900, 700, "bbox.png")
```

### 快速截图（静态方法）

```python
from Screenshot import Screenshot

# 不需要创建实例
img = Screenshot.quick_fullscreen("screenshot.png")
img = Screenshot.quick_region(0, 0, 800, 600, "region.png")
```

## 📖 详细使用

### 1. 初始化

```python
from Screenshot import Screenshot

# 使用默认保存目录（screenshots/）
screenshot = Screenshot()

# 指定保存目录
screenshot = Screenshot(save_dir="my_screenshots")
```

### 2. 全屏截图

```python
# 自动生成文件名
img = screenshot.capture_fullscreen()

# 指定文件名
img = screenshot.capture_fullscreen("my_screenshot.png")
```

### 3. 区域截图

```python
# 从(100, 100)开始，宽800高600的区域
img = screenshot.capture_region(100, 100, 800, 600)

# 带保存路径
img = screenshot.capture_region(100, 100, 800, 600, "region.png")
```

### 4. 边界框截图

```python
# 从左上(100, 100)到右下(900, 700)
img = screenshot.capture_bbox(100, 100, 900, 700)

# 带保存路径
img = screenshot.capture_bbox(100, 100, 900, 700, "bbox.png")
```

### 5. 获取屏幕尺寸

```python
width, height = screenshot.get_screen_size()
print(f"屏幕尺寸: {width}x{height}")
```

### 6. 截取屏幕中心区域

```python
# 获取屏幕尺寸
screen_width, screen_height = screenshot.get_screen_size()

# 计算中心区域坐标
capture_width = 1000
capture_height = 800
x = (screen_width - capture_width) // 2
y = (screen_height - capture_height) // 2

# 截取中心区域
img = screenshot.capture_region(x, y, capture_width, capture_height)
```

### 7. 不保存到文件

```python
# 仅获取图像对象，不保存
img = screenshot.capture_region(0, 0, 800, 600)

# 对图像进行处理
img = img.resize((400, 300))
img = img.convert('L')  # 转为灰度图

# 手动保存
img.save("processed.png")
```

### 8. 多显示器支持

```python
# 获取所有显示器信息
monitors = screenshot.get_monitors_info()
print(f"检测到 {len(monitors)} 个显示器")

for monitor in monitors:
    print(f"显示器{monitor['index']}: {monitor['width']}x{monitor['height']}")
    print(f"  位置: ({monitor['x']}, {monitor['y']})")

# 捕获主显示器
img = screenshot.capture_monitor(0)

# 捕获第二个显示器
img = screenshot.capture_monitor(1)

# 分别捕获所有显示器
images = screenshot.capture_all_monitors()

# 捕获所有显示器作为一个整体
img = screenshot.capture_fullscreen(all_screens=True)
```

### 9. 跨显示器区域截图

```python
# 获取显示器信息
monitors = screenshot.get_monitors_info()

# 假设显示器水平排列，捕获跨越两个显示器的区域
monitor0 = monitors[0]
monitor1 = monitors[1]

# 从显示器0的右侧到显示器1的左侧
left = monitor0['x'] + monitor0['width'] - 400
top = monitor0['y'] + 200
right = monitor1['x'] + 400
bottom = top + 600

img = screenshot.capture_bbox(left, top, right, bottom)
```

## 🎯 实用示例

### 批量截图

```python
screenshot = Screenshot(save_dir="batch")

# 将屏幕分成4个区域
screen_width, screen_height = screenshot.get_screen_size()
half_w = screen_width // 2
half_h = screen_height // 2

regions = [
    (0, 0, half_w, half_h, "左上.png"),
    (half_w, 0, half_w, half_h, "右上.png"),
    (0, half_h, half_w, half_h, "左下.png"),
    (half_w, half_h, half_w, half_h, "右下.png")
]

for x, y, w, h, name in regions:
    screenshot.capture_region(x, y, w, h, name)
```

### 定时截图

```python
import time

screenshot = Screenshot()

for i in range(5):
    print(f"截图 {i+1}/5...")
    screenshot.capture_fullscreen(f"screenshot_{i+1}.png")
    time.sleep(2)  # 每2秒截图一次
```

### 延迟截图

```python
import time

screenshot = Screenshot()

print("3秒后进行截图，请切换到目标窗口...")
time.sleep(3)
screenshot.capture_fullscreen("delayed.png")
```

## 📋 API 参考

### Screenshot 类

#### `__init__(save_dir: str = "screenshots")`
初始化截图工具
- `save_dir`: 默认保存目录

#### `capture_fullscreen(save_path: Optional[str] = None) -> Image.Image`
捕获全屏截图
- `save_path`: 保存路径，None则自动生成
- 返回: PIL Image 对象

#### `capture_region(x, y, width, height, save_path=None) -> Image.Image`
捕获指定区域
- `x, y`: 左上角坐标
- `width, height`: 区域大小
- `save_path`: 保存路径
- 返回: PIL Image 对象

#### `capture_bbox(left, top, right, bottom, save_path=None) -> Image.Image`
使用边界框截图
- `left, top`: 左上角坐标
- `right, bottom`: 右下角坐标
- `save_path`: 保存路径
- 返回: PIL Image 对象

#### `get_screen_size(all_screens: bool = False) -> Tuple[int, int]`
获取屏幕尺寸
- `all_screens`: 是否获取所有屏幕的总尺寸
- 返回: (宽度, 高度)

#### `get_monitors_info() -> List[Dict]`
获取所有显示器信息
- 返回: 显示器信息列表，包含索引、位置、尺寸等

#### `capture_monitor(monitor_index: int = 0, save_path: Optional[str] = None) -> Image.Image`
捕获指定显示器
- `monitor_index`: 显示器索引（0为主显示器）
- `save_path`: 保存路径
- 返回: PIL Image 对象

#### `capture_all_monitors(save_dir: Optional[str] = None) -> List[Image.Image]`
分别捕获所有显示器
- `save_dir`: 保存目录
- 返回: 所有显示器的截图列表

#### `quick_fullscreen(save_path: str = None)` (静态方法)
快速全屏截图

#### `quick_region(x, y, width, height, save_path=None)` (静态方法)
快速区域截图

## 🎨 运行示例

```bash
# 运行基础演示程序
python src/Screenshot/Screenshot.py

# 运行详细示例
python src/Screenshot/example.py

# 运行多屏幕示例（推荐多显示器环境）
python src/Screenshot/multi_monitor_example.py
```

## 📝 注意事项

1. **权限**: 某些操作系统可能需要屏幕录制权限
2. **多显示器**: 会捕获主显示器的内容
3. **坐标系统**: 坐标原点(0,0)在屏幕左上角
4. **图像格式**: 默认保存为 PNG 格式

## 🔧 常见问题

**Q: 如何在多显示器环境下使用？**  
A: 完全支持！使用以下方法：
- `capture_fullscreen(all_screens=True)` - 捕获所有显示器作为整体
- `capture_monitor(1)` - 捕获指定显示器
- `capture_all_monitors()` - 分别捕获每个显示器
- `get_monitors_info()` - 获取所有显示器信息

**Q: 多显示器的坐标系统如何工作？**  
A: 多个显示器形成一个大的虚拟屏幕空间。主显示器通常从(0,0)开始，其他显示器的坐标相对于主显示器定位。使用 `get_monitors_info()` 查看每个显示器的准确位置。

**Q: 需要安装额外的库吗？**  
A: 
- 基础功能只需要 Pillow
- 多显示器详细信息需要 `pip install screeninfo`（可选）

**Q: 支持哪些图像格式？**  
A: 支持 PNG, JPEG, BMP 等 PIL 支持的所有格式。

**Q: 如何提高截图质量？**  
A: PNG 格式无损，JPEG 可以调整 quality 参数。

**Q: 可以截取跨越多个显示器的区域吗？**  
A: 可以！使用 `capture_bbox()` 或 `capture_region()` 指定跨越显示器的坐标即可。

## 📄 许可证

MIT License

## 👥 贡献

欢迎提交 Issue 和 Pull Request！

