"""
快速测试多屏幕功能
"""

from Screenshot import Screenshot


def test_basic():
    """测试基础功能"""
    print("=" * 60)
    print("测试1: 基础功能")
    print("=" * 60)
    
    screenshot = Screenshot()
    
    # 获取屏幕尺寸
    width, height = screenshot.get_screen_size()
    print(f"✓ 主屏幕尺寸: {width}x{height}")
    
    # 全屏截图
    img = screenshot.capture_fullscreen()
    print(f"✓ 全屏截图: {img.size}")
    
    return True


def test_monitor_detection():
    """测试显示器检测"""
    print("\n" + "=" * 60)
    print("测试2: 显示器检测")
    print("=" * 60)
    
    screenshot = Screenshot()
    monitors = screenshot.get_monitors_info()
    
    print(f"✓ 检测到 {len(monitors)} 个显示器")
    
    for monitor in monitors:
        primary = " (主)" if monitor.get('is_primary') else ""
        print(f"  - 显示器{monitor['index']}{primary}: "
              f"{monitor['width']}x{monitor['height']} "
              f"at ({monitor['x']}, {monitor['y']})")
    
    return len(monitors) > 0


def test_single_monitor_capture():
    """测试单个显示器捕获"""
    print("\n" + "=" * 60)
    print("测试3: 单个显示器捕获")
    print("=" * 60)
    
    screenshot = Screenshot()
    monitors = screenshot.get_monitors_info()
    
    # 捕获主显示器
    img = screenshot.capture_monitor(0)
    print(f"✓ 捕获显示器0: {img.size}")
    
    # 如果有多个显示器，捕获第二个
    if len(monitors) > 1:
        img = screenshot.capture_monitor(1)
        print(f"✓ 捕获显示器1: {img.size}")
    
    return True


def test_all_screens():
    """测试所有屏幕捕获"""
    print("\n" + "=" * 60)
    print("测试4: 所有屏幕捕获")
    print("=" * 60)
    
    screenshot = Screenshot()
    monitors = screenshot.get_monitors_info()
    
    # 单屏幕尺寸
    single_width, single_height = screenshot.get_screen_size(all_screens=False)
    print(f"✓ 主屏幕: {single_width}x{single_height}")
    
    # 所有屏幕尺寸
    all_width, all_height = screenshot.get_screen_size(all_screens=True)
    print(f"✓ 所有屏幕: {all_width}x{all_height}")
    
    if len(monitors) > 1:
        # 捕获所有屏幕
        img = screenshot.capture_fullscreen(all_screens=True)
        print(f"✓ 所有屏幕截图: {img.size}")
    
    return True


def test_all_monitors_separately():
    """测试分别捕获所有显示器"""
    print("\n" + "=" * 60)
    print("测试5: 分别捕获所有显示器")
    print("=" * 60)
    
    screenshot = Screenshot()
    monitors = screenshot.get_monitors_info()
    
    if len(monitors) == 1:
        print("⚠️  只有一个显示器，跳过此测试")
        return True
    
    images = screenshot.capture_all_monitors()
    print(f"✓ 捕获了 {len(images)} 个显示器")
    
    for i, img in enumerate(images):
        print(f"  - 显示器{i}: {img.size}")
    
    return len(images) == len(monitors)


def test_region_on_monitor():
    """测试在特定显示器上捕获区域"""
    print("\n" + "=" * 60)
    print("测试6: 特定显示器区域捕获")
    print("=" * 60)
    
    screenshot = Screenshot()
    monitors = screenshot.get_monitors_info()
    
    # 在主显示器中心捕获区域
    monitor = monitors[0]
    x = monitor['x'] + 100
    y = monitor['y'] + 100
    
    img = screenshot.capture_region(x, y, 400, 300)
    print(f"✓ 显示器0区域: {img.size}")
    
    # 如果有第二个显示器
    if len(monitors) > 1:
        monitor = monitors[1]
        x = monitor['x'] + 100
        y = monitor['y'] + 100
        
        img = screenshot.capture_region(x, y, 400, 300)
        print(f"✓ 显示器1区域: {img.size}")
    
    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "🧪 " + "=" * 58)
    print("   多屏幕功能测试套件")
    print("=" * 60 + "\n")
    
    tests = [
        ("基础功能", test_basic),
        ("显示器检测", test_monitor_detection),
        ("单显示器捕获", test_single_monitor_capture),
        ("所有屏幕捕获", test_all_screens),
        ("分别捕获", test_all_monitors_separately),
        ("区域捕获", test_region_on_monitor),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result, None))
        except Exception as e:
            results.append((name, False, str(e)))
            print(f"❌ 测试失败: {e}")
    
    # 显示结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for name, result, error in results:
        if result:
            print(f"✅ {name}: 通过")
            passed += 1
        else:
            print(f"❌ {name}: 失败")
            if error:
                print(f"   错误: {error}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"总计: {passed + failed} 个测试")
    print(f"✅ 通过: {passed}")
    print(f"❌ 失败: {failed}")
    print("=" * 60)
    
    # 显示环境信息
    screenshot = Screenshot()
    monitors = screenshot.get_monitors_info()
    
    print("\n📊 环境信息:")
    print(f"  显示器数量: {len(monitors)}")
    
    if len(monitors) == 1:
        print("\n💡 提示: 连接第二个显示器可以测试更多功能")
    else:
        print(f"\n✨ 多显示器环境已就绪！")
    
    return passed, failed


if __name__ == "__main__":
    try:
        passed, failed = run_all_tests()
        exit(0 if failed == 0 else 1)
    except KeyboardInterrupt:
        print("\n\n测试已取消")
        exit(1)
    except Exception as e:
        print(f"\n❌ 测试套件错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

