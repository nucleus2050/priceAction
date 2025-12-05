"""
工具函数集合
"""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple
import matplotlib.pyplot as plt


def visualize_chart(data_points: List, save_path: str = None, show: bool = True):
    """
    可视化图形元素数据
    
    Args:
        data_points: 图形元素数据列表
        save_path: 保存路径
        show: 是否显示
    """
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for i, DataPoint in enumerate(data_points):
        # 计算颜色
        color = 'red' if DataPoint.close >= DataPoint.open else 'green'
        
        # 绘制实体
        body_height = abs(DataPoint.close - DataPoint.open)
        body_bottom = min(DataPoint.open, DataPoint.close)
        rect = Rectangle((i-0.3, body_bottom), 0.6, body_height, 
                         facecolor=color, edgecolor='black', alpha=0.8)
        ax.add_patch(rect)
        
        # 绘制影线
        ax.plot([i, i], [DataPoint.low, DataPoint.high], color='black', linewidth=1)
    
    ax.set_xlabel('图形元素序号')
    ax.set_ylabel('价格')
    ax.set_title('图形元素图')
    ax.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    
    plt.close()


def validate_DataPoint_data(data_points: List) -> Tuple[bool, List[str]]:
    """
    验证图形元素数据合理性
    
    Returns:
        (is_valid, error_messages)
    """
    errors = []
    
    for i, DataPoint in enumerate(data_points):
        # 检查价格关系
        if DataPoint.high < DataPoint.low:
            errors.append(f"图形元素{i}: 最高价 < 最低价")
        
        if DataPoint.high < DataPoint.open or DataPoint.high < DataPoint.close:
            errors.append(f"图形元素{i}: 最高价小于开盘价或收盘价")
        
        if DataPoint.low > DataPoint.open or DataPoint.low > DataPoint.close:
            errors.append(f"图形元素{i}: 最低价大于开盘价或收盘价")
        
        # 检查价格范围
        if any(p <= 0 for p in [DataPoint.open, DataPoint.high, DataPoint.low, DataPoint.close]):
            errors.append(f"图形元素{i}: 价格不能为负数或零")
    
    return len(errors) == 0, errors


def resize_image(image_path: str, max_width: int = 1920, max_height: int = 1080) -> str:
    """
    调整图片大小以优化处理速度
    
    Args:
        image_path: 图片路径
        max_width: 最大宽度
        max_height: 最大高度
    
    Returns:
        调整后的图片路径
    """
    img = cv2.imread(image_path)
    if img is None:
        return image_path
    
    h, w = img.shape[:2]
    
    # 计算缩放比例
    scale = min(max_width / w, max_height / h, 1.0)
    
    if scale < 1.0:
        new_w = int(w * scale)
        new_h = int(h * scale)
        img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
        # 保存调整后的图片
        resized_path = str(Path(image_path).with_stem(Path(image_path).stem + '_resized'))
        cv2.imwrite(resized_path, img)
        return resized_path
    
    return image_path


def enhance_image_contrast(image_path: str) -> str:
    """
    增强图片对比度
    
    Args:
        image_path: 图片路径
    
    Returns:
        增强后的图片路径
    """
    img = cv2.imread(image_path)
    if img is None:
        return image_path
    
    # 转换为LAB色彩空间
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # 对L通道应用CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    
    # 合并通道
    enhanced_lab = cv2.merge([l, a, b])
    enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    
    # 保存增强后的图片
    enhanced_path = str(Path(image_path).with_stem(Path(image_path).stem + '_enhanced'))
    cv2.imwrite(enhanced_path, enhanced)
    
    return enhanced_path


