"""
图形元素图识别使用示例
"""

from chart_recognizer import ChartRecognizer
import json


def example_single_image():
    """示例1: 识别单张图片"""
    print("=" * 50)
    print("示例1: 识别单张图形元素图")
    print("=" * 50)
    
    recognizer = ChartRecognizer(debug=True)
    
    # 替换为您的图片路径
    image_path = 'test_chart.png'
    
    result = recognizer.recognize(image_path)
    
    print(f"\n图片: {result.image_name}")
    print(f"股票代码: {result.symbol or '未识别'}")
    print(f"置信度: {result.confidence}")
    print(f"识别到 {len(result.data_points)} 根图形元素")
    
    if result.data_points:
        print("\n最近5根图形元素数据:")
        for i, DataPoint in enumerate(result.data_points[-5:], 1):
            print(f"  {i}. 日期: {DataPoint.date}")
            print(f"     开盘: {DataPoint.open}, 最高: {DataPoint.high}")
            print(f"     最低: {DataPoint.low}, 收盘: {DataPoint.close}")
    
    # 导出为JSON
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)
    
    print("\n结果已保存到 result.json")


def example_batch_process():
    """示例2: 批量处理"""
    print("\n" + "=" * 50)
    print("示例2: 批量处理图形元素图")
    print("=" * 50)
    
    recognizer = ChartRecognizer()
    
    # 批量处理文件夹中的所有图片
    results = recognizer.batch_process(
        input_dir='screenshots',      # 输入文件夹
        output_dir='output',           # 输出文件夹
        output_formats=['json', 'csv', 'excel']  # 输出格式
    )
    
    print(f"\n共处理 {len(results)} 张图片")
    print(f"成功: {sum(1 for r in results if r.confidence > 0.5)} 张")
    
    # 查看结果
    for result in results:
        if result.confidence > 0.8:
            print(f"✓ {result.image_name}: {len(result.data_points)} 根图形元素")
        elif result.confidence > 0.5:
            print(f"⚠ {result.image_name}: {len(result.data_points)} 根图形元素 (置信度: {result.confidence})")
        else:
            print(f"✗ {result.image_name}: 识别失败 ({result.error})")


def example_custom_processing():
    """示例3: 自定义处理"""
    print("\n" + "=" * 50)
    print("示例3: 自定义数据处理")
    print("=" * 50)
    
    recognizer = ChartRecognizer()
    result = recognizer.recognize('test_chart.png')
    
    if result.data_points:
        # 计算技术指标
        closes = [c.close for c in result.data_points]
        
        # 简单移动平均线 MA5
        if len(closes) >= 5:
            ma5 = sum(closes[-5:]) / 5
            print(f"MA5: {ma5:.2f}")
        
        # 涨跌幅
        if len(closes) >= 2:
            change = (closes[-1] - closes[-2]) / closes[-2] * 100
            print(f"涨跌幅: {change:+.2f}%")
        
        # 最高价和最低价
        highs = [c.high for c in result.data_points]
        lows = [c.low for c in result.data_points]
        print(f"期间最高: {max(highs):.2f}")
        print(f"期间最低: {min(lows):.2f}")
        
        # 导出为pandas DataFrame
        import pandas as pd
        df = pd.DataFrame([
            {
                'date': c.date,
                'open': c.open,
                'high': c.high,
                'low': c.low,
                'close': c.close
            }
            for c in result.data_points
        ])
        
        print("\nDataFrame预览:")
        print(df.head())
        
        # 保存为CSV
        df.to_csv('chart_data.csv', index=False)
        print("\n数据已保存到 chart_data.csv")


def main():
    """运行所有示例"""
    print("图形元素图识别系统 - 使用示例\n")
    
    # 提示用户
    print("请确保您已准备好测试图片:")
    print("  - 单张图片: test_chart.png")
    print("  - 批量图片: screenshots/ 文件夹")
    print()
    
    choice = input("选择示例 (1: 单张图片, 2: 批量处理, 3: 自定义处理, a: 全部): ")
    
    if choice == '1':
        example_single_image()
    elif choice == '2':
        example_batch_process()
    elif choice == '3':
        example_custom_processing()
    elif choice.lower() == 'a':
        example_single_image()
        example_batch_process()
        example_custom_processing()
    else:
        print("无效选择")


if __name__ == '__main__':
    main()

