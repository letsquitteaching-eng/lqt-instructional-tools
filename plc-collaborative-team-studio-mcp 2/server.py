import os
from typing import Optional

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse

PORT = int(os.getenv("PORT", "8000"))
DOMAIN_TOKEN = (
    os.getenv("OPENAI_DOMAIN_CHALLENGE", "")
    or os.getenv("OPENAI_DOMAIN_VERIFICATION_TOKEN", "")
).strip()

mcp = FastMCP(
    "PLC/Collaborative Team Studio",
    instructions=(
        "Facilitate evidence-centered PLC and collaborative-team meetings without storing user data. "
        "Ask for grade/course first, then whether the user is working individually or with a team, "
        "meeting purpose, available time, and typed or spoken facilitation preference. Ask whether the "
        "school or district requires a specific documentation form; if yes, ask the user to upload it. "
        "Do not invent evidence, consensus, owners, deadlines, learner improvement, or prior meeting history. "
        "For continued work, use only prior records or documentation supplied in the current conversation."
    ),
    host="0.0.0.0",
    port=PORT,
)


@mcp.custom_route("/health", methods=["GET"])
async def health(_: Request):
    return JSONResponse(
        {
            "status": "ok",
            "service": "plc-collaborative-team-studio",
            "storage": "stateless",
        }
    )


@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def openai_challenge(_: Request):
    if not DOMAIN_TOKEN:
        return PlainTextResponse(
            "Domain verification token not configured", status_code=404
        )
    return PlainTextResponse(DOMAIN_TOKEN)


def protocol_for(purpose: str, duration: int) -> dict:
    common = [
        "Begin by collecting free-entry grade/course.",
        "Ask whether this is an individual inquiry or a collaborative-team/PLC meeting.",
        "Confirm the meeting purpose and available time.",
        "Ask whether the user prefers typed facilitation or spoken facilitation when the host supports voice.",
        "Ask whether the school or district requires a specific form for documenting this work. If yes, ask the user to upload it before final documentation is produced.",
        "Ask one clear facilitation question at a time and preserve educator judgment.",
        "Distinguish observations, interpretations, proposals, and confirmed decisions.",
        "Never invent evidence, consensus, attribution, owners, deadlines, learner improvement, or prior history.",
        "When evidence is missing, help the team plan how to elicit it.",
        "Before closing, review decisions, actions, owners, deadlines, evidence to collect, and the next review point with the user.",
        "The Studio is stateless. Do not claim that a meeting has been saved. For future continuation, provide a handoff record the user can keep and supply in a later conversation.",
    ]

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
            ("handoff", "Recover prior work", "Please paste or upload the prior meeting record, required form, minutes, or handoff document you want to continue from.", 5),
            ("resume", "Review prior commitments", "Which prior commitments, unresolved questions, and evidence plans need attention first?", 7),
            ("evidence", "Examine what happened", "What evidence do we have since the previous meeting?", 10),
            ("interpret", "Interpret", "What does that evidence suggest, and what remains uncertain?", 8),
            ("respond", "Respond", "What should we do next based on the evidence?", 8),
            ("check", "Set the review point", "What evidence will we bring back, and when will we review it?", 5),
        ]
    else:
        steps = [
            ("learning", "Clarify the learning", "What should learners understand and be able to do?", 5),
            ("criteria", "Make success visible", "What qualities would show that learners are successful?", 5),
            ("task", "Design the task", "What will learners do that makes their thinking visible?", 8),
            ("support", "Anticipate and support", "Where might learners need support or greater challenge?", 7),
            ("evidence", "Plan evidence", "What will learners do or produce that will let us judge the impact of the design?", 5),
            ("check", "Plan the response", "How will the team respond to the evidence it collects?", 5),
        ]

    return {
        "purpose": purpose,
        "duration": duration,
        "operating_rules": common,
        "steps": [
            {"key": key, "title": title, "question": question, "minutes": minutes}
            for key, title, question, minutes in steps
        ],
        "closing_products": [
            "meeting agenda/minutes",
            "confirmed decisions",
            "action steps with owners and dates only when supplied or confirmed",
            "open questions",
            "evidence to collect and review point",
            "next-meeting agenda when useful",
            "completed school/district documentation when the user supplied a required form",
            "portable handoff record for continuing the work in a future conversation",
        ],
    }


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=True, destructiveHint=False, openWorldHint=False
    )
)
def get_meeting_protocol(purpose: str, duration: int = 45) -> dict:
    """Return a bounded, stateless facilitation protocol for planning learning, examining evidence, or continuing prior work. It stores nothing and contacts no external service."""
    if purpose not in {"plan", "evidence", "continue"}:
        raise ValueError("purpose must be plan, evidence, or continue")
    if duration < 10 or duration > 240:
        raise ValueError("duration must be between 10 and 240 minutes")
    return protocol_for(purpose, duration)


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=True, destructiveHint=False, openWorldHint=False
    )
)
def create_meeting_handoff(
    title: str,
    grade_or_course: str,
    team_or_individual: str,
    purpose: str,
    observations: Optional[str] = None,
    interpretations: Optional[str] = None,
    confirmed_decisions: Optional[str] = None,
    action_steps: Optional[str] = None,
    open_questions: Optional[str] = None,
    evidence_to_collect: Optional[str] = None,
    review_point: Optional[str] = None,
    required_form_note: Optional[str] = None,
) -> dict:
    """Format user-supplied meeting information into a portable handoff record. Stateless and read-only: it does not save, send, share, or modify any user data."""
    if purpose not in {"plan", "evidence", "continue"}:
        raise ValueError("purpose must be plan, evidence, or continue")

    sections = [
        f"# {title}",
        f"Grade/course: {grade_or_course}",
        f"Team/individual: {team_or_individual}",
        f"Purpose: {purpose}",
        "",
        "## Observations / evidence",
        observations or "Not provided.",
        "",
        "## Interpretations",
        interpretations or "Not provided.",
        "",
        "## Confirmed decisions",
        confirmed_decisions or "No confirmed decisions provided.",
        "",
        "## Action steps",
        action_steps or "No confirmed action steps provided.",
        "",
        "## Open questions",
        open_questions or "None provided.",
        "",
        "## Evidence to collect",
        evidence_to_collect or "Not provided.",
        "",
        "## Review point",
        review_point or "Not provided.",
    ]

    if required_form_note:
        sections += ["", "## Required documentation", required_form_note]

    sections += [
        "",
        "## Continue this work",
        "Keep this handoff record and paste or upload it in a future PLC/Collaborative Team Studio conversation. The Studio does not store meeting records between conversations.",
    ]

    return {
        "storage": "none",
        "record": "\n".join(sections),
        "continuation_instruction": (
            "Provide this record in a future conversation to continue the work."
        ),
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
