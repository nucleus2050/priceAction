"""
配置文件 - 可根据需要调整参数
"""

# OCR配置
OCR_CONFIG = {
    'use_angle_cls': True,      # 是否使用角度分类
    'lang': 'ch',               # 语言：'ch'中文, 'en'英文
    'use_gpu': False,           # 是否使用GPU
    'show_log': False,          # 是否显示日志
    'det_db_thresh': 0.3,       # 检测阈值
    'det_db_box_thresh': 0.5,   # 框选阈值
}

# 图像预处理配置
IMAGE_PROCESSING = {
    'denoise_strength': 10,     # 去噪强度 (5-15)
    'binary_block_size': 11,    # 二值化块大小 (奇数)
    'binary_constant': 2,       # 二值化常数
}

# 图形元素检测配置
DataPoint_DETECTION = {
    # 红色图形元素HSV范围
    'red_hsv_lower_1': (0, 50, 50),
    'red_hsv_upper_1': (10, 255, 255),
    'red_hsv_lower_2': (170, 50, 50),
    'red_hsv_upper_2': (180, 255, 255),
    
    # 绿色图形元素HSV范围
    'green_hsv_lower': (40, 50, 50),
    'green_hsv_upper': (80, 255, 255),
    
    # 图形元素过滤参数
    'min_DataPoint_width': 3,      # 最小图形元素宽度（像素）
    'min_DataPoint_height': 5,     # 最小图形元素高度（像素）
}

# 坐标区域配置（相对比例）
CHART_REGIONS = {
    'chart_left': 0.1,          # 图表左边界（比例）
    'chart_right': 0.9,         # 图表右边界（比例）
    'chart_top': 0.1,           # 图表上边界（比例）
    'chart_bottom': 0.8,        # 图表下边界（比例）
    
    'price_axis_left': 0.15,    # 价格轴左侧宽度（比例）
    'price_axis_right': 0.85,   # 价格轴右侧起始（比例）
    'date_axis_top': 0.85,      # 日期轴顶部起始（比例）
}

# 置信度阈值
CONFIDENCE_THRESHOLDS = {
    'high': 0.8,                # 高质量阈值
    'medium': 0.5,              # 中等质量阈值
    'min_data_points': 5,           # 最少图形元素数量
}

# 价格范围验证
PRICE_VALIDATION = {
    'min_price': 0.01,          # 最低价格
    'max_price': 1000000,       # 最高价格
    'max_price_change': 0.5,    # 单根图形元素最大涨跌幅（50%）
}

# 批处理配置
BATCH_PROCESSING = {
    'batch_size': 50,           # 每批处理数量
    'max_workers': 4,           # 最大并行数
    'timeout': 30,              # 单张图片超时时间（秒）
}

# 输出配置
OUTPUT_CONFIG = {
    'default_formats': ['json', 'csv', 'excel'],
    'date_format': '%Y-%m-%d',
    'float_precision': 2,       # 浮点数精度
    'excel_sheet_name': 'chart',
}

# 调试配置
DEBUG_CONFIG = {
    'save_preprocessed': True,   # 保存预处理图片
    'save_data_points': True,        # 保存图形元素检测图片
    'save_axis': False,          # 保存坐标轴识别图片
    'debug_output_dir': 'debug_output',
}


def get_config(section: str = None) -> dict:
    """
    获取配置
    
    Args:
        section: 配置节名称，None表示返回所有配置
    
    Returns:
        配置字典
    """
    all_config = {
        'ocr': OCR_CONFIG,
        'image_processing': IMAGE_PROCESSING,
        'DataPoint_detection': DataPoint_DETECTION,
        'chart_regions': CHART_REGIONS,
        'confidence': CONFIDENCE_THRESHOLDS,
        'price_validation': PRICE_VALIDATION,
        'batch_processing': BATCH_PROCESSING,
        'output': OUTPUT_CONFIG,
        'debug': DEBUG_CONFIG,
    }
    
    if section:
        return all_config.get(section, {})
    return all_config


if __name__ == '__main__':
    import json
    print("当前配置:")
    print(json.dumps(get_config(), indent=2, ensure_ascii=False))

