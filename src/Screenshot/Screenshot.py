"""
屏幕截图工具包
支持全屏截图、指定区域截图和多屏幕截图
"""

import os
import sys
from typing import Optional, Tuple, List, Dict
from PIL import ImageGrab, Image
from datetime import datetime

# 尝试导入多屏幕支持库
try:
    from screeninfo import get_monitors
    SCREENINFO_AVAILABLE = True
except ImportError:
    SCREENINFO_AVAILABLE = False


class Screenshot:
    """屏幕截图工具类"""
    
    def __init__(self, save_dir: str = "screenshots"):
        """
        初始化截图工具
        
        Args:
            save_dir: 默认保存目录
        """
        self.save_dir = save_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    
    def capture_fullscreen(self, save_path: Optional[str] = None, 
                          all_screens: bool = False) -> Image.Image:
        """
        捕获全屏截图
        
        Args:
            save_path: 保存路径，如果为None则自动生成文件名
            all_screens: 是否捕获所有屏幕（多显示器时）
        
        Returns:
            PIL.Image.Image: 截图图像对象
        
        Examples:
            >>> screenshot = Screenshot()
            >>> img = screenshot.capture_fullscreen()
            >>> img = screenshot.capture_fullscreen("my_screenshot.png")
            >>> img = screenshot.capture_fullscreen(all_screens=True)  # 捕获所有屏幕
        """
        # 捕获屏幕（支持多屏幕）
        img = ImageGrab.grab(all_screens=all_screens)
        
        # 保存图片
        if save_path:
            img.save(save_path)
            print(f"✓ 全屏截图已保存: {save_path}")
        else:
            # 自动生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fullscreen_{timestamp}.png"
            filepath = os.path.join(self.save_dir, filename)
            img.save(filepath)
            print(f"✓ 全屏截图已保存: {filepath}")
        
        return img
    
    def capture_region(self, 
                      x: int, 
                      y: int, 
                      width: int, 
                      height: int,
                      save_path: Optional[str] = None) -> Image.Image:
        """
        捕获指定区域的截图
        
        Args:
            x: 区域左上角X坐标
            y: 区域左上角Y坐标
            width: 区域宽度
            height: 区域高度
            save_path: 保存路径，如果为None则自动生成文件名
        
        Returns:
            PIL.Image.Image: 截图图像对象
        
        Examples:
            >>> screenshot = Screenshot()
            >>> # 截取从(100, 100)开始，宽800高600的区域
            >>> img = screenshot.capture_region(100, 100, 800, 600)
        """
        # 计算边界框 (left, top, right, bottom)
        bbox = (x, y, x + width, y + height)
        
        # 捕获指定区域
        img = ImageGrab.grab(bbox=bbox)
        
        # 保存图片
        if save_path:
            img.save(save_path)
            print(f"✓ 区域截图已保存: {save_path}")
        else:
            # 自动生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"region_{x}_{y}_{width}x{height}_{timestamp}.png"
            filepath = os.path.join(self.save_dir, filename)
            img.save(filepath)
            print(f"✓ 区域截图已保存: {filepath}")
        
        return img
    
    def capture_bbox(self,
                    left: int,
                    top: int,
                    right: int,
                    bottom: int,
                    save_path: Optional[str] = None) -> Image.Image:
        """
        使用边界框坐标捕获截图
        
        Args:
            left: 左边界X坐标
            top: 上边界Y坐标
            right: 右边界X坐标
            bottom: 下边界Y坐标
            save_path: 保存路径，如果为None则自动生成文件名
        
        Returns:
            PIL.Image.Image: 截图图像对象
        
        Examples:
            >>> screenshot = Screenshot()
            >>> # 截取从(100, 100)到(900, 700)的区域
            >>> img = screenshot.capture_bbox(100, 100, 900, 700)
        """
        bbox = (left, top, right, bottom)
        
        # 捕获指定区域
        img = ImageGrab.grab(bbox=bbox)
        
        # 保存图片
        if save_path:
            img.save(save_path)
            print(f"✓ 边界框截图已保存: {save_path}")
        else:
            # 自动生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            width = right - left
            height = bottom - top
            filename = f"bbox_{left}_{top}_{width}x{height}_{timestamp}.png"
            filepath = os.path.join(self.save_dir, filename)
            img.save(filepath)
            print(f"✓ 边界框截图已保存: {filepath}")
        
        return img
    
    def get_screen_size(self, all_screens: bool = False) -> Tuple[int, int]:
        """
        获取屏幕尺寸
        
        Args:
            all_screens: 是否获取所有屏幕的总尺寸
        
        Returns:
            Tuple[int, int]: (宽度, 高度)
        
        Examples:
            >>> screenshot = Screenshot()
            >>> width, height = screenshot.get_screen_size()
            >>> print(f"屏幕尺寸: {width}x{height}")
        """
        img = ImageGrab.grab(all_screens=all_screens)
        return img.size
    
    def get_monitors_info(self) -> List[Dict]:
        """
        获取所有显示器信息（需要安装 screeninfo 库）
        
        Returns:
            List[Dict]: 显示器信息列表，每个包含 x, y, width, height, is_primary
        
        Examples:
            >>> screenshot = Screenshot()
            >>> monitors = screenshot.get_monitors_info()
            >>> for i, monitor in enumerate(monitors):
            ...     print(f"显示器{i}: {monitor['width']}x{monitor['height']}")
        """
        if not SCREENINFO_AVAILABLE:
            print("⚠️  需要安装 screeninfo 库: pip install screeninfo")
            # 返回主屏幕信息
            width, height = self.get_screen_size()
            return [{
                'index': 0,
                'x': 0,
                'y': 0,
                'width': width,
                'height': height,
                'is_primary': True
            }]
        
        monitors = []
        for i, monitor in enumerate(get_monitors()):
            monitors.append({
                'index': i,
                'name': monitor.name if hasattr(monitor, 'name') else f"Monitor {i}",
                'x': monitor.x,
                'y': monitor.y,
                'width': monitor.width,
                'height': monitor.height,
                'is_primary': monitor.is_primary if hasattr(monitor, 'is_primary') else (i == 0)
            })
        return monitors
    
    def capture_monitor(self, monitor_index: int = 0, 
                       save_path: Optional[str] = None) -> Image.Image:
        """
        捕获指定显示器的截图
        
        Args:
            monitor_index: 显示器索引（0为主显示器）
            save_path: 保存路径
        
        Returns:
            PIL.Image.Image: 截图图像对象
        
        Examples:
            >>> screenshot = Screenshot()
            >>> img = screenshot.capture_monitor(0)  # 主显示器
            >>> img = screenshot.capture_monitor(1)  # 第二个显示器
        """
        monitors = self.get_monitors_info()
        
        if monitor_index >= len(monitors):
            print(f"⚠️  显示器索引 {monitor_index} 超出范围，使用主显示器")
            monitor_index = 0
        
        monitor = monitors[monitor_index]
        
        # 使用边界框捕获指定显示器
        bbox = (
            monitor['x'],
            monitor['y'],
            monitor['x'] + monitor['width'],
            monitor['y'] + monitor['height']
        )
        
        img = ImageGrab.grab(bbox=bbox)
        
        # 保存图片
        if save_path:
            img.save(save_path)
            print(f"✓ 显示器{monitor_index}截图已保存: {save_path}")
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"monitor_{monitor_index}_{monitor['width']}x{monitor['height']}_{timestamp}.png"
            filepath = os.path.join(self.save_dir, filename)
            img.save(filepath)
            print(f"✓ 显示器{monitor_index}截图已保存: {filepath}")
        
        return img
    
    def capture_all_monitors(self, save_dir: Optional[str] = None) -> List[Image.Image]:
        """
        分别捕获所有显示器的截图
        
        Args:
            save_dir: 保存目录，如果为None则使用默认目录
        
        Returns:
            List[Image.Image]: 所有显示器的截图列表
        
        Examples:
            >>> screenshot = Screenshot()
            >>> images = screenshot.capture_all_monitors()
            >>> print(f"捕获了 {len(images)} 个显示器")
        """
        monitors = self.get_monitors_info()
        images = []
        
        save_directory = save_dir if save_dir else self.save_dir
        
        print(f"\n捕获 {len(monitors)} 个显示器的截图...")
        for i, monitor in enumerate(monitors):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"monitor_{i}_{monitor['width']}x{monitor['height']}_{timestamp}.png"
            filepath = os.path.join(save_directory, filename)
            
            img = self.capture_monitor(i, filepath)
            images.append(img)
        
        return images
    
    @staticmethod
    def quick_fullscreen(save_path: str = None) -> Image.Image:
        """
        快速全屏截图（静态方法）
        
        Args:
            save_path: 保存路径
        
        Returns:
            PIL.Image.Image: 截图图像对象
        
        Examples:
            >>> img = Screenshot.quick_fullscreen("screenshot.png")
        """
        img = ImageGrab.grab()
        if save_path:
            img.save(save_path)
            print(f"✓ 截图已保存: {save_path}")
        return img
    
    @staticmethod
    def quick_region(x: int, y: int, width: int, height: int, 
                    save_path: str = None) -> Image.Image:
        """
        快速区域截图（静态方法）
        
        Args:
            x: 区域左上角X坐标
            y: 区域左上角Y坐标
            width: 区域宽度
            height: 区域高度
            save_path: 保存路径
        
        Returns:
            PIL.Image.Image: 截图图像对象
        
        Examples:
            >>> img = Screenshot.quick_region(100, 100, 800, 600, "region.png")
        """
        bbox = (x, y, x + width, y + height)
        img = ImageGrab.grab(bbox=bbox)
        if save_path:
            img.save(save_path)
            print(f"✓ 截图已保存: {save_path}")
        return img