def compare_results(result1, result2) -> Dict:
    """
    比较两个识别结果的差异
    
    Args:
        result1: 第一个识别结果
        result2: 第二个识别结果
    
    Returns:
        差异统计信息
    """
    diff = {
        'DataPoint_count_diff': len(result1.data_points) - len(result2.data_points),
        'confidence_diff': result1.confidence - result2.confidence,
        'price_differences': []
    }
    
    # 比较对应位置的图形元素数据
    min_len = min(len(result1.data_points), len(result2.data_points))
    for i in range(min_len):
        c1 = result1.data_points[i]
        c2 = result2.data_points[i]
        
        diff['price_differences'].append({
            'index': i,
            'open_diff': abs(c1.open - c2.open),
            'close_diff': abs(c1.close - c2.close),
            'high_diff': abs(c1.high - c2.high),
            'low_diff': abs(c1.low - c2.low),
        })
    
    return diff


def export_to_tradingview_format(data_points: List, output_file: str):
    """
    导出为TradingView格式（CSV）
    
    Args:
        data_points: 图形元素数据
        output_file: 输出文件路径
    """
    import csv
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['time', 'open', 'high', 'low', 'close', 'volume'])
        
        for DataPoint in data_points:
            # 转换日期为Unix时间戳
            from datetime import datetime
            timestamp = int(datetime.strptime(DataPoint.date, '%Y-%m-%d').timestamp())
            
            writer.writerow([
                timestamp,
                DataPoint.open,
                DataPoint.high,
                DataPoint.low,
                DataPoint.close,
                DataPoint.volume or 0
            ])


def split_images_by_quality(results: List) -> Dict[str, List]:
    """
    根据识别质量分类结果
    
    Args:
        results: 识别结果列表
    
    Returns:
        {'high': [...], 'medium': [...], 'low': [...]}
    """
    categorized = {
        'high': [],      # confidence > 0.8
        'medium': [],    # 0.5 <= confidence <= 0.8
        'low': []        # confidence < 0.5
    }
    
    for result in results:
        if result.confidence > 0.8:
            categorized['high'].append(result)
        elif result.confidence >= 0.5:
            categorized['medium'].append(result)
        else:
            categorized['low'].append(result)
    
    return categorized


def generate_report(results: List, output_file: str = 'report.html'):
    """
    生成HTML格式的识别报告
    
    Args:
        results: 识别结果列表
        output_file: 输出文件路径
    """
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>图形元素图识别报告</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #333; }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            .high {{ color: green; font-weight: bold; }}
            .medium {{ color: orange; }}
            .low {{ color: red; }}
        </style>
    </head>
    <body>
        <h1>图形元素图识别报告</h1>
        <p>总计: {total} 张图片</p>
        <p>高质量: {high_count} 张 | 中等质量: {medium_count} 张 | 低质量: {low_count} 张</p>
        
        <h2>详细结果</h2>
        <table>
            <tr>
                <th>图片名称</th>
                <th>股票代码</th>
                <th>图形元素数量</th>
                <th>置信度</th>
                <th>状态</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """
    
    categorized = split_images_by_quality(results)
    
    rows = []
    for result in results:
        conf_class = 'high' if result.confidence > 0.8 else 'medium' if result.confidence >= 0.5 else 'low'
        status = '✓ 成功' if result.confidence > 0.5 else '✗ 失败'
        
        rows.append(f"""
            <tr>
                <td>{result.image_name}</td>
                <td>{result.symbol or '未识别'}</td>
                <td>{len(result.data_points)}</td>
                <td class="{conf_class}">{result.confidence:.2f}</td>
                <td>{status}</td>
            </tr>
        """)
    
    html_content = html_template.format(
        total=len(results),
        high_count=len(categorized['high']),
        medium_count=len(categorized['medium']),
        low_count=len(categorized['low']),
        rows=''.join(rows)
    )
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"报告已生成: {output_file}")


if __name__ == '__main__':
    print("工具函数库已加载")
    print("可用函数:")
    print("  - visualize_chart(): 可视化图形元素")
    print("  - validate_DataPoint_data(): 验证数据")
    print("  - resize_image(): 调整图片大小")
    print("  - enhance_image_contrast(): 增强对比度")
    print("  - export_to_tradingview_format(): 导出TradingView格式")
    print("  - generate_report(): 生成HTML报告")

