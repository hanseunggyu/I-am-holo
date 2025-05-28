# profile.py
from flask import Blueprint, render_template, session, redirect, url_for
from db import get_connection

# Blueprint 생성
profile_bp = Blueprint('profile', __name__, template_folder='templates')

# 라우터 등록
@profile_bp.route('/profile')
def profile():
    if 'email' not in session:
        return redirect(url_for('home'))

    email = session['email']
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM profiles WHERE user_email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('profile.html', user=user)


@profile_bp.route('/profile_edit', methods=['GET', 'POST'])
def edit_profile():
    if 'email' not in session:
        return redirect(url_for('home'))

    email = session['email']
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        nickname = request.form['nickname']
        mbti = request.form['mbti']
        age = request.form['age']
        gender = request.form['gender']
        job = request.form['job']
        location = request.form['location']
        religion = request.form['religion']
        dream = request.form['dream']
        love_style = request.form['love_style']
        preference = request.form['preference']
        keywords = request.form['keywords']
        phone = request.form['phone']
        instagram = request.form['instagram']
        profile_img_url = request.form.get('profile_img_url') or None

        cursor.execute("""
            UPDATE profiles
            SET nickname=%s, mbti=%s, age=%s, gender=%s, job=%s, location=%s,
                religion=%s, dream=%s, love_style=%s, preference=%s, keywords=%s,
                phone=%s, instagram=%s, profile_img=%s
            WHERE user_email=%s
        """, (nickname, mbti, age, gender, job, location, religion,
              dream, love_style, preference, keywords, phone, instagram, profile_img_url, email))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('profile.profile'))

    cursor.execute("SELECT * FROM profiles WHERE user_email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template("edit_profile.html", user=user)
