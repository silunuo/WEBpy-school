#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
#  author:lwl
#  Collaborator:cr and lx and tyf
import pymysql
###请修改这里的个人数据库信息再使用！！！！！
def get_connection():
    return pymysql.connect(
        host="your_host",
        user="your_password",
        password="your_password",
        database="scanner_db",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
#这里应该写一个检测宿主的数据库信息或者填写的，但是我懒
def insert_url(url):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO urls (url) VALUES (%s)"
            cursor.execute(sql, (url,))
        connection.commit()
    finally:
        connection.close()

def get_all_urls():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM urls ORDER BY crawled_at DESC")
            return cursor.fetchall()
    finally:
        connection.close()

def delete_url(url_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # 先删除关联的日志
            sql_logs = "DELETE FROM xss_scan_logs WHERE url_id = %s"
            cursor.execute(sql_logs, (url_id,))
            # 再删除URL
            sql_url = "DELETE FROM urls WHERE id = %s"
            cursor.execute(sql_url, (url_id,))
        connection.commit()
    finally:
        connection.close()

def log_xss_scan(url_id, result):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # 记录到扫描日志表
            sql_log = "INSERT INTO xss_scan_logs (url_id, scan_result) VALUES (%s, %s)"
            cursor.execute(sql_log, (url_id, result))

            # 更新主URL表的状态
            is_detected = 1 if "发现XSS漏洞" in result else 0
            sql_update = """
                UPDATE urls 
                SET is_xss_detected = %s, 
                    xss_scan_result = %s, 
                    scan_date = CURRENT_TIMESTAMP 
                WHERE id = %s
            """
            cursor.execute(sql_update, (is_detected, result, url_id))

        connection.commit()
    finally:
        connection.close()

def get_scan_logs():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT l.id, u.url, l.scan_result, l.scan_date 
                FROM xss_scan_logs l
                JOIN urls u ON l.url_id = u.id
                ORDER BY l.scan_date DESC
            """)
            return cursor.fetchall()
    finally:
        connection.close()

def get_recent_scans():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM urls 
                WHERE scan_date IS NOT NULL 
                ORDER BY scan_date DESC 
                LIMIT 5
            """)
            return cursor.fetchall()
    finally:
        connection.close()

def log_sql_scan(url_id, result):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # 记录到扫描日志表
            sql_log = "INSERT INTO sql_scan_logs (url_id, scan_result) VALUES (%s, %s)"
            cursor.execute(sql_log, (url_id, result))

            # 更新主URL表的状态
            is_detected = 1 if "发现SQL注入漏洞" in result else 0
            sql_update = """
                UPDATE urls 
                SET is_sql_detected = %s, 
                    sql_scan_result = %s, 
                    sql_scan_date = CURRENT_TIMESTAMP 
                WHERE id = %s
            """
            cursor.execute(sql_update, (is_detected, result, url_id))

        connection.commit()
    finally:
        connection.close()

def get_sql_scan_logs():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT l.id, u.url, l.scan_result, l.scan_date 
                FROM sql_scan_logs l
                JOIN urls u ON l.url_id = u.id
                ORDER BY l.scan_date DESC
            """)
            return cursor.fetchall()
    finally:
        connection.close()

def get_all_scan_logs():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # 合并XSS和SQL注入扫描日志
            cursor.execute("""
                (SELECT 'xss' AS scan_type, l.id, u.url, l.scan_result, l.scan_date 
                 FROM xss_scan_logs l
                 JOIN urls u ON l.url_id = u.id)
                UNION
                (SELECT 'sql' AS scan_type, l.id, u.url, l.scan_result, l.scan_date 
                 FROM sql_scan_logs l
                 JOIN urls u ON l.url_id = u.id)
                ORDER BY scan_date DESC
            """)
            return cursor.fetchall()
    finally:
        connection.close()