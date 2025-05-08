# -*- coding: utf-8 -*-
# @Time    : 2025/4/16 10:12
# @Author  : cz
# @File    : __init__.py.py
# @Software: PyCharm
import logging
COLORS = {
    'DEBUG': '\033[96m',  # 青色
    'INFO': '\033[92m',   # 绿色
    'WARNING': '\033[93m',# 黄色
    'ERROR': '\033[91m',  # 红色
    'CRITICAL': '\033[1;91m',  # 粗体红色
    'RESET': '\033[0m'    # 重置颜色
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        levelname = record.levelname
        message = super().format(record)
        color = COLORS.get(levelname, COLORS['RESET'])
        return f"{color}{message}{COLORS['RESET']}"


# 创建一个 Logger 对象
logger = logging.getLogger('contract_parse')
logger.setLevel(logging.DEBUG)  # 设置日志级别

# 创建一个 Handler，用于写入日志文件
file_handler = logging.FileHandler(r'app.log')
file_handler.setLevel(logging.DEBUG)

# 创建一个 Handler，用于输出到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 定义日志格式
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = ColoredFormatter("[%(asctime)s] [%(levelname)s] %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 将 Handler 添加到 Logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 记录日志
logger.info("日志系统初始化成功")
