# chat.py
from flask import Blueprint, render_template, session, redirect, url_for
from db import get_connection

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chatlist')
def chatlist():
    if 'email' not in session:
        return redirect(url_for('home'))
    my_email = session['email']
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT
            CASE
                WHEN sender = %s THEN receiver
                ELSE sender
            END AS chat_partner
        FROM messages
        WHERE sender = %s OR receiver = %s
    """, (my_email, my_email, my_email))
    partner_emails = [row[0] for row in cursor.fetchall()]

    matches = []
    if partner_emails:
        format_strings = ','.join(['%s'] * len(partner_emails))
        cursor.execute(f"""
            SELECT p.nickname, p.mbti, p.age, p.location, p.animal_icon, p.instagram, p.phone, p.user_email
            FROM profiles p
            WHERE p.user_email IN ({format_strings})
        """, tuple(partner_emails))
        matches = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("chatlist.html", matches=matches)
