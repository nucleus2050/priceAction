# 📚 图形识别系统 - 文档索引

欢迎使用图形识别系统！本文档帮助您快速找到所需信息。

## 🚀 快速导航

### 新手入门

1. **[README.md](README.md)** - 从这里开始！
   - 项目简介和核心特性
   - 技术架构概览
   - 快速安装和使用

2. **[QUICKSTART.md](QUICKSTART.md)** - 5分钟上手
   - 最快的入门路径
   - 常用命令速查
   - 基础示例代码

3. **[INSTALL.md](INSTALL.md)** - 安装指南
   - 详细安装步骤
   - 环境配置
   - 常见问题解决

### 使用文档

4. **[USAGE.md](USAGE.md)** - 完整使用文档
   - API详细说明
   - 高级用法
   - 数据处理示例
   - 性能优化技巧

5. **[example.py](example.py)** - 代码示例
   - 单张图片识别
   - 批量处理
   - 自定义数据处理
   - 与pandas集成

6. **[demo.py](demo.py)** - 演示程序
   - 自动创建测试数据
   - 完整识别流程演示
   - 结果可视化

### 技术文档

7. **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - 项目架构
   - 目录结构说明
   - 模块功能介绍
   - 技术架构图
   - 开发指南

8. **[SUMMARY.md](SUMMARY.md)** - 项目总结
   - 技术方案详解
   - 核心算法流程
   - 性能指标
   - 优势对比

9. **[config.py](config.py)** - 配置说明
   - 所有可调参数
   - 配置项说明
   - 自定义配置

### 核心代码

10. **[chart_recognizer.py](chart_recognizer.py)** - 核心引擎
    - `chartRecognizer` 类
    - 识别算法实现
    - 数据结构定义

11. **[cli.py](cli.py)** - 命令行工具
    - CLI接口
    - 参数说明
    - 批处理功能

12. **[utils.py](utils.py)** - 工具函数
    - 数据验证
    - 可视化
    - 格式转换
    - 报告生成

13. **[test_system.py](test_system.py)** - 系统测试
    - 功能测试
    - 依赖检查
    - 创建测试数据

### 其他

14. **[requirements.txt](requirements.txt)** - 依赖清单
15. **[LICENSE](LICENSE)** - MIT许可证
16. **[.gitignore](.gitignore)** - Git忽略规则

---

## 📖 按场景查找

### 我想快速开始使用

→ [QUICKSTART.md](QUICKSTART.md) → [demo.py](demo.py)

### 我想了解如何安装

→ [INSTALL.md](INSTALL.md) → [requirements.txt](requirements.txt)

### 我想学习API用法

→ [USAGE.md](USAGE.md) → [example.py](example.py)

### 我想了解技术细节

