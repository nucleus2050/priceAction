"""
多屏幕截图示例
演示如何在多显示器环境下使用截图工具
"""

from Screenshot import Screenshot
import time


def display_monitors_info():
    """显示所有显示器信息"""
    print("\n" + "=" * 60)
    print("显示器信息")
    print("=" * 60)
    
    screenshot = Screenshot()
    monitors = screenshot.get_monitors_info()
    
    print(f"\n检测到 {len(monitors)} 个显示器:\n")
    
    for monitor in monitors:
        primary = " ⭐ (主显示器)" if monitor.get('is_primary') else ""
        print(f"显示器 {monitor['index']}{primary}")
        print(f"  位置: ({monitor['x']}, {monitor['y']})")
        print(f"  尺寸: {monitor['width']} x {monitor['height']}")
        if 'name' in monitor:
            print(f"  名称: {monitor['name']}")
        print()
    
    return monitors


def capture_primary_monitor():
    """捕获主显示器"""
    print("\n" + "=" * 60)
    print("示例1: 捕获主显示器")
    print("=" * 60)
    
    screenshot = Screenshot(save_dir="multi_monitor_screenshots")
    
    print("\n捕获主显示器（显示器0）...")
    time.sleep(1)
    img = screenshot.capture_monitor(0, "primary_monitor.png")
    print(f"尺寸: {img.size}")


def capture_all_monitors_separately():
    """分别捕获所有显示器"""
    print("\n" + "=" * 60)
    print("示例2: 分别捕获所有显示器")
    print("=" * 60)
    
    screenshot = Screenshot(save_dir="multi_monitor_screenshots")
    monitors = screenshot.get_monitors_info()
    
    if len(monitors) == 1:
        print("\n只检测到一个显示器，跳过此示例")
        return
    
    print(f"\n分别捕获 {len(monitors)} 个显示器...")
    time.sleep(1)
    
    images = screenshot.capture_all_monitors()
    
    print(f"\n成功捕获 {len(images)} 个显示器的截图")
    for i, img in enumerate(images):
        print(f"  显示器{i}: {img.size}")


def capture_all_monitors_as_one():
    """将所有显示器作为一个大图捕获"""
    print("\n" + "=" * 60)
    print("示例3: 捕获所有显示器（作为一个整体）")
    print("=" * 60)
    
    screenshot = Screenshot(save_dir="multi_monitor_screenshots")
    monitors = screenshot.get_monitors_info()
    
    if len(monitors) == 1:
        print("\n只检测到一个显示器，跳过此示例")
        return
    
    print("\n捕获所有显示器（all_screens=True）...")
    time.sleep(1)
    
    # 主屏幕尺寸
    single_width, single_height = screenshot.get_screen_size(all_screens=False)
    print(f"主屏幕尺寸: {single_width}x{single_height}")
    
    # 所有屏幕总尺寸
    img = screenshot.capture_fullscreen(save_path="all_monitors.png", all_screens=True)
    print(f"所有屏幕总尺寸: {img.size}")


def capture_specific_monitor_region():
    """捕获特定显示器的指定区域"""
    print("\n" + "=" * 60)
    print("示例4: 捕获特定显示器的指定区域")
    print("=" * 60)
    
    screenshot = Screenshot(save_dir="multi_monitor_screenshots")
    monitors = screenshot.get_monitors_info()
    
    # 选择第一个显示器
    monitor = monitors[0]
    
    print(f"\n在显示器0上捕获中心区域...")
    time.sleep(1)
    
    # 计算该显示器中心区域
    capture_width = 800
    capture_height = 600
    x = monitor['x'] + (monitor['width'] - capture_width) // 2
    y = monitor['y'] + (monitor['height'] - capture_height) // 2
    
    img = screenshot.capture_region(x, y, capture_width, capture_height,
                                   "monitor0_center.png")
    print(f"捕获区域尺寸: {img.size}")
    
    # 如果有第二个显示器，也捕获其中心区域
    if len(monitors) > 1:
        monitor = monitors[1]
        print(f"\n在显示器1上捕获中心区域...")
        time.sleep(1)
        
        x = monitor['x'] + (monitor['width'] - capture_width) // 2
        y = monitor['y'] + (monitor['height'] - capture_height) // 2
        
        img = screenshot.capture_region(x, y, capture_width, capture_height,
                                       "monitor1_center.png")
        print(f"捕获区域尺寸: {img.size}")