def main():
    """演示使用示例"""
    print("=" * 60)
    print("屏幕截图工具演示")
    print("=" * 60)
    
    # 创建截图工具实例
    screenshot = Screenshot(save_dir="screenshots")
    
    # 获取屏幕尺寸
    width, height = screenshot.get_screen_size()
    print(f"\n主屏幕尺寸: {width}x{height}")
    
    # 检查多显示器
    print("\n多显示器信息:")
    monitors = screenshot.get_monitors_info()
    print(f"  检测到 {len(monitors)} 个显示器")
    for monitor in monitors:
        primary = " (主显示器)" if monitor.get('is_primary') else ""
        print(f"  - 显示器{monitor['index']}: {monitor['width']}x{monitor['height']} "
              f"at ({monitor['x']}, {monitor['y']}){primary}")
    
    # 示例1: 主屏幕截图
    print("\n示例1: 主屏幕截图")
    img1 = screenshot.capture_fullscreen()
    print(f"  尺寸: {img1.size}")
    
    # 示例2: 所有屏幕截图（如果有多个显示器）
    if len(monitors) > 1:
        print("\n示例2: 捕获所有屏幕")
        img2 = screenshot.capture_fullscreen(all_screens=True)
        print(f"  总尺寸: {img2.size}")
        
        print("\n示例3: 分别捕获每个显示器")
        for i in range(len(monitors)):
            img = screenshot.capture_monitor(i)
            print(f"  显示器{i}: {img.size}")
    else:
        print("\n示例2: 捕获屏幕中心区域")
        center_x = (width - 800) // 2
        center_y = (height - 600) // 2
        img2 = screenshot.capture_region(center_x, center_y, 800, 600)
        print(f"  尺寸: {img2.size}")
    
    # 示例: 使用边界框
    print(f"\n示例{len(monitors)+2}: 使用边界框捕获左上角区域")
    img3 = screenshot.capture_bbox(0, 0, 400, 300)
    print(f"  尺寸: {img3.size}")
    
    # 示例: 快速截图
    print(f"\n示例{len(monitors)+3}: 快速全屏截图")
    img4 = Screenshot.quick_fullscreen("quick_fullscreen.png")
    print(f"  尺寸: {img4.size}")
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！请查看生成的截图文件")
    print("=" * 60)
    
    if not SCREENINFO_AVAILABLE:
        print("\n💡 提示: 安装 screeninfo 可获得更准确的多显示器信息")
        print("   pip install screeninfo")


if __name__ == "__main__":
    main()

