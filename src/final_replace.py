#!/usr/bin/env python3
"""最终批量替换 - 确保所有K线相关词汇被替换"""
import os, sys

# 所有替换规则
RULES = [
    ('kline_recognizer', 'chart_recognizer'),
    ('KLineRecognizer', 'ChartRecognizer'),
    ('K线图识别系统', '图形识别系统'),
    ('K线图', '图形'),
    ('K线', '图形元素'),
    ('k线', '图形'),
    ('candles_raw', 'data_raw'),
    ('candles:', 'data_points:'),
    ('candles=', 'data_points='),
    ('candles)', 'data_points)'),
    ('candles,', 'data_points,'),
    ('result.candles', 'result.data_points'),
    ('Candle(', 'DataPoint('),
    ('Candle:', 'DataPoint:'),
    ('List[Candle]', 'List[DataPoint]'),
    ('candle.', 'data_point.'),
    ('for candle in', 'for data_point in'),
    ('candles', 'data_points'),
    ('Candle', 'DataPoint'),
    ('candle', 'data_point'),
    ('debug_candles.png', 'debug_data_points.png'),
    ('蜡烛图', '图形'),
    ('candlestick', 'chart'),
]

# 获取所有需要处理的文件
FILES = [f for f in os.listdir('.') if f.endswith(('.py', '.md', '.txt')) and 
         not f.startswith(('batch', 'replace', 'do_', 'final', 'FINAL', 'Replace'))]

count = 0
for fname in sorted(FILES):
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            text = f.read()
        new_text = text
        for old, new in RULES:
            new_text = new_text.replace(old, new)
        if text != new_text:
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(new_text)
            count += 1
            sys.stdout.write(f'✓ {fname}\n')
            sys.stdout.flush()
    except Exception as e:
        sys.stderr.write(f'✗ {fname}: {e}\n')

sys.stdout.write(f'\nDone! Modified {count} files\n')
sys.stdout.flush()