def capture_cross_monitor_region():
    """捕获跨越多个显示器的区域"""
    print("\n" + "=" * 60)
    print("示例5: 捕获跨越多个显示器的区域")
    print("=" * 60)
    
    screenshot = Screenshot(save_dir="multi_monitor_screenshots")
    monitors = screenshot.get_monitors_info()
    
    if len(monitors) == 1:
        print("\n只检测到一个显示器，跳过此示例")
        return
    
    print("\n捕获跨越显示器0和显示器1的区域...")
    time.sleep(1)
    
    # 假设显示器水平排列，捕获跨越边界的区域
    monitor0 = monitors[0]
    monitor1 = monitors[1]
    
    # 从显示器0的右侧开始，到显示器1的左侧
    left = monitor0['x'] + monitor0['width'] - 400
    top = monitor0['y'] + 200
    right = monitor1['x'] + 400
    bottom = top + 600
    
    img = screenshot.capture_bbox(left, top, right, bottom, "cross_monitor.png")
    print(f"跨显示器区域尺寸: {img.size}")


def create_monitor_layout_screenshot():
    """创建显示器布局可视化"""
    print("\n" + "=" * 60)
    print("示例6: 显示器布局可视化")
    print("=" * 60)
    
    screenshot = Screenshot()
    monitors = screenshot.get_monitors_info()
    
    print("\n显示器布局:")
    print("```")
    
    # 找出所有显示器的边界
    min_x = min(m['x'] for m in monitors)
    max_x = max(m['x'] + m['width'] for m in monitors)
    min_y = min(m['y'] for m in monitors)
    max_y = max(m['y'] + m['height'] for m in monitors)
    
    print(f"总虚拟屏幕空间: {max_x - min_x} x {max_y - min_y}")
    print(f"范围: X({min_x} to {max_x}), Y({min_y} to {max_y})")
    print()
    
    for i, monitor in enumerate(monitors):
        primary = " (主)" if monitor.get('is_primary') else ""
        print(f"[显示器{i}{primary}]")
        print(f"  左上角: ({monitor['x']}, {monitor['y']})")
        print(f"  右下角: ({monitor['x'] + monitor['width']}, "
              f"{monitor['y'] + monitor['height']})")
        print()
    
    print("```")


def main():
    """运行所有多屏幕示例"""
    print("\n" + "=" * 70)
    print(" " * 20 + "多屏幕截图工具演示")
    print("=" * 70)
    
    try:
        # 显示显示器信息
        monitors = display_monitors_info()
        
        # 根据显示器数量选择示例
        if len(monitors) == 1:
            print("💡 检测到单显示器环境")
            print("   部分多显示器示例将被跳过\n")
        else:
            print(f"💡 检测到 {len(monitors)} 个显示器环境")
            print("   将运行完整的多显示器示例\n")
        
        input("按 Enter 键开始演示...")
        
        # 运行示例
        capture_primary_monitor()
        capture_all_monitors_separately()
        capture_all_monitors_as_one()
        capture_specific_monitor_region()
        capture_cross_monitor_region()
        create_monitor_layout_screenshot()
        
        print("\n" + "=" * 70)
        print("✅ 所有示例执行完成！")
        print("=" * 70)
        print("\n生成的文件:")
        print("  - multi_monitor_screenshots/  # 多屏幕截图目录")
        print("  - primary_monitor.png         # 主显示器截图")
        print("  - all_monitors.png           # 所有显示器（整体）")
        print("  - monitor_*.png              # 各个显示器截图")
        print("  - cross_monitor.png          # 跨显示器截图（如果适用）")
        
        print("\n💡 提示:")
        if len(monitors) == 1:
            print("  - 连接第二个显示器以测试完整的多屏幕功能")
        print("  - 使用 all_screens=True 参数可捕获所有显示器")
        print("  - 坐标系统中，多个显示器形成一个大的虚拟屏幕空间")
        
    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

