"""
图形识别核心模块
支持高精度批量识别图形截图
"""

import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional
import json
from pathlib import Path
from dataclasses import dataclass, asdict
import pandas as pd
from datetime import datetime, timedelta

# PaddleOCR是可选依赖，如果不可用将使用基础识别模式
try:
    from paddleocr import PaddleOCR
    PADDLEOCR_AVAILABLE = True
except ImportError:
    PADDLEOCR_AVAILABLE = False
    print("⚠️  PaddleOCR未安装，将使用基础识别模式")


@dataclass
class DataPoint:
    """图形数据点结构"""
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: Optional[float] = None
    
    def to_dict(self):
        return asdict(self)


@dataclass
class RecognitionResult:
    """识别结果"""
    image_name: str
    data_points: List[DataPoint]
    confidence: float
    symbol: Optional[str] = None
    error: Optional[str] = None
    
    def to_dict(self):
        return {
            'image_name': self.image_name,
            'symbol': self.symbol,
            'data_points': [c.to_dict() for c in self.data_points],
            'confidence': self.confidence,
            'error': self.error
        }


class ChartRecognizer:
    """图形识别器"""
    
    def __init__(self, use_gpu=False, debug=False, use_ocr=True):
        """
        初始化识别器
        
        Args:
            use_gpu: 是否使用GPU加速（注意：PaddleOCR 3.x 版本已移除此参数）
            debug: 是否开启调试模式（保存中间处理图片）
            use_ocr: 是否使用OCR识别坐标轴（如果False，将使用估算方法）
        """
        self.debug = debug
        self.use_ocr = use_ocr and PADDLEOCR_AVAILABLE
        self.ocr = None
        
        # 尝试初始化OCR（如果启用且可用）
        if self.use_ocr:
            try:
                self.ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
                if debug:
                    print("✓ OCR初始化成功")
            except Exception as e:
                print(f"⚠️  警告: OCR初始化失败: {e}")
                print("   将使用基础识别模式（不使用OCR）")
                self.ocr = None
                self.use_ocr = False
        
    def recognize(self, image_path: str) -> RecognitionResult:
        """
        识别单张图形元素图
        
        Args:
            image_path: 图片路径
            
        Returns:
            RecognitionResult: 识别结果
        """
        try:
            # 读取图片
            img = cv2.imread(image_path)
            if img is None:
                return RecognitionResult(
                    image_name=Path(image_path).name,
                    data_points=[],
                    confidence=0.0,
                    error="无法读取图片"
                )
            
            # 1. 图像预处理
            processed_img = self._preprocess_image(img)
            
            # 2. 识别坐标轴刻度
            axis_info = self._recognize_axis(img)
            
            # 3. 检测图形元素实体和影线
            data_points_raw = self._detect_data_points(processed_img, img)
            
            # 4. 坐标映射：像素 -> 实际价格
            data_points = self._map_coordinates(data_points_raw, axis_info, img.shape)
            
            # 5. 计算置信度
            confidence = self._calculate_confidence(data_points, axis_info)
            
            return RecognitionResult(
                image_name=Path(image_path).name,
                data_points=data_points,
                confidence=confidence,
                symbol=axis_info.get('symbol')
            )
            
        except Exception as e:
            return RecognitionResult(
                image_name=Path(image_path).name,
                data_points=[],
                confidence=0.0,
                error=str(e)
            )
    
    def _preprocess_image(self, img: np.ndarray) -> np.ndarray:
        """图像预处理"""
        # 转换为灰度图
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img.copy()
        
        # 去噪
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        # 自适应二值化
        binary = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        
        if self.debug:
            cv2.imwrite('debug_preprocessed.png', binary)
        
        return binary
    
    def _recognize_axis(self, img: np.ndarray) -> Dict:
        """
        识别坐标轴信息（价格刻度、日期等）
        
        Returns:
            {
                'price_min': float,
                'price_max': float,
                'price_coords': [(y_pixel, price_value), ...],
                'date_coords': [(x_pixel, date_str), ...],
                'symbol': str
            }
        """
        axis_info = {
            'price_min': None,
            'price_max': None,
            'price_coords': [],
            'date_coords': [],
            'symbol': None
        }
        
        # 使用OCR识别文字（如果可用）
        if self.ocr is None:
            # OCR不可用，返回基础信息
            return axis_info
            
        try:
            result = self.ocr.ocr(img, cls=True)
            
            if not result or not result[0]:
                return axis_info
        except Exception as e:
            if self.debug:
                print(f"OCR识别失败: {e}")
            return axis_info
        
        height, width = img.shape[:2]
        
        # 提取价格和日期信息
        for line in result[0]:
            bbox, (text, confidence) = line
            
            # 获取文字位置
            x_center = int((bbox[0][0] + bbox[2][0]) / 2)
            y_center = int((bbox[0][1] + bbox[2][1]) / 2)
            
            # 识别价格（通常在右侧或左侧）
            if (x_center < width * 0.15 or x_center > width * 0.85):
                price = self._parse_price(text)
                if price:
                    axis_info['price_coords'].append((y_center, price))
            
            # 识别日期（通常在底部）
            if y_center > height * 0.85:
                date = self._parse_date(text)
                if date:
                    axis_info['date_coords'].append((x_center, date))
            
            # 识别股票代码（通常在顶部）
            if y_center < height * 0.1:
                symbol = self._parse_symbol(text)
                if symbol:
                    axis_info['symbol'] = symbol
        
        # 计算价格范围
        if axis_info['price_coords']:
            prices = [p[1] for p in axis_info['price_coords']]
            axis_info['price_min'] = min(prices)
            axis_info['price_max'] = max(prices)
        
        if self.debug:
            print(f"识别到的坐标轴信息: {axis_info}")
        
        return axis_info
    
    def _detect_data_points(self, binary_img: np.ndarray, color_img: np.ndarray) -> List[Dict]:
        """
        检测图形元素实体和影线
        
        Returns:
            List of {
                'x_center': int,
                'body_top': int,
                'body_bottom': int,
                'shadow_high': int,
                'shadow_low': int,
                'is_red': bool  # 红色为涨，绿色为跌
            }
        """
        data_points = []
        
        height, width = color_img.shape[:2]
        
        # 定义图形元素图主体区域（排除坐标轴）
        chart_left = int(width * 0.1)
        chart_right = int(width * 0.9)
        chart_top = int(height * 0.1)
        chart_bottom = int(height * 0.8)
        
        # 提取红色和绿色通道
        hsv = cv2.cvtColor(color_img, cv2.COLOR_BGR2HSV)
        
        # 红色图形元素检测（两个色调范围）
        red_mask1 = cv2.inRange(hsv, (0, 50, 50), (10, 255, 255))
        red_mask2 = cv2.inRange(hsv, (170, 50, 50), (180, 255, 255))
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)
        
        # 绿色图形元素检测
        green_mask = cv2.inRange(hsv, (40, 50, 50), (80, 255, 255))
        
        # 检测红色图形元素
        data_points.extend(self._extract_data_points_from_mask(
            red_mask, color_img, chart_left, chart_right, chart_top, chart_bottom, is_red=True
        ))
        
        # 检测绿色图形元素
        data_points.extend(self._extract_data_points_from_mask(
            green_mask, color_img, chart_left, chart_right, chart_top, chart_bottom, is_red=False
        ))
        
        # 按x坐标排序
        data_points.sort(key=lambda c: c['x_center'])
        
        if self.debug:
            debug_img = color_img.copy()
            for c in data_points:
                cv2.rectangle(debug_img, 
                            (c['x_center']-5, c['body_top']), 
                            (c['x_center']+5, c['body_bottom']),
                            (0, 255, 0), 1)
                cv2.line(debug_img,
                        (c['x_center'], c['shadow_high']),
                        (c['x_center'], c['shadow_low']),
                        (255, 0, 0), 1)
            cv2.imwrite('debug_data_points.png', debug_img)
        
        return data_points
    
    def _extract_data_points_from_mask(self, mask: np.ndarray, color_img: np.ndarray,
                                   left: int, right: int, top: int, bottom: int,
                                   is_red: bool) -> List[Dict]:
        """从颜色掩码中提取图形元素"""
        data_points = []
        
        # 在图表区域内查找轮廓
        roi_mask = mask[top:bottom, left:right]
        contours, _ = cv2.findContours(roi_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        gray = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
        
        for contour in contours:
            # 获取边界框
            x, y, w, h = cv2.boundingRect(contour)
            
            # 过滤太小的轮廓
            if w < 3 or h < 5:
                continue
            
            # 转换回原图坐标
            x_abs = x + left
            y_abs = y + top
            
            x_center = x_abs + w // 2
            body_top = y_abs
            body_bottom = y_abs + h
            
            # 检测影线（在实体上下的细线）
            shadow_high = self._find_shadow_top(gray, x_center, body_top, top)
            shadow_low = self._find_shadow_bottom(gray, x_center, body_bottom, bottom)
            
            data_points.append({
                'x_center': x_center,
                'body_top': body_top,
                'body_bottom': body_bottom,
                'shadow_high': shadow_high,
                'shadow_low': shadow_low,
                'is_red': is_red
            })
        
        return data_points
    
    def _find_shadow_top(self, gray: np.ndarray, x: int, body_top: int, limit_top: int) -> int:
        """查找上影线最高点"""
        threshold = 50  # 暗色阈值
        for y in range(body_top - 1, limit_top, -1):
            if y < 0 or y >= gray.shape[0] or x < 0 or x >= gray.shape[1]:
                break
            if gray[y, x] > threshold:
                return y + 1
        return body_top
    
    def _find_shadow_bottom(self, gray: np.ndarray, x: int, body_bottom: int, limit_bottom: int) -> int:
        """查找下影线最低点"""
        threshold = 50
        for y in range(body_bottom + 1, limit_bottom):
            if y >= gray.shape[0] or x >= gray.shape[1]:
                break
            if gray[y, x] > threshold:
                return y - 1
        return body_bottom
    
    def _map_coordinates(self, data_points_raw: List[Dict], axis_info: Dict, 
                        img_shape: Tuple) -> List[DataPoint]:
        """将像素坐标映射为实际价格"""
        if not data_points_raw:
            return []
        
        height, width = img_shape[:2]
        
        # 如果没有识别到价格坐标，使用估算
        if not axis_info['price_coords'] or len(axis_info['price_coords']) < 2:
            price_min = 100.0
            price_max = 200.0
            price_top = int(height * 0.1)
            price_bottom = int(height * 0.8)
        else:
            # 使用识别到的价格坐标
            price_coords = sorted(axis_info['price_coords'], key=lambda x: x[0])
            price_top = price_coords[0][0]
            price_bottom = price_coords[-1][0]
            price_min = axis_info['price_min']
            price_max = axis_info['price_max']
        
        # 计算价格映射函数
        def pixel_to_price(y_pixel):
            ratio = (y_pixel - price_top) / (price_bottom - price_top)
            price = price_max - ratio * (price_max - price_min)
            return round(price, 2)
        
        # 生成日期（如果没有识别到，使用序号）
        base_date = datetime.now()
        
        data_points = []
        for i, c_raw in enumerate(data_points_raw):
            # 计算OHLC
            if c_raw['is_red']:  # 红色图形元素：收盘价 > 开盘价
                open_price = pixel_to_price(c_raw['body_bottom'])
                close_price = pixel_to_price(c_raw['body_top'])
            else:  # 绿色图形元素：收盘价 < 开盘价
                open_price = pixel_to_price(c_raw['body_top'])
                close_price = pixel_to_price(c_raw['body_bottom'])
            
            high_price = pixel_to_price(c_raw['shadow_high'])
            low_price = pixel_to_price(c_raw['shadow_low'])
            
            # 确保数据合理性
            high_price = max(high_price, open_price, close_price)
            low_price = min(low_price, open_price, close_price)
            
            # 生成日期
            date_str = (base_date - timedelta(days=len(data_points_raw) - i)).strftime('%Y-%m-%d')
            
            data_points.append(DataPoint(
                date=date_str,
                open=open_price,
                high=high_price,
                low=low_price,
                close=close_price
            ))
        
        return data_points
    
    def _calculate_confidence(self, data_points: List[DataPoint], axis_info: Dict) -> float:
        """计算识别置信度"""
        confidence = 1.0
        
        # 如果没有识别到图形元素，置信度为0
        if not data_points:
            return 0.0
        
        # 如果没有识别到价格坐标，降低置信度
        if not axis_info['price_coords']:
            confidence *= 0.5
        
        # 检查数据合理性
        for DataPoint in data_points:
            if DataPoint.high < DataPoint.low:
                confidence *= 0.8
            if DataPoint.open < 0 or DataPoint.close < 0:
                confidence *= 0.8
        
        return round(confidence, 2)
    
    def _parse_price(self, text: str) -> Optional[float]:
        """从文本中解析价格"""
        import re
        # 匹配数字（整数或小数）
        pattern = r'(\d+\.?\d*)'
        match = re.search(pattern, text)
        if match:
            try:
                price = float(match.group(1))
                # 过滤不合理的价格
                if 0.01 < price < 1000000:
                    return price
            except ValueError:
                pass
        return None
    
    def _parse_date(self, text: str) -> Optional[str]:
        """从文本中解析日期"""
        import re
        # 匹配日期格式
        patterns = [
            r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})',
            r'(\d{1,2}[-/]\d{1,2})',
            r'(\d{4}年\d{1,2}月\d{1,2}日)'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None
    
    def _parse_symbol(self, text: str) -> Optional[str]:
        """从文本中解析股票代码"""
        import re
        # 匹配股票代码格式
        patterns = [
            r'([A-Z]{2,4})',  # 美股
            r'(\d{6})',       # A股
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None
    
    def batch_process(self, input_dir: str, output_dir: str = 'output',
                     output_formats: List[str] = ['json', 'csv', 'excel']) -> List[RecognitionResult]:
        """
        批量处理图形元素图
        
        Args:
            input_dir: 输入图片文件夹
            output_dir: 输出文件夹
            output_formats: 输出格式列表 ['json', 'csv', 'excel']
            
        Returns:
            List[RecognitionResult]: 所有识别结果
        """
        from tqdm import tqdm
        
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 支持的图片格式
        image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
        image_files = []
        for ext in image_extensions:
            image_files.extend(input_path.glob(f'*{ext}'))
        
        print(f"找到 {len(image_files)} 张图片")
        
        results = []
        for img_file in tqdm(image_files, desc="处理中"):
            result = self.recognize(str(img_file))
            results.append(result)
        
        # 输出结果
        self._export_results(results, output_path, output_formats)
        
        # 统计信息
        success_count = sum(1 for r in results if r.confidence > 0.5)
        print(f"\n处理完成！成功: {success_count}/{len(results)}")
        print(f"结果已保存到: {output_path}")
        
        return results
    
    def _export_results(self, results: List[RecognitionResult], 
                       output_path: Path, formats: List[str]):
        """导出结果到多种格式"""
        
        # JSON格式
        if 'json' in formats:
            json_file = output_path / 'results.json'
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump([r.to_dict() for r in results], f, 
                         ensure_ascii=False, indent=2)
        
        # CSV格式（展平数据）
        if 'csv' in formats or 'excel' in formats:
            all_data_points = []
            for result in results:
                for DataPoint in result.data_points:
                    all_data_points.append({
                        'image': result.image_name,
                        'symbol': result.symbol,
                        'date': DataPoint.date,
                        'open': DataPoint.open,
                        'high': DataPoint.high,
                        'low': DataPoint.low,
                        'close': DataPoint.close,
                        'volume': DataPoint.volume,
                        'confidence': result.confidence
                    })
            
            df = pd.DataFrame(all_data_points)
            
            if 'csv' in formats:
                csv_file = output_path / 'results.csv'
                df.to_csv(csv_file, index=False, encoding='utf-8-sig')
            
            if 'excel' in formats:
                excel_file = output_path / 'results.xlsx'
                df.to_excel(excel_file, index=False, engine='openpyxl')


if __name__ == '__main__':
    # 示例用法
    recognizer = ChartRecognizer(debug=True)
    
    # 单张图片识别
    # result = recognizer.recognize('test.png')
    # print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    
    # 批量处理
    # results = recognizer.batch_process('screenshots/', 'output/')
    
    print("图形识别系统已就绪")
    print("使用方法:")
    print("  recognizer = ChartRecognizer()")
    print("  result = recognizer.recognize('your_chart.png')")
    print("  results = recognizer.batch_process('screenshots/', 'output/')")

