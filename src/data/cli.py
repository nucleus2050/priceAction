"""
图形元素图识别命令行工具
"""

import argparse
import sys
from pathlib import Path
from chart_recognizer import ChartRecognizer
import json


def main():
    parser = argparse.ArgumentParser(
        description='图形元素图识别工具 - 批量提取OHLC数据',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 识别单张图片
  python cli.py -i chart.png
  
  # 批量处理文件夹
  python cli.py -i screenshots/ -o output/
  
  # 指定输出格式
  python cli.py -i screenshots/ -o output/ -f json csv excel
  
  # 开启GPU加速和调试模式
  python cli.py -i screenshots/ -o output/ --gpu --debug
        """
    )
    
    parser.add_argument('-i', '--input', required=True,
                       help='输入文件或文件夹路径')
    parser.add_argument('-o', '--output', default='output',
                       help='输出文件夹路径（默认: output）')
    parser.add_argument('-f', '--formats', nargs='+',
                       choices=['json', 'csv', 'excel'],
                       default=['json', 'csv', 'excel'],
                       help='输出格式（默认: 全部）')
    parser.add_argument('--gpu', action='store_true',
                       help='使用GPU加速')
    parser.add_argument('--debug', action='store_true',
                       help='开启调试模式（保存中间处理图片）')
    
    args = parser.parse_args()
    
    # 初始化识别器
    print("正在初始化图形元素图识别器...")
    recognizer = ChartRecognizer(use_gpu=args.gpu, debug=args.debug)
    
    input_path = Path(args.input)
    
    # 判断是单个文件还是文件夹
    if input_path.is_file():
        # 单个文件
        print(f"识别图片: {input_path}")
        result = recognizer.recognize(str(input_path))
        
        # 打印结果
        print("\n" + "="*50)
        print(f"图片: {result.image_name}")
        print(f"股票代码: {result.symbol or '未识别'}")
        print(f"置信度: {result.confidence}")
        print(f"图形元素数量: {len(result.data_points)}")
        
        if result.error:
            print(f"错误: {result.error}")
        elif result.data_points:
            print("\n前3根图形元素数据:")
            for i, DataPoint in enumerate(result.data_points[:3]):
                print(f"  {i+1}. {DataPoint.date}: O={DataPoint.open} H={DataPoint.high} L={DataPoint.low} C={DataPoint.close}")
        
        # 保存结果
        output_path = Path(args.output)
        output_path.mkdir(parents=True, exist_ok=True)
        
        json_file = output_path / f"{input_path.stem}_result.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)
        
        print(f"\n结果已保存到: {json_file}")
        
    elif input_path.is_dir():
        # 文件夹批量处理
        results = recognizer.batch_process(
            str(input_path),
            args.output,
            args.formats
        )
        
        # 显示详细统计
        print("\n" + "="*50)
        print("处理统计:")
        total = len(results)
        high_conf = sum(1 for r in results if r.confidence > 0.8)
        medium_conf = sum(1 for r in results if 0.5 <= r.confidence <= 0.8)
        low_conf = sum(1 for r in results if r.confidence < 0.5)
        
        print(f"  总计: {total} 张")
        print(f"  高置信度 (>0.8): {high_conf} 张")
        print(f"  中置信度 (0.5-0.8): {medium_conf} 张")
        print(f"  低置信度 (<0.5): {low_conf} 张")
        
        if low_conf > 0:
            print("\n低置信度图片:")
            for r in results:
                if r.confidence < 0.5:
                    print(f"  - {r.image_name}: {r.confidence} ({r.error or '数据质量差'})")
    
    else:
        print(f"错误: 路径不存在 - {input_path}")
        sys.exit(1)
    
    print("\n✅ 完成!")


if __name__ == '__main__':
    main()

