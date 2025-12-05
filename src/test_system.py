"""
系统测试脚本 - 快速验证安装和功能
"""

import sys
from pathlib import Path


def test_dependencies():
    """测试依赖库"""
    print("=" * 50)
    print("测试1: 检查依赖库")
    print("=" * 50)
    
    dependencies = {
        'cv2': 'opencv-python',
        'numpy': 'numpy',
        'pandas': 'pandas',
        'PIL': 'Pillow',
        'paddleocr': 'paddleocr'
    }
    
    all_ok = True
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"✓ {package:20s} - 已安装")
        except ImportError:
            print(f"✗ {package:20s} - 未安装")
            all_ok = False
    
    return all_ok


def test_recognizer():
    """测试识别器初始化"""
    print("\n" + "=" * 50)
    print("测试2: 初始化识别器")
    print("=" * 50)
    
    try:
        from chart_recognizer import chartRecognizer
        recognizer = chartRecognizer(use_gpu=False)
        print("✓ chartRecognizer 初始化成功")
        return True
    except Exception as e:
        print(f"✗ chartRecognizer 初始化失败: {e}")
        return False


def test_data_structures():
    """测试数据结构"""
    print("\n" + "=" * 50)
    print("测试3: 数据结构")
    print("=" * 50)
    
    try:
        from chart_recognizer import DataPoint, RecognitionResult
        
        # 测试DataPoint
        DataPoint = DataPoint(
            date='2024-01-01',
            open=100.0,
            high=105.0,
            low=98.0,
            close=103.0
        )
        assert DataPoint.to_dict()['open'] == 100.0
        print("✓ DataPoint 数据结构正常")
        
        # 测试RecognitionResult
        result = RecognitionResult(
            image_name='test.png',
            data_points=[DataPoint],
            confidence=0.95
        )
        assert len(result.data_points) == 1
        print("✓ RecognitionResult 数据结构正常")
        
        return True
    except Exception as e:
        print(f"✗ 数据结构测试失败: {e}")
        return False


def test_utils():
    """测试工具函数"""
    print("\n" + "=" * 50)
    print("测试4: 工具函数")
    print("=" * 50)
    
    try:
        from utils import validate_DataPoint_data
        from chart_recognizer import DataPoint
        
        # 测试数据验证
        data_points = [
            DataPoint(date='2024-01-01', open=100, high=105, low=98, close=103)
        ]
        is_valid, errors = validate_DataPoint_data(data_points)
        
        assert is_valid == True
        print("✓ 数据验证功能正常")
        
        return True
    except Exception as e:
        print(f"✗ 工具函数测试失败: {e}")
        return False


def create_test_image():
    """创建测试用图形"""
    print("\n" + "=" * 50)
    print("测试5: 创建测试图片")
    print("=" * 50)
    
    try:
        import cv2
        import numpy as np
        
        # 创建一个简单的测试图片
        img = np.ones((600, 800, 3), dtype=np.uint8) * 255
        
        # 绘制坐标轴
        cv2.line(img, (50, 50), (50, 500), (0, 0, 0), 2)  # Y轴
        cv2.line(img, (50, 500), (750, 500), (0, 0, 0), 2)  # X轴
        
        # 绘制几根简单的图形元素（用于测试）
        positions = [100, 200, 300, 400, 500, 600, 700]
        for i, x in enumerate(positions):
            # 随机生成OHLC
            base_price = 300 - i * 10
            is_red = i % 2 == 0
            
            if is_red:
                # 红色图形元素（涨）
                body_top = base_price - 10
                body_bottom = base_price + 10
                shadow_top = base_price - 20
                shadow_bottom = base_price + 15
                color = (0, 0, 255)  # 红色
            else:
                # 绿色图形元素（跌）
                body_top = base_price + 10
                body_bottom = base_price - 10
                shadow_top = base_price + 20
                shadow_bottom = base_price - 15
                color = (0, 255, 0)  # 绿色
            
            # 绘制影线
            cv2.line(img, (x, shadow_top), (x, shadow_bottom), (0, 0, 0), 1)
            
            # 绘制实体
            cv2.rectangle(img, (x-5, body_top), (x+5, body_bottom), color, -1)
        
        # 添加价格标签
        cv2.putText(img, '100.00', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        cv2.putText(img, '200.00', (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        cv2.putText(img, '300.00', (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        
        # 保存测试图片
        test_dir = Path('test_data')
        test_dir.mkdir(exist_ok=True)
        test_image_path = test_dir / 'test_chart.png'
        
        cv2.imwrite(str(test_image_path), img)
        print(f"✓ 测试图片已创建: {test_image_path}")
        
        return str(test_image_path)
    except Exception as e:
        print(f"✗ 创建测试图片失败: {e}")
        return None


def test_recognition(image_path):
    """测试识别功能"""
    print("\n" + "=" * 50)
    print("测试6: 识别功能")
    print("=" * 50)
    
    if not image_path or not Path(image_path).exists():
        print("⚠ 跳过识别测试（无测试图片）")
        return False
    
    try:
        from chart_recognizer import chartRecognizer
        
        recognizer = chartRecognizer(debug=True)
        result = recognizer.recognize(image_path)
        
        print(f"图片: {result.image_name}")
        print(f"识别到 {len(result.data_points)} 根图形元素")
        print(f"置信度: {result.confidence}")
        
        if result.error:
            print(f"错误: {result.error}")
            return False
        
        print("✓ 识别功能正常")
        return True
        
    except Exception as e:
        print(f"✗ 识别测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    print("\n" + "="*50)
    print("图形识别系统 - 功能测试")
    print("="*50 + "\n")
    
    results = []
    
    # 依赖测试
    results.append(("依赖库检查", test_dependencies()))
    
    # 识别器测试
    results.append(("识别器初始化", test_recognizer()))
    
    # 数据结构测试
    results.append(("数据结构", test_data_structures()))
    
    # 工具函数测试
    results.append(("工具函数", test_utils()))
    
    # 创建测试图片
    test_image = create_test_image()
    
    # 识别测试
    if test_image:
        results.append(("识别功能", test_recognition(test_image)))
    
    # 汇总结果
    print("\n" + "="*50)
    print("测试总结")
    print("="*50)
    
    for test_name, passed in results:
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"{test_name:20s}: {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统已就绪。")
        print("\n下一步:")
        print("  1. 准备您的图形截图")
        print("  2. 使用 python cli.py -i your_image.png 开始识别")
        print("  3. 查看 example.py 了解更多用法")
    else:
        print("\n⚠️  部分测试失败，请检查安装。")
        print("参考 INSTALL.md 排查问题")
    
    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

