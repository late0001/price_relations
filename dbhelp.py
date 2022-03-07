# * coding=utf-8 *
__author__ = 'maybe'

#导入模块
import sqlite3

class DbHelp:
    def __init__(self):
        self.db_conn("./ds82.mdb")
        
    
        
    #定义conn
    def db_conn(self, db_name, password = ""):
        """
        功能：创建数据库连接
        :param db_name: 数据库名称
        :param db_name: 数据库密码，默认为空
        :return: 返回数据库连接
        """
        #str = u'Driver={Microsoft Access Driver (*.mdb)};PWD' + password + ";DBQ=" + db_name
        #conn = pypyodbc.win_connect_mdb(str)
        str = u'./ds89.db'
        conn = sqlite3.connect(str)
        self.conn = conn
        self.cur = conn.cursor()
        return conn
    
    def __del__(self):
        self.cur.close()    #关闭游标
        self.conn.close()   #关闭数据库连接
        
    #执行sql语句
    def exec_sql(self, sql):
        """
        功能：执行sql语句
        :param conn: 数据库连接
        :param cur: 游标
        :param sql: sql语句
        :return: sql语句是否执行成功
        """
        try:
            self.cur.execute(sql)
            self.conn.commit()
            return True
        except :
            print('exec_sql error')
            return False
    
    #增加记录
    def db_insert(self, sql):
        """
        功能：向数据库插入数据
        :param conn: 数据库连接
        :param cur: 游标
        :param sql: sql语句
        :return: sql语句是否执行成功
        """
        try:
            self.cur.execute(sql)
            self.conn.commit()
            return True
        except:
            print('db_insert error')
            return False    
            
    #删除记录
    def db_delete(self, sql):
        """
        功能：向数据库删除数据
        :param conn: 数据库连接
        :param cur: 游标
        :param sql: sql语句
        :return: sql语句是否执行成功
        """
        try:
            self.cur.execute(sql)
            self.conn.commit()
            return True
        except:
            print('db_delete error')
            return False
    
    #修改记录
    def db_update(self, sql):
        """
        功能：向数据库修改数据
        :param conn: 数据库连接
        :param cur: 游标
        :param sql: sql语句
        :return: sql语句是否执行成功
        """
        try:
            self.cur.execute(sql)
            self.conn.commit()
            return True
        except:
            print('db_update error')
            return False
    
    #查询记录
    def db_select(self, sql):
        """
        功能：向数据库查询数据
        :param cur: 游标
        :param sql: sql语句
        :return: 查询结果集
        """
        try:
            self.cur.execute(sql)
            return self.cur.fetchall()
        except:
            print('db_select error')
            return []

if __name__ == '__main__':
    db = DbHelp()
    if db.db_insert('''INSERT INTO table1 ( pid, description, torrent, movlink )
    VALUES (1, 'nimei02', 'bb.torrent', 'a.php?id=a343543542')'''):
        print ("OK")
    else:
        print ("Insert failed")
   