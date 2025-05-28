@app.route('/profile_edit', methods=['GET', 'POST'], endpoint='edit_profile')
def profile_edit():
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

        # 프로필 이미지 URL은 선택적이므로 None으로 설정
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
        return redirect(url_for('profile'))

    cursor.execute("SELECT * FROM profiles WHERE user_email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template("edit_profile.html", user=user)