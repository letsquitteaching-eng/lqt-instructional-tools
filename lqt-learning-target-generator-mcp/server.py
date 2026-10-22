"""LQT Learning Target Generator: standards-grounded, read-only planning tools."""
import logging
import os
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lqt.learning_targets")
mcp = FastMCP("LQT Learning Target Generator")

@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def openai_domain_verification(request: Request) -> PlainTextResponse:
    return PlainTextResponse(os.environ.get("OPENAI_DOMAIN_CHALLENGE", ""))

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def get_learning_target_framework(grade_level: str, standard_text: str, lesson_minutes: int = 60) -> dict:
    """Retrieve LQT's standards-to-daily-learning-target design requirements. Use only the exact user-provided standard; this tool does not verify external standards or generate authoritative standard interpretations."""
    logger.info("LQT TOOL CALLED: get_learning_target_framework")
    if not grade_level.strip() or not standard_text.strip():
        return {"error": "Grade level and the standard exactly as written are required."}
    if not 10 <= lesson_minutes <= 180:
        return {"error": "Lesson minutes must be between 10 and 180."}
    return {
        "grade_level": grade_level.strip(),
        "standard_text": standard_text.strip(),
        "lesson_minutes": lesson_minutes,
        "target_requirements": [
            "Derive each target only from the supplied standard; no unsupported additions.",
            "Preserve the cognitive demand, scope, and intended rigor.",
            "Start every target with 'I can'.",
            "Use learner-friendly wording for the stated grade.",
            "Each target should be suitable for one class period.",
            "Use only as many targets as needed to fully address the standard without over-fragmenting."
        ],
        "required_fields": {
            "Learning Target": "Age-appropriate I can statement",
            "Know": "Key content, concepts, vocabulary or understanding needed",
            "Do": "Observable disciplinary skills, thinking, and actions",
            "Connection to the Standard": "How this daily target advances the provided standard"
        },
        "interaction": {
            "first_question": "What is the learner's grade level?",
            "second_question": "Please provide the standard exactly as written.",
            "post_output_question": "Are these Learning Targets broken down enough for single-day lessons?",
            "yes_follow_up": "Are there more standards you would like to break down?",
            "no_follow_up": "Revise the same targets into more focused daily targets while preserving alignment and rigor."
        },
        "limitations": "The supplied standard is teacher-provided text; do not claim it has been validated against state standards.",
        "source": "LQT Learning Target Generator author-provided instructions"
    }

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def review_daily_target_alignment(grade_level: str, standard_text: str, proposed_targets: list[str], lesson_minutes: int = 60) -> dict:
    """Return a transparent review checklist for teacher-provided daily I-can targets, identifying mechanical issues and criteria requiring professional judgment; does not certify alignment."""
    logger.info("LQT TOOL CALLED: review_daily_target_alignment")
    if not grade_level.strip() or not standard_text.strip() or not proposed_targets:
        return {"error": "Grade level, original standard, and at least one proposed target are required."}
    if not 10 <= lesson_minutes <= 180:
        return {"error": "Lesson minutes must be between 10 and 180."}
    if len(proposed_targets) > 30:
        return {"error": "Review no more than 30 targets at a time."}
    checks = []
    for i, target in enumerate(proposed_targets, 1):
        clean = target.strip()
        checks.append({
            "target_number": i, "target": clean,
            "starts_with_i_can": clean.lower().startswith("i can "),
            "requires_teacher_review": [
                "Does the target follow directly from the standard without adding requirements?",
                "Does it preserve the original cognitive demand and rigor?",
                "Could a learner reasonably demonstrate it within the class period?",
                "Are Know and Do components clear and assessable?"
            ]
        })
    return {
        "grade_level": grade_level.strip(), "standard_text": standard_text.strip(),
        "lesson_minutes": lesson_minutes, "target_checks": checks,
        "whole_standard_checks": [
            "Do the proposed targets collectively cover the full standard?",
            "Is anything important omitted or introduced without support?",
            "Could any targets be combined to avoid unnecessary fragmentation?"
        ],
        "limitations": "Checklist only. This tool does not semantically verify alignment, evaluate curricula, or access external standards."
    }

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
