from mcp.server.fastmcp import FastMCP
from digest import get_deadlines, classify
from db import supabase
from datetime import date

mcp = FastMCP("Earlybird")


@mcp.tool()
def list_deadlines() -> list[dict]:
    """Get all upcoming pending deadlines within the next 7 days."""
    deadlines = get_deadlines()
    return [
        {
            "task": d["task_name"],
            "subject": d["subject"],
            "due_date": d["due_date"],
            "urgency": classify(d["due_date"]),
            "type": d.get("type", ""),
        }
        for d in deadlines
    ]


@mcp.tool()
def add_deadline(task_name: str, subject: str, due_date: str, type: str = "Assignment") -> dict:
    """
    Add a new deadline to Earlybird.
    due_date must be in YYYY-MM-DD format.
    """
    result = supabase.table("deadlines").insert({
        "task_name": task_name,
        "subject": subject,
        "due_date": due_date,
        "type": type,
        "status": "Pending"
    }).execute()

    return {"status": "added", "data": result.data}


@mcp.tool()
def get_urgent_deadlines() -> list[dict]:
    """Returns only deadlines due today or tomorrow — for urgent triage."""
    deadlines = get_deadlines()
    urgent = [
        d for d in deadlines
        if classify(d["due_date"]) in ["🔴 DUE TODAY", "🔴 DUE TOMORROW"]
    ]
    return urgent


if __name__ == "__main__":
    print("🔌 Earlybird MCP server running...")
    mcp.run()