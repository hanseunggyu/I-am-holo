from flask import Blueprint, render_template, request, redirect, url_for, session
from db import get_connection

auth_bp = Blueprint('auth', __name__, template_folder='templates')

# 회원가입 처리
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if register_user(email, password):
            return redirect(url_for('auth.login'))
        else:
            return "회원가입 실패"

    return render_template('register.html')

# 로그인 처리
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if login_user(email, password):
            session['user_email'] = email
            return redirect(url_for('profile.profile'))
        else:
            return "로그인 실패"

    return render_template('login.html')


# 로그아웃
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


# 이미 있던 함수는 아래에 유지
def register_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
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
        return password == result[0]
    return False
