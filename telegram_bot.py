import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)
from dotenv import load_dotenv
from digest import get_deadlines, classify, send_digest

load_dotenv()

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


# ── Helpers ──────────────────────────────────────────────────────────────────

def build_telegram_message(deadlines):
    """Same logic as digest.py but plain text for Telegram."""
    if not deadlines:
        return "✅ No deadlines this week. Enjoy the break!"

    lines = ["🐦 *Earlybird Digest Preview*\n"]
    for d in deadlines:
        label = classify(d["due_date"])
        lines.append(
            f"{label}\n"
            f"  *{d['subject']}* — {d['task_name']}\n"
            f"  📅 {d['due_date']}  |  📋 {d.get('type', '')}\n"
        )
    lines.append("\n_Send this as email digest?_")
    return "\n".join(lines)


# ── Guardrail: Human-in-the-loop ─────────────────────────────────────────────

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /check — shows upcoming deadlines and asks for approval before emailing.
    This is the human-in-the-loop guardrail (Day 4 concept).
    Agent does NOT send the email until you explicitly approve here.
    """
    deadlines = get_deadlines()
    message = build_telegram_message(deadlines)

    # Only show approve button if there are deadlines
    if deadlines:
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Yes, send email", callback_data="approve_digest"),
                InlineKeyboardButton("❌ Skip", callback_data="skip_digest"),
            ]
        ])
    else:
        keyboard = None

    await update.message.reply_text(
        message,
        parse_mode="Markdown",
        reply_markup=keyboard
    )


async def handle_approval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the Yes/No button tap — the actual guardrail decision point."""
    query = update.callback_query
    await query.answer()

    if query.data == "approve_digest":
        try:
            send_digest()  # reuses your existing digest.py function
            await query.edit_message_text("✅ Email digest sent successfully!")
        except Exception as e:
            await query.edit_message_text(f"❌ Failed to send digest: {e}")

    elif query.data == "skip_digest":
        await query.edit_message_text("⏭️ Skipped. No email sent.")


# ── Basic Commands ────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🐦 *Earlybird Bot*\n\n"
        "Commands:\n"
        "/check — Preview deadlines & approve email send\n"
        "/list  — Just list upcoming deadlines\n",
        parse_mode="Markdown"
    )


async def list_deadlines(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Simple list — no approval flow, no email."""
    deadlines = get_deadlines()
    message = build_telegram_message(deadlines).split("\n_Send")[0]  # strip approval prompt
    await update.message.reply_text(message, parse_mode="Markdown")


# ── App Entry ─────────────────────────────────────────────────────────────────

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(CommandHandler("list", list_deadlines))
    app.add_handler(CallbackQueryHandler(handle_approval))
    print("🐦 Earlybird bot is running...")
    app.run_polling()


if __name__ == "__main__":
    run_bot()