# 🐦 Earlybird — AI-Powered Deadline Tracking Agent

> An agentic deadline tracker that classifies urgency, notifies via Telegram
> with human-in-the-loop approval, and exposes tools via MCP for AI interoperability.

**Capstone Project — 5-Day AI Agents Intensive with Google (Kaggle, June 2026)**
**Track: Agents for Business**

---

## 🎯 Problem It Solves

Students and professionals miss deadlines not because they forget to add them,
but because reminders arrive without context or urgency — or worse, spam them
until they're ignored entirely.

Earlybird fixes this with an agent that:
- Classifies every deadline by urgency automatically
- Previews reminders to the user **before** sending them (human-in-the-loop)
- Exposes deadline data as MCP tools so any AI agent can query or act on it

---

## 🧠 Concepts Demonstrated (3 of 5 from the course)

| Concept | Day | Implementation |
|---|---|---|
| **MCP Server** | Day 2 | `mcp_server.py` — 3 tools exposing deadline data |
| **Agent Skills / SKILL.md** | Day 3 | `SKILL.md` — portable triage skill with rules |
| **Human-in-the-Loop Guardrail** | Day 4 | `telegram_bot.py` — approve before email sends |

---

## 🏗️ Architecture

---

## 🔌 MCP Tools

Any AI agent can connect to Earlybird and call:

| Tool | Description |
|---|---|
| `list_deadlines()` | All pending deadlines in next 7 days |
| `get_urgent_deadlines()` | Only deadlines due today or tomorrow |
| `add_deadline(task, subject, date, type)` | Add a new deadline |

---

## 🛡️ The Guardrail (Human-in-the-Loop)

The agent **never sends an email autonomously.**

Before any digest is sent, the Telegram bot previews the
upcoming deadlines and shows two buttons:

- ✅ **Yes, send email** → triggers `send_digest()`
- ❌ **Skip** → no action taken

This ensures the agent acts as an assistant, not an autonomous actor.

---

## 🚀 Tech Stack

- **Backend:** Python, Flask
- **Database:** Supabase (PostgreSQL)
- **AI:** Azure AI Foundry (GPT-4.1-mini via Respo7)
- **Notifications:** Gmail SMTP + Telegram Bot API
- **Agentic Layer:** MCP (`python-telegram-bot`, `mcp`)
- **Deployment:** Render

---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/Moh8Ans/Earlybird
cd Earlybird
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set environment variables
Create a `.env` file:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
GMAIL_SENDER=your_gmail
GMAIL_APP_PASSWORD=your_app_password
GMAIL_RECEIVER=your_receiver_email
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
AZURE_FOUNDRY_ENDPOINT=your_endpoint
AZURE_FOUNDRY_KEY=your_key
```

### 4. Run the Flask app
```bash
python app.py
```

### 5. Run the Telegram bot
```bash
python telegram_bot.py
```

### 6. Run the MCP server
```bash
python mcp_server.py
```

---

## 📁 Project Structure

---

## 👤 Author

**Mohammed Anas S**
B.Tech CSE, MES Institute of Technology and Management, Kerala
[GitHub](https://github.com/Moh8Ans)

---

*Built during the 5-Day AI Agents Intensive Vibe Coding Course with Google — Kaggle, June 2026*