→ [SUMMARY.md](SUMMARY.md) → [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

### 我想修改配置参数

→ [config.py](config.py) → [USAGE.md#高级配置](USAGE.md)

### 我想贡献代码

→ [PROJECT_STRUCTURE.md#开发指南](PROJECT_STRUCTURE.md) → [README.md#贡献指南](README.md)

### 我遇到了问题

→ [INSTALL.md#常见问题](INSTALL.md) → [USAGE.md#故障排除](USAGE.md)

---

## 🎯 按角色查找

### 普通用户

**目标**: 快速使用系统识别图形

**推荐路径**:
1. [README.md](README.md) - 了解项目
2. [INSTALL.md](INSTALL.md) - 安装系统
3. [QUICKSTART.md](QUICKSTART.md) - 开始使用
4. [demo.py](demo.py) - 运行演示

**常用命令**:
```bash
# 安装
pip install -r requirements.txt

# 测试
python test_system.py

# 使用
python cli.py -i your_image.png
```

---

### Python开发者

**目标**: 集成到自己的项目

**推荐路径**:
1. [README.md](README.md) - 项目概览
2. [USAGE.md](USAGE.md) - API文档
3. [example.py](example.py) - 代码示例
4. [chart_recognizer.py](chart_recognizer.py) - 源码

**示例代码**:
```python
from chart_recognizer import chartRecognizer

recognizer = chartRecognizer()
result = recognizer.recognize('chart.png')

# 处理结果
for DataPoint in result.data_points:
    print(DataPoint.to_dict())
```

---

### 数据分析师

**目标**: 批量提取数据并分析

**推荐路径**:
1. [QUICKSTART.md](QUICKSTART.md) - 快速上手
2. [USAGE.md#数据处理示例](USAGE.md) - 数据处理
3. [utils.py](utils.py) - 工具函数
4. [example.py](example.py) - 分析示例

**工作流程**:
```bash
# 批量识别
python cli.py -i screenshots/ -o output/

# 在Python中分析
import pandas as pd
df = pd.read_csv('output/results.csv')
df.describe()
```

---

### 系统管理员

**目标**: 部署和维护系统

**推荐路径**:
1. [INSTALL.md](INSTALL.md) - 安装部署
2. [config.py](config.py) - 配置管理
3. [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 架构理解
4. [test_system.py](test_system.py) - 系统测试

**运维命令**:
```bash
# 环境检查
python test_system.py

# 批量处理监控
python cli.py -i input/ -o output/ --debug

# 查看配置
python config.py
```

---

### 研究人员

**目标**: 理解算法并改进

**推荐路径**:
1. [SUMMARY.md](SUMMARY.md) - 技术总结
2. [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 架构设计
3. [chart_recognizer.py](chart_recognizer.py) - 核心算法
4. [config.py](config.py) - 参数调优

**研究方向**:
- 图像预处理优化
- 图形元素检测算法改进
- 坐标映射精度提升
- 多模态模型集成

---

## 📊 文档关系图

```
README.md (入口)
    ├── QUICKSTART.md (快速开始)
    │   ├── INSTALL.md (安装)
    │   └── demo.py (演示)
    │
    ├── USAGE.md (使用文档)
    │   ├── example.py (示例)
    │   ├── cli.py (命令行)
    │   └── config.py (配置)
    │
    ├── PROJECT_STRUCTURE.md (架构)
    │   ├── chart_recognizer.py (核心)
    │   ├── utils.py (工具)
    │   └── test_system.py (测试)
    │
    └── SUMMARY.md (总结)
        ├── 技术方案
        ├── 性能指标
        └── 未来规划
```

---

## 🔍 快速搜索

### 关键词索引

- **安装**: [INSTALL.md](INSTALL.md)
- **快速开始**: [QUICKSTART.md](QUICKSTART.md)
- **API文档**: [USAGE.md](USAGE.md)
- **示例代码**: [example.py](example.py)
- **命令行**: [cli.py](cli.py)
- **配置**: [config.py](config.py)
- **测试**: [test_system.py](test_system.py)
- **架构**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- **算法**: [SUMMARY.md](SUMMARY.md)
- **工具函数**: [utils.py](utils.py)

### 功能索引

- **单张识别**: [QUICKSTART.md](QUICKSTART.md), [example.py](example.py)
- **批量处理**: [cli.py](cli.py), [USAGE.md](USAGE.md)
- **数据导出**: [utils.py](utils.py), [USAGE.md](USAGE.md)
- **可视化**: [utils.py](utils.py)
- **数据验证**: [utils.py](utils.py)
- **性能优化**: [USAGE.md](USAGE.md), [config.py](config.py)

---

## 💡 学习路径建议

### 路径1: 快速使用 (30分钟)

```
README.md (5分钟)
    ↓
INSTALL.md (10分钟)
    ↓
QUICKSTART.md (10分钟)
    ↓
demo.py (5分钟)
```

### 路径2: 深入学习 (2小时)

```
README.md (10分钟)
    ↓
INSTALL.md (15分钟)
    ↓
USAGE.md (30分钟)
    ↓
example.py (20分钟)
    ↓
PROJECT_STRUCTURE.md (30分钟)
    ↓
chart_recognizer.py (15分钟)
```

### 路径3: 全面掌握 (1天)

```
所有文档阅读 (4小时)
    ↓
运行所有示例 (2小时)
    ↓
阅读核心代码 (4小时)
    ↓
自定义开发 (2小时)
```

---

## 📞 获取帮助

1. **查看文档**: 先查阅相关文档
2. **运行测试**: `python test_system.py`
3. **查看示例**: 参考 [example.py](example.py)
4. **提交Issue**: 在GitHub上提问
5. **联系作者**: 通过邮件沟通

---

## 🎉 开始使用

选择您的起点：

- 🚀 **我想立即开始**: → [QUICKSTART.md](QUICKSTART.md)
- 📖 **我想了解更多**: → [README.md](README.md)
- 💻 **我想看代码**: → [example.py](example.py)
- 🔧 **我想深入研究**: → [SUMMARY.md](SUMMARY.md)

祝您使用愉快！ 🎊

