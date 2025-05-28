from db import get_connection

def register_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (%s, %s)",
            (email, password)
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

    if result and password == result[0]:
        # 로그인 성공 → 활동중으로 표시
        cursor.execute("UPDATE users SET is_online = 1 WHERE email = %s", (email,))
        conn.commit()

        cursor.close()
        conn.close()
        return True

    cursor.close()
    conn.close()
    return False

