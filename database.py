import sqlite3
DATABASE_PATH = "data/password_manager.db"

class DatabaseManager:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self._init_db()

    def _init_db(self):
        # 连接到SQLite数据库（如果数据库不存在会自动创建）
        conn=sqlite3.connect(self.db_path)
        cursor=conn.cursor()
        # 创建数据表（如果不存在）
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS passwords (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            website TEXT NOT NULL,
                            username TEXT NOT NULL,
                            password TEXT NOT NULL
                        )
                    ''')
        # 提交事务并关闭连接
        conn.commit()
        conn.close()
    def add_password(self,website, username, password):
        # 连接到SQLite数据库
        conn=sqlite3.connect(self.db_path)
        cursor=conn.cursor()
        # 插入新数据
        cursor.execute('''
                        INSERT INTO passwords (website, username, password)
                        VALUES (?, ?, ?)
                    ''', (website, username, password))
        conn.commit()
        conn.close()

    def search_password(self, website):
        # 连接到SQLite数据库
        conn=sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 设置行工厂,这行很关健
        cursor=conn.cursor()
        # search数据
        cursor.execute('''SELECT * FROM passwords WHERE website = ?''', (website,))
        rows=cursor.fetchall()
        conn.close()
        return rows

    def get_all_passwords(self):
        # 连接到SQLite数据库
        conn=sqlite3.connect(self.db_path)
        conn.row_factory=sqlite3.Row  # 设置行工厂,这行很关健
        cursor=conn.cursor()
        cursor.execute('''SELECT * FROM passwords''')
        rows=cursor.fetchall()
        conn.close()
        return rows

    def update_password(self,user_id,website,username,password):
        # 连接到SQLite数据库
        conn=sqlite3.connect(self.db_path)
        cursor=conn.cursor()
        cursor.execute('''
            UPDATE passwords
            SET website = ?, username = ?, password = ?
            WHERE id = ?
            ''', (website, username, password, user_id))
        # 提交事务并关闭连接
        conn.commit()
        conn.close()

    def delete_password(self,website, username, password):
        # 连接到SQLite数据库
        conn=sqlite3.connect(self.db_path)
        cursor=conn.cursor()
        # 删除数据
        cursor.execute('''
                       DELETE FROM passwords
                       WHERE website = ? AND username = ? AND password = ?
                   ''', (website, username, password))
        # 提交事务并关闭连接
        conn.commit()
        conn.close()

    def get_user_id_by_website_and_username(self, website, username):
        # 连接到SQLite数据库
        conn=sqlite3.connect(self.db_path)
        cursor=conn.cursor()
        cursor.execute('''
            SELECT id FROM passwords WHERE website = ? AND username = ?
            ''', (website, username))
        row=cursor.fetchone()

        conn.close()

        if row:
            return row[0]
        else:
            return None