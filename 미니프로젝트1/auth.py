from db import get_connection

def register_user(email, password, nickname):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, password, nickname) VALUES (%s, %s, %s)",
            (email, password, nickname)  # 암호화 없이 그대로 저장
        )
        conn.commit()
        return True
    except Exception as e:
        print("❌ 회원가입 오류:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        return password == result[0]  # 단순 비교
    return False

