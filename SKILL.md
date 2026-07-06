# 🐦 Earlybird — Deadline Triage Skill

## What This Skill Does
Earlybird tracks academic and work deadlines, classifies them by urgency,
and sends reminders via email and Telegram with human approval before acting.

## Available Tools

| Tool | What it does |
|---|---|
| `list_deadlines()` | Get all pending deadlines in the next 7 days |
| `get_urgent_deadlines()` | Get only deadlines due today or tomorrow |
| `add_deadline(task, subject, date, type)` | Add a new deadline |

## Urgency Classification

| Label | Meaning |
|---|---|
| 🔴 DUE TODAY | Act immediately |
| 🔴 DUE TOMORROW | High priority |
| 🟡 DUE SOON | Due within 3 days |
| 🟢 COMING UP | Due within 7 days |

## Triage Rules (Guardrail)
- NEVER send a reminder without human approval via Telegram first
- NEVER remind about a deadline not present in the database
- ALWAYS call `get_urgent_deadlines()` before `list_deadlines()` — urgent first
- If no deadlines exist, respond with encouragement, not silence

## Example Agent Workflow
1. User says "remind me about my deadlines"
2. Agent calls `get_urgent_deadlines()` first
3. If urgent items exist → send Telegram preview and wait for approval
4. If approved → trigger email digest
5. If not urgent → call `list_deadlines()` and summarize