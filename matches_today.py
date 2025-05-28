from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from db import get_connection

matches_today_bp = Blueprint('matches_today', __name__)  

@matches_today_bp.route('/matches_today')
def matches_today():
    if 'email' not in session:
        return redirect(url_for('home'))

    my_email = session['email']

    conn = get_connection()
    cursor = conn.cursor()

    # 오늘 서로 좋아요를 한 경우만 필터링
    cursor.execute("""
        SELECT p.nickname, p.mbti, p.age, p.location, p.animal_icon, p.instagram, p.phone, p.user_email
        FROM profiles p
        WHERE p.user_email IN (
            SELECT l1.to_user
            FROM likes l1
            JOIN likes l2
              ON l1.to_user = l2.from_user AND l1.from_user = l2.to_user
            WHERE l1.from_user = %s
              AND DATE(l1.created_at) = CURDATE()
              AND DATE(l2.created_at) = CURDATE()
        )
    """, (my_email,))
    
    matches = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("matches_today.html", matches=matches)