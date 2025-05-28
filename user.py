# user.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from db import get_connection

user_bp = Blueprint('user', __name__)

@user_bp.route('/delete-account', methods=['GET'], endpoint='delete_account_confirm')
def delete_account_confirm():
    if 'email' not in session:
        return redirect(url_for('logout'))
    return render_template('delete_account.html')  # 확인용 템플릿

@user_bp.route('/delete-account-action', methods=['POST'], endpoint='delete_account_action')
def delete_account_action():
    if 'email' not in session:
        return redirect(url_for('logout'))
    email = session['email']
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 메시지, 좋아요, 프로필, 유저(인증) 순으로 삭제
        cursor.execute("DELETE FROM messages WHERE sender=%s OR receiver=%s", (email, email))
        cursor.execute("DELETE FROM likes WHERE from_user=%s OR to_user=%s", (email, email))
        cursor.execute("DELETE FROM profiles WHERE user_email=%s", (email,))
        cursor.execute("DELETE FROM users WHERE email=%s", (email,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
        session.clear()
    return redirect(url_for('home'))
