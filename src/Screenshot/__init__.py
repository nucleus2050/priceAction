"""
屏幕截图工具包

提供简单易用的屏幕截图功能，支持全屏和区域截图。

Examples:
    >>> from Screenshot import Screenshot
    >>> screenshot = Screenshot()
    >>> 
    >>> # 全屏截图
    >>> img = screenshot.capture_fullscreen("fullscreen.png")
    >>> 
    >>> # 区域截图
    >>> img = screenshot.capture_region(100, 100, 800, 600, "region.png")
    >>> 
    >>> # 快速截图
    >>> img = Screenshot.quick_fullscreen("quick.png")
"""

from .Screenshot import Screenshot

__version__ = "1.0.0"
__author__ = "Your Name"
__all__ = ["Screenshot"]

