# -*- coding: utf-8 -*-
import os


class Config:
    file_path = '{0}\keyword.txt'.format(os.sys.path[0])
    print(file_path)

    def get_config(self):  # 获取配置项
        file = open(self.file_path, 'r', encoding='utf-8')
        configs = file.readlines()
        config_list = []

        for config in configs:  # 去除 \n
            if not config.strip():
                continue
            if config.startswith('--') \
                    or config.startswith('#') \
                    or config.startswith('//'):  # 不记录注释行
                continue
            print(config)
            config_list.append(config.rstrip('\n'))

        return config_list
