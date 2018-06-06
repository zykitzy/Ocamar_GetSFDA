# -*- coding: utf-8 -*-
import logging


# log 辅助类
class Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler("log.txt", "a", encoding="utf-8")  # 设置属性和编码
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # 辅助方法
    def log_info(self, msg):
        self.logger.info(msg)
