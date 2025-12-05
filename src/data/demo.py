"""
演示脚本 - 创建示例图形并进行识别
用于快速验证系统功能
"""

import cv2
import numpy as np
from pathlib import Path
import json


def create_demo_chart_image(output_path='demo_chart.png'):
    """
    创建一个演示用的图形
    包含完整的坐标轴、刻度和图形元素
    """
    # 创建白色背景
    width, height = 1200, 800
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # 定义区域
    margin_left = 80
    margin_right = 50
    margin_top = 80
    margin_bottom = 100
    
    chart_left = margin_left
    chart_right = width - margin_right
    chart_top = margin_top
    chart_bottom = height - margin_bottom
    
    # 绘制标题
    cv2.putText(img, 'Demo Stock - 600000', (width//2 - 150, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2)
    
    # 绘制坐标轴
    cv2.line(img, (chart_left, chart_top), (chart_left, chart_bottom), (0, 0, 0), 2)  # Y轴
    cv2.line(img, (chart_left, chart_bottom), (chart_right, chart_bottom), (0, 0, 0), 2)  # X轴
    
    # 绘制网格线和价格刻度
    price_min = 95.0
    price_max = 115.0
    price_range = price_max - price_min
    num_price_lines = 5
    
    for i in range(num_price_lines):
        y = chart_bottom - int((chart_bottom - chart_top) * i / (num_price_lines - 1))
        price = price_min + price_range * i / (num_price_lines - 1)
        
        # 网格线
        cv2.line(img, (chart_left, y), (chart_right, y), (200, 200, 200), 1)
        
        # 价格标签
        cv2.putText(img, f'{price:.2f}', (10, y + 5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    
    # 生成图形元素数据（20根图形元素）
    num_data_points = 20
    DataPoint_width = (chart_right - chart_left - 100) // num_data_points
    start_x = chart_left + 50
    
    # 模拟价格数据
    base_price = 105.0
    prices = []
    
    for i in range(num_data_points):
        # 生成随机OHLC
        change = np.random.randn() * 2
        open_price = base_price + change
        close_price = open_price + np.random.randn() * 3
        high_price = max(open_price, close_price) + abs(np.random.randn()) * 2
        low_price = min(open_price, close_price) - abs(np.random.randn()) * 2
        
        prices.append({
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'close': close_price
        })
        
        base_price = close_price  # 下一根图形元素从这根的收盘价开始
    
    # 绘制图形元素
    for i, price_data in enumerate(prices):
        x = start_x + i * DataPoint_width + DataPoint_width // 2
        
        # 计算像素坐标
        def price_to_y(price):
            ratio = (price - price_min) / price_range
            return chart_bottom - int((chart_bottom - chart_top) * ratio)
        
        open_y = price_to_y(price_data['open'])
        close_y = price_to_y(price_data['close'])
        high_y = price_to_y(price_data['high'])
        low_y = price_to_y(price_data['low'])
        
        # 判断涨跌
        is_up = price_data['close'] >= price_data['open']
        color = (0, 0, 255) if is_up else (0, 255, 0)  # 红涨绿跌
        
        # 绘制影线
        cv2.line(img, (x, high_y), (x, low_y), (0, 0, 0), 1)
        
        # 绘制实体
        body_top = min(open_y, close_y)
        body_bottom = max(open_y, close_y)
        body_height = max(body_bottom - body_top, 2)  # 至少2像素高
        
        cv2.rectangle(img, (x - 6, body_top), (x + 6, body_bottom), color, -1)
        cv2.rectangle(img, (x - 6, body_top), (x + 6, body_bottom), (0, 0, 0), 1)
    
    # 绘制日期标签
    dates = ['01-01', '01-05', '01-10', '01-15', '01-20']
    for i, date in enumerate(dates):
        x = start_x + int(i * (num_data_points / (len(dates) - 1)) * DataPoint_width)
        cv2.putText(img, date, (x - 20, chart_bottom + 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    # 添加成交量（简化版）
    volume_height = 80
    volume_bottom = height - 10
    volume_top = volume_bottom - volume_height
    
    cv2.putText(img, 'Volume', (10, volume_top - 5),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 1)
    
    for i in range(num_data_points):
        x = start_x + i * DataPoint_width + DataPoint_width // 2
        vol_height = int(np.random.rand() * volume_height * 0.8)
        color = (0, 0, 255) if prices[i]['close'] >= prices[i]['open'] else (0, 255, 0)
        cv2.rectangle(img, (x - 4, volume_bottom - vol_height), 
                     (x + 4, volume_bottom), color, -1)
    
    # 保存图片
    cv2.imwrite(output_path, img)
    print(f"✓ 演示图形已创建: {output_path}")
    
    return output_path, prices


def run_demo():
    """运行完整演示"""
    print("=" * 60)
    print("图形识别系统 - 演示程序")
    print("=" * 60)
    
    # 1. 创建演示图片
    print("\n步骤1: 创建演示图形...")
    demo_image, true_prices = create_demo_chart_image('demo_chart.png')
    
    # 2. 识别图片
    print("\n步骤2: 识别图形...")
    try:
        from chart_recognizer import ChartRecognizer
        
        recognizer = ChartRecognizer(debug=True)
        result = recognizer.recognize(demo_image)
        
        print(f"\n识别结果:")
        print(f"  - 图片: {result.image_name}")
        print(f"  - 股票代码: {result.symbol or '600000 (演示)'}")
        print(f"  - 图形元素数量: {len(result.data_points)}")
        print(f"  - 置信度: {result.confidence:.2f}")
        
        if result.error:
            print(f"  - 错误: {result.error}")
        
        # 3. 显示前5根图形元素
        if result.data_points:
            print(f"\n前5根图形元素数据:")
            print(f"{'序号':<6} {'日期':<12} {'开盘':<8} {'最高':<8} {'最低':<8} {'收盘':<8}")
            print("-" * 60)
            for i, DataPoint in enumerate(result.data_points[:5], 1):
                print(f"{i:<6} {DataPoint.date:<12} {DataPoint.open:<8.2f} "
                      f"{DataPoint.high:<8.2f} {DataPoint.low:<8.2f} {DataPoint.close:<8.2f}")
        
        # 4. 保存结果
        print("\n步骤3: 保存识别结果...")
        output_dir = Path('demo_output')
        output_dir.mkdir(exist_ok=True)
        
        # JSON格式
        json_file = output_dir / 'demo_result.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)
        print(f"  ✓ JSON结果: {json_file}")
        
        # CSV格式
        if result.data_points:
            import pandas as pd
            df = pd.DataFrame([c.to_dict() for c in result.data_points])
            csv_file = output_dir / 'demo_result.csv'
            df.to_csv(csv_file, index=False, encoding='utf-8-sig')
            print(f"  ✓ CSV结果: {csv_file}")
        
        # 5. 生成可视化
        print("\n步骤4: 生成可视化...")
        try:
            from utils import visualize_chart
            if result.data_points:
                viz_file = output_dir / 'demo_visualization.png'
                visualize_chart(result.data_points, str(viz_file), show=False)
                print(f"  ✓ 可视化图表: {viz_file}")
        except Exception as e:
            print(f"  ⚠ 可视化失败: {e}")
        
        print("\n" + "=" * 60)
        print("✅ 演示完成！")
        print("=" * 60)
        print("\n生成的文件:")
        print(f"  - 演示图片: demo_chart.png")
        print(f"  - 识别结果: demo_output/demo_result.json")
        print(f"  - CSV数据: demo_output/demo_result.csv")
        print(f"  - 调试图片: debug_*.png")
        print("\n下一步:")
        print("  1. 查看生成的图片和结果")
        print("  2. 准备您自己的图形截图")
        print("  3. 使用 python cli.py -i your_image.png 开始识别")
        
    except ImportError:
        print("\n❌ 错误: 无法导入 chart_recognizer")
        print("请先运行: pip install -r requirements.txt")
    except Exception as e:
        print(f"\n❌ 识别失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    run_demo()

