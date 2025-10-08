import pymysql
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.connection = None
    
    def connect(self):
        """建立数据库连接"""
        try:
            self.connection = pymysql.connect(**DB_CONFIG)
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False
    
    def disconnect(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query, params=None):
        """执行查询并返回结果"""
        try:
            if not self.connection:
                if not self.connect():
                    return None
            
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                self.connection.commit()
                return result
        except Exception as e:
            print(f"Query execution error: {e}")
            return None
    
    def execute_update(self, query, params=None):
        """执行更新操作并返回影响行数"""
        try:
            if not self.connection:
                if not self.connect():
                    return 0
            
            with self.connection.cursor() as cursor:
                affected_rows = cursor.execute(query, params)
                self.connection.commit()
                return affected_rows
        except Exception as e:
            print(f"Update execution error: {e}")
            return 0

# 创建数据库实例
db = Database()
