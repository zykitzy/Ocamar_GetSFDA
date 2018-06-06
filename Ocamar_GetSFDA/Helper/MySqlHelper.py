# -*- coding: utf-8 -*-
import pymysql

class Dbsfda:
    host = '127.0.0.1'
    port = 3306
    user = 'root'
    password = 'Password@1'
    db = 'sfda'
    charset = 'utf8mb4'

    def add_entity(self, item):
        sql = "INSERT INTO `sfda`.`search_sfda`(" \
              "`yao_pin_name`," \
              "`pi_zhun_num`," \
              "`sheng_chan_company`," \
              "`zhi_ji`," \
              "`gui_ge`) VALUES(" \
              "'{0}'," \
              "'{1}'," \
              "'{2}'," \
              "'{3}'," \
              "'{4}');"
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                               passwd=self.password, db=self.db, charset=self.charset,
                               cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        sql = sql.format(item.yao_pin_name, item.pi_zhun_num,
                              item.sheng_chan_company, item.zhi_ji, item.gui_ge)
        print(sql)
        result = self.cursor.execute(sql)

        if result is not None and result > 0:
            conn.commit()
        cursor.close()
        conn.close()

    def add_list(self, items):
        sql = "INSERT INTO `sfda`.`search_sfda`(" \
              "`yao_pin_name`," \
              "`pi_zhun_num`," \
              "`sheng_chan_company`," \
              "`zhi_ji`," \
              "`gui_ge`) VALUES(" \
              "%s," \
              "%s," \
              "%s," \
              "%s," \
              "%s);"
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                               passwd=self.password, db=self.db, charset=self.charset,
                               cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        data = []
        for item in items:
            data.append((item.yao_pin_name,item.pi_zhun_num,
                         item.sheng_chan_company,item.zhi_ji,item.gui_ge))

        result = cursor.executemany(sql, data)
        if result is not None and result > 0:
            conn.commit()
        cursor.close()
        conn.close()
