"""
屏幕截图工具使用示例
"""

from Screenshot import Screenshot
import time


def example_basic():
    """基础使用示例"""
    print("\n" + "=" * 60)
    print("示例1: 基础使用")
    print("=" * 60)
    
    # 创建截图工具
    screenshot = Screenshot(save_dir="screenshots")
    
    # 获取屏幕尺寸
    width, height = screenshot.get_screen_size()
    print(f"\n屏幕尺寸: {width}x{height}")
    
    # 全屏截图
    print("\n正在进行全屏截图...")
    time.sleep(1)  # 给用户一点准备时间
    img = screenshot.capture_fullscreen("example_fullscreen.png")
    print(f"截图尺寸: {img.size}")


def example_region():
    """区域截图示例"""
    print("\n" + "=" * 60)
    print("示例2: 区域截图")
    print("=" * 60)
    
    screenshot = Screenshot()
    
    # 截取屏幕左上角区域
    print("\n截取左上角 800x600 区域...")
    time.sleep(1)
    img = screenshot.capture_region(0, 0, 800, 600, "example_region.png")
    print(f"截图尺寸: {img.size}")


def example_center():
    """截取屏幕中心区域"""
    print("\n" + "=" * 60)
    print("示例3: 截取屏幕中心区域")
    print("=" * 60)
    
    screenshot = Screenshot()
    
    # 获取屏幕尺寸
    screen_width, screen_height = screenshot.get_screen_size()
    
    # 计算中心区域
    capture_width = 1000
    capture_height = 800
    x = (screen_width - capture_width) // 2
    y = (screen_height - capture_height) // 2
    
    print(f"\n截取中心区域 {capture_width}x{capture_height}...")
    time.sleep(1)
    img = screenshot.capture_region(x, y, capture_width, capture_height, 
                                   "example_center.png")
    print(f"截图尺寸: {img.size}")


def example_bbox():
    """使用边界框截图"""
    print("\n" + "=" * 60)
    print("示例4: 使用边界框截图")
    print("=" * 60)
    
    screenshot = Screenshot()
    
    # 使用边界框坐标
    print("\n截取坐标 (100, 100) 到 (900, 700) 的区域...")
    time.sleep(1)
    img = screenshot.capture_bbox(100, 100, 900, 700, "example_bbox.png")
    print(f"截图尺寸: {img.size}")


def example_quick():
    """快速截图方法"""
    print("\n" + "=" * 60)
    print("示例5: 快速截图（静态方法）")
    print("=" * 60)
    
    # 不需要创建实例，直接使用静态方法
    print("\n使用静态方法快速截图...")
    time.sleep(1)
    
    # 快速全屏
    img1 = Screenshot.quick_fullscreen("quick_fullscreen.png")
    print(f"全屏截图尺寸: {img1.size}")
    
    # 快速区域截图
    img2 = Screenshot.quick_region(200, 200, 600, 400, "quick_region.png")
    print(f"区域截图尺寸: {img2.size}")


def example_no_save():
    """不保存文件，仅返回图像对象"""
    print("\n" + "=" * 60)
    print("示例6: 不保存文件，仅获取图像对象")
    print("=" * 60)
    
    screenshot = Screenshot()
    
    # 截图但不保存到文件
    print("\n截图但不保存...")
    time.sleep(1)
    img = screenshot.capture_region(0, 0, 400, 300)
    
    # 可以对图像进行处理
    print(f"\n图像信息:")
    print(f"  尺寸: {img.size}")
    print(f"  模式: {img.mode}")
    print(f"  格式: {img.format}")
    
    # 手动保存
    img.save("manual_save.png")
    print("✓ 手动保存成功")


def example_multiple():
    """批量截图示例"""
    print("\n" + "=" * 60)
    print("示例7: 批量截图")
    print("=" * 60)
    
    screenshot = Screenshot(save_dir="batch_screenshots")
    
    # 将屏幕分成4个区域分别截图
    screen_width, screen_height = screenshot.get_screen_size()
    half_w = screen_width // 2
    half_h = screen_height // 2
    
    regions = [
        (0, 0, half_w, half_h, "左上"),
        (half_w, 0, half_w, half_h, "右上"),
        (0, half_h, half_w, half_h, "左下"),
        (half_w, half_h, half_w, half_h, "右下")
    ]
    
    print(f"\n将屏幕分成4个区域进行截图...")
    time.sleep(1)
    
    for i, (x, y, w, h, name) in enumerate(regions, 1):
        img = screenshot.capture_region(x, y, w, h, f"region_{i}_{name}.png")
        print(f"  区域{i}({name}): {img.size}")


def main():
    """运行所有示例"""
    print("\n🎯 屏幕截图工具 - 使用示例")
    print("=" * 60)
    print("\n提示: 每个示例会等待1秒后执行截图")
    print("      您可以切换到想要截图的窗口")
    
    try:
        # 运行所有示例
        example_basic()
        example_region()
        example_center()
        example_bbox()
        example_quick()
        example_no_save()
        example_multiple()
        
        print("\n" + "=" * 60)
        print("✅ 所有示例执行完成！")
        print("=" * 60)
        print("\n生成的文件:")
        print("  - screenshots/       # 默认截图目录")
        print("  - batch_screenshots/ # 批量截图目录")
        print("  - *.png             # 各种示例截图")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

