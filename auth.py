from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta
import secrets
from db import get_connection

auth_bp = Blueprint('auth', __name__)

# ✅ 회원가입
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


# ✅ 로그인
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


# ✅ 1. 이메일(아이디) 찾기
@auth_bp.route('/find_email', methods=['GET', 'POST'])
def find_email():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.email
            FROM users u
            JOIN profiles p ON u.email = p.user_email
            WHERE p.nickname = %s AND p.phone = %s
        """, (name, phone))
        
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            flash(f"📧 등록된 이메일: {user['email']}", 'success')
        else:
            flash("❌ 일치하는 정보가 없습니다.", 'danger')

    return render_template("find_email.html")


# ✅ 2. 비밀번호 재설정 요청
@auth_bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form['email']
        token = secrets.token_hex(16)
        expire = datetime.now() + timedelta(minutes=15)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.execute("UPDATE users SET reset_token=%s, reset_expire=%s WHERE email=%s",
                           (token, expire, email))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('auth.reset_password', token=token))
        else:
            flash("❌ 존재하지 않는 이메일입니다.", 'danger')
            cursor.close()
            conn.close()

    return render_template("reset_password_request.html")


# ✅ 3. 비밀번호 재설정 실행
@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # 토큰 유효성 확인
    cursor.execute("SELECT email, reset_expire FROM users WHERE reset_token=%s", (token,))
    user = cursor.fetchone()

    if not user or user['reset_expire'] < datetime.now():
        cursor.close()
        conn.close()
        return "❌ 링크가 만료되었거나 유효하지 않습니다."

    if request.method == 'POST':
        new_pw = request.form['password']

        # 평문으로 비밀번호 업데이트 (암호화 X)
        cursor.execute("""
        UPDATE users 
        SET password = %s, reset_token = NULL, reset_expire = NULL 
        WHERE email = %s
        """, (new_pw, user['email']))
        conn.commit()

        cursor.close()
        conn.close()
        return render_template('reset_password.html', password_changed=True)

    cursor.close()
    conn.close()
    return render_template("reset_password.html")
