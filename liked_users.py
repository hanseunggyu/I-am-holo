# liked_users.py
from flask import Blueprint, render_template, session, redirect, url_for
from db import get_connection

liked_users_bp = Blueprint('liked_users', __name__, template_folder='templates')

@liked_users_bp.route('/liked')
def liked_users():
    if 'email' not in session:
        return redirect(url_for('home'))

    email = session['email']
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.nickname, p.mbti, p.age, p.location, p.animal_icon, p.instagram, p.phone, p.user_email
        FROM profiles p
        JOIN likes l ON p.user_email = l.to_user
        WHERE l.from_user = %s
    """, (email,))

    liked = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("liked_users.html", liked=liked)
