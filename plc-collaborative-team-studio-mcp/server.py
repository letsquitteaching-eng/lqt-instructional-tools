import json
import os
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse

PORT = int(os.getenv("PORT", "8000"))
DATA_DIR = Path(os.getenv("DATA_DIR", "/tmp/plc-studio"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = Path(os.getenv("DATABASE_PATH", str(DATA_DIR / "plc_studio.sqlite3")))
DOMAIN_TOKEN = (os.getenv("OPENAI_DOMAIN_CHALLENGE", "") or os.getenv("OPENAI_DOMAIN_VERIFICATION_TOKEN", "")).strip()
LOCK = threading.Lock()

mcp = FastMCP(
    "PLC/Collaborative Team Studio",
    instructions=(
        "Facilitate evidence-centered PLC and collaborative-team meetings. "
        "Do not invent evidence, consensus, owners, deadlines, or saved state. "
        "Confirm records before marking them confirmed."
    ),
    host="0.0.0.0",
    port=PORT,
)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def connect():
    con = sqlite3.connect(DB_PATH, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA foreign_keys=ON")
    return con


def init_db():
    with LOCK, connect() as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS meetings (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                grade TEXT NOT NULL,
                subject TEXT,
                team TEXT NOT NULL,
                pathway TEXT NOT NULL CHECK(pathway IN ('singleton','team')),
                purpose TEXT NOT NULL CHECK(purpose IN ('plan','evidence','continue')),
                duration INTEGER,
                participants TEXT,
                target TEXT,
                prior_id TEXT,
                status TEXT NOT NULL DEFAULT 'draft',
                stage INTEGER NOT NULL DEFAULT 0,
                notes_json TEXT NOT NULL DEFAULT '{}',
                decisions TEXT NOT NULL DEFAULT '',
                open_questions TEXT NOT NULL DEFAULT '',
                actions_json TEXT NOT NULL DEFAULT '[]',
                include_next_agenda INTEGER NOT NULL DEFAULT 0,
                confirmed_by_user INTEGER NOT NULL DEFAULT 0,
                version INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        con.commit()


init_db()


@mcp.custom_route("/health", methods=["GET"])
async def health(_: Request):
    return JSONResponse({"status": "ok", "service": "plc-collaborative-team-studio"})


@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def openai_challenge(_: Request):
    if not DOMAIN_TOKEN:
        return PlainTextResponse("Domain verification token not configured", status_code=404)
    return PlainTextResponse(DOMAIN_TOKEN)


def protocol_for(purpose: str, duration: int):
    common = (
        "Begin with free-entry grade/course, singleton or team, purpose, time, and typed/spoken preference. "
        "Ask one clear question at a time. Preserve teacher judgment. Distinguish observations, interpretations, "
        "proposals, and confirmed decisions. Never invent evidence, attribution, agreement, owners, deadlines, "
        "or improvement. When no evidence exists, plan how to elicit it. At close, review the record before confirmation."
    )
    if purpose == "evidence":
        steps = [
            ("evidence", "Describe the evidence", "What do we actually see in the learner evidence?", 8),
            ("interpret", "Interpret cautiously", "What might this evidence mean, and what alternative explanations should we consider?", 10),
            ("corroborate", "Corroborate", "What additional learner evidence would strengthen or challenge that interpretation?", 7),
            ("respond", "Decide the response", "What should we adjust, preserve, reteach, scaffold, extend, or test next?", 10),
            ("check", "Plan the next evidence", "What will tell us whether that response helped?", 5),
        ]
    elif purpose == "continue":
        steps = [
            ("resume", "Resume prior commitments", "Which prior commitments and evidence plans need review first?", 7),
            ("evidence", "Examine what happened", "What evidence do we have since the previous meeting?", 10),
            ("interpret", "Interpret", "What does that evidence suggest, and what remains uncertain?", 10),
            ("respond", "Respond", "What should we do next based on the evidence?", 10),
            ("check", "Set the review point", "What evidence will we bring back, and when will we review it?", 5),
        ]
    else:
        steps = [
            ("learning", "Clarify the learning", "What should learners understand and be able to do?", 5),
            ("criteria", "Make success visible", "What qualities would show that learners are successful?", 5),
            ("task", "Design the task", "What will learners do that makes their thinking visible?", 8),
            ("respond", "Anticipate and support", "Where might learners need support or greater challenge?", 7),
            ("check", "Plan the next evidence", "How will you find out whether the response helped learners?", 5),
        ]
    return {
        "instructions": common,
        "purpose": purpose,
        "duration": duration,
        "steps": [
            {"key": k, "title": t, "question": q, "minutes": mins}
            for k, t, q, mins in steps
        ],
        "closing": "Confirm decisions, owners, deadlines, evidence, and review point; offer the next agenda.",
    }


@mcp.tool(
    annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=False),
)
def get_meeting_protocol(purpose: str, duration: int = 45) -> dict:
    """Start here. Return facilitation instructions and a purposeful meeting protocol. Read-only; it uses only bounded server content and changes no state."""
    if purpose not in {"plan", "evidence", "continue"}:
        raise ValueError("purpose must be plan, evidence, or continue")
    if duration < 10 or duration > 240:
        raise ValueError("duration must be between 10 and 240 minutes")
    return protocol_for(purpose, duration)


@mcp.tool(
    annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=False),
)
def list_studio_meetings() -> list[dict]:
    """List saved Studio meetings. Read-only; it retrieves bounded Studio records and changes no state. For a public multi-user deployment, add OAuth and scope this query to the authenticated user before enabling this tool."""
    with connect() as con:
        rows = con.execute(
            "SELECT id,title,team,grade,purpose,status,updated_at,version FROM meetings ORDER BY updated_at DESC LIMIT 100"
        ).fetchall()
    return [dict(r) for r in rows]


@mcp.tool(
    annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=False),
)
def load_studio_meeting(meeting_id: str) -> dict:
    """Load one saved meeting. Read-only; it retrieves a bounded Studio record and changes no state. Public multi-user deployments must enforce authorization before returning a record."""
    with connect() as con:
        row = con.execute("SELECT * FROM meetings WHERE id=?", (meeting_id,)).fetchone()
    if not row:
        raise ValueError("Meeting not found")
    d = dict(row)
    d["notes"] = json.loads(d.pop("notes_json"))
    d["actions"] = json.loads(d.pop("actions_json"))
    d["confirmed_by_user"] = bool(d["confirmed_by_user"])
    d["include_next_agenda"] = bool(d["include_next_agenda"])
    return d


@mcp.tool(
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=False),
)
def create_studio_meeting(
    meeting_id: str,
    grade: str,
    team: str,
    title: str,
    pathway: str,
    purpose: str,
    subject: Optional[str] = None,
    duration: Optional[int] = None,
    participants: Optional[str] = None,
    target: Optional[str] = None,
    prior_id: Optional[str] = None,
) -> dict:
    """Create a durable draft meeting. Writes a new bounded Studio record but does not overwrite/delete existing records or contact external parties."""
    if pathway not in {"singleton", "team"}:
        raise ValueError("pathway must be singleton or team")
    if purpose not in {"plan", "evidence", "continue"}:
        raise ValueError("purpose must be plan, evidence, or continue")
    if duration is not None and not 10 <= duration <= 240:
        raise ValueError("duration must be between 10 and 240 minutes")
    ts = now_iso()
    with LOCK, connect() as con:
        existing = con.execute("SELECT * FROM meetings WHERE id=?", (meeting_id,)).fetchone()
        if existing:
            return load_studio_meeting(meeting_id)
        con.execute(
            """INSERT INTO meetings
            (id,title,grade,subject,team,pathway,purpose,duration,participants,target,prior_id,created_at,updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (meeting_id,title,grade,subject,team,pathway,purpose,duration,participants,target,prior_id,ts,ts),
        )
        con.commit()
    return load_studio_meeting(meeting_id)


@mcp.tool(
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=False),
)
def save_studio_progress(
    meeting_id: str,
    expected_version: int,
    notes: Optional[dict[str, str]] = None,
    decisions: Optional[str] = None,
    open_questions: Optional[str] = None,
    actions: Optional[list[dict]] = None,
    include_next_agenda: Optional[bool] = None,
    confirmed_by_user: Optional[bool] = None,
    stage: Optional[int] = None,
) -> dict:
    """Save progress to an existing meeting using optimistic version checking. Writes supplied fields only; stale versions fail instead of overwriting newer work, so it is non-destructive."""
    if stage is not None and not 0 <= stage <= 6:
        raise ValueError("stage must be between 0 and 6")
    with LOCK, connect() as con:
        row = con.execute("SELECT * FROM meetings WHERE id=?", (meeting_id,)).fetchone()
        if not row:
            raise ValueError("Meeting not found")
        if row["version"] != expected_version:
            raise ValueError(f"Version conflict: current version is {row['version']}. Reload before saving.")
        updates, values = [], []
        mapping = {
            "notes_json": json.dumps(notes, ensure_ascii=False) if notes is not None else None,
            "decisions": decisions,
            "open_questions": open_questions,
            "actions_json": json.dumps(actions, ensure_ascii=False) if actions is not None else None,
            "include_next_agenda": int(include_next_agenda) if include_next_agenda is not None else None,
            "confirmed_by_user": int(confirmed_by_user) if confirmed_by_user is not None else None,
            "stage": stage,
        }
        for col, val in mapping.items():
            if val is not None:
                updates.append(f"{col}=?")
                values.append(val)
        if confirmed_by_user is True:
            updates.append("status=?")
            values.append("confirmed")
        elif confirmed_by_user is False:
            updates.append("status=?")
            values.append("draft")
        updates += ["version=version+1", "updated_at=?"]
        values += [now_iso(), meeting_id, expected_version]
        cur = con.execute(
            f"UPDATE meetings SET {', '.join(updates)} WHERE id=? AND version=?",
            values,
        )
        if cur.rowcount != 1:
            raise ValueError("Version conflict. Reload before saving.")
        con.commit()
    return load_studio_meeting(meeting_id)


@mcp.tool(
    annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=False),
)
def get_studio_record(meeting_id: str) -> dict:
    """Return a model-readable agenda/minutes/action record for one saved meeting. Read-only; it does not send, share, export, or modify anything."""
    m = load_studio_meeting(meeting_id)
    lines = [
        f"# {m['title']}",
        f"Grade/course: {m['grade']}",
        f"Team: {m['team']}",
        f"Purpose: {m['purpose']}",
        f"Status: {m['status']}",
        "",
        "## Notes",
    ]
    notes = m.get("notes") or {}
    if notes:
        for key, value in notes.items():
            lines.append(f"- {key}: {value}")
    else:
        lines.append("- No notes saved yet.")
    lines += ["", "## Decisions", m.get("decisions") or "No confirmed decisions recorded."]
    lines += ["", "## Actions"]
    actions = m.get("actions") or []
    if actions:
        for a in actions:
            lines.append(
                f"- {a.get('action','')} | Owner: {a.get('owner','')} | Due: {a.get('due','')} | "
                f"Evidence: {a.get('evidence','')} | Review: {a.get('review','')}"
            )
    else:
        lines.append("- No actions recorded.")
    lines += ["", "## Open questions", m.get("open_questions") or "None recorded."]
    if m.get("include_next_agenda"):
        lines += ["", "## Next agenda", "Review the agreed evidence, unresolved questions, and progress on action steps."]
    return {"meeting_id": meeting_id, "version": m["version"], "status": m["status"], "record": "\n".join(lines)}


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
