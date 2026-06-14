import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date, timedelta
from dotenv import load_dotenv
from db import supabase

load_dotenv()

SENDER = os.environ.get("GMAIL_SENDER")
PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
RECEIVER = os.environ.get("GMAIL_RECEIVER")


def get_deadlines():
    today = date.today().isoformat()
    week_end = (date.today() + timedelta(days=7)).isoformat()

    result = (
        supabase.table("deadlines")
        .select("*")
        .eq("status", "Pending")
        .gte("due_date", today)
        .lte("due_date", week_end)
        .order("due_date", desc=False)
        .execute()
    )
    return result.data


def classify(due_date_str):
    due = date.fromisoformat(due_date_str)
    today = date.today()
    delta = (due - today).days

    if delta == 0:
        return "🔴 DUE TODAY"
    elif delta == 1:
        return "🔴 DUE TOMORROW"
    elif delta <= 3:
        return "🟡 DUE SOON"
    else:
        return "🟢 COMING UP"


def build_html(deadlines):
    if not deadlines:
        return "<p>No deadlines this week. Enjoy the break! 🎉</p>"

    grouped = {}
    for d in deadlines:
        label = classify(d["due_date"])
        grouped.setdefault(label, []).append(d)

    html = """
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto;">
        <h2 style="background:#1a1a2e; color:#00d4ff; padding:16px; border-radius:8px;">
            🐦 Earlybird Morning Digest
        </h2>
        <p style="color:#555;">Good morning Anas! Here's what's coming up:</p>
    """

    order = ["🔴 DUE TODAY", "🔴 DUE TOMORROW", "🟡 DUE SOON", "🟢 COMING UP"]
    colors = {
        "🔴 DUE TODAY": "#ff4444",
        "🔴 DUE TOMORROW": "#ff6666",
        "🟡 DUE SOON": "#ffaa00",
        "🟢 COMING UP": "#00aa44"
    }

    for label in order:
        if label not in grouped:
            continue
        color = colors[label]
        html += f"""
        <h3 style="color:{color}; border-left: 4px solid {color};
            padding-left:10px;">{label}</h3>
        <ul style="list-style:none; padding:0;">
        """
        for d in grouped[label]:
            html += f"""
            <li style="background:#f9f9f9; margin:6px 0; padding:10px;
                border-radius:6px; border-left: 3px solid {color};">
                <strong>{d['subject']}</strong> — {d['task_name']}<br>
                <small style="color:#888;">📅 {d['due_date']} &nbsp;|&nbsp;
                📋 {d.get('type','')}</small>
            </li>
            """
        html += "</ul>"

    html += """
        <p style="color:#aaa; font-size:12px; margin-top:20px;">
            Sent by Earlybird 🐦
        </p>
    </div>
    """
    return html


def send_digest():
    deadlines = get_deadlines()
    html_body = build_html(deadlines)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🐦 Earlybird Digest — {date.today().strftime('%A, %b %d')}"
    msg["To"] = RECEIVER

    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, RECEIVER, msg.as_string())

    print(f"✅ Digest sent to {RECEIVER}")


if __name__ == "__main__":
    send_digest()