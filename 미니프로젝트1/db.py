import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        user='proj-1',
        passwd='admin',
        charset='utf8',
        database='proj-1'
    )
    conn.autocommit = True  # 명시적 커밋 자동 설정
    return conn

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("✅ MySQL 연결 성공!")
        conn.close()
    except Exception as e:
        print("❌ 연결 실패:", e)