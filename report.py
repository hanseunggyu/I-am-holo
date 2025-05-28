from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from db import get_connection

report_bp = Blueprint('report', __name__)  

@report_bp.route('/report/<reported_email>', methods=['POST'])
def report_user(reported_email):
    if 'email' not in session:
        return redirect(url_for('home'))

    reporter_email = session['email']
    if reporter_email == reported_email:
        flash("자기 자신은 신고할 수 없습니다.", "warning")
        return redirect(url_for('chat.chat', user_email=reported_email))

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO reports (reporter_email, reported_email)
            VALUES (%s, %s)
        """, (reporter_email, reported_email))
        conn.commit()
        flash("신고가 접수되었습니다.", "success")
    except Exception as e:
        conn.rollback()
        print("❌ 신고 실패:", e)
        flash("이미 신고한 사용자입니다.", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('chat', user_email=reported_email))

def is_reported_many_times(user_email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM reports
        WHERE reported_email = %s
    """, (user_email,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count >= 1