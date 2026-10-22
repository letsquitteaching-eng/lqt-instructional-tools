"""LQT Gradual Release Idea Generator: read-only, evidence-led design helpers."""
import json
import logging
import os
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lqt.gradual_release")
mcp = FastMCP("LQT Gradual Release Idea Generator")

# OpenAI ownership verification for this Render hostname.
# This verification value is intended to be publicly returned by the endpoint.
OPENAI_DOMAIN_CHALLENGE = "eKGwD9sxxaSGBjd0qlbZW6VF5GRhf70thNiRSXG65Vg"

@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def openai_domain_verification(request: Request) -> PlainTextResponse:
    return PlainTextResponse(OPENAI_DOMAIN_CHALLENGE)

PHASES = {
    "I Do": {"purpose": "Make the disciplinary thinking visible through concise modeling.", "responsibility": "teacher makes decisions and reasoning explicit", "evidence": "Learners predict/explain a model step, rather than report confidence.", "possible_supports": ["worked example", "think-aloud", "visual model"]},
    "We Do": {"purpose": "Elicit learner thinking through guided practice and adaptive prompting.", "responsibility": "learners begin decisions with teacher guidance", "evidence": "All-learner response with reasoning or short worked example.", "possible_supports": ["targeted prompts", "partially worked example", "vocabulary cues"]},
    "They Do": {"purpose": "Peers explain, compare, justify, revise, or apply the essential thinking.", "responsibility": "learners explain choices with peers", "evidence": "Teacher samples individual explanations and partner reasoning.", "possible_supports": ["discussion cues", "task representation", "self-check prompt"]},
    "You Do": {"purpose": "Elicit independent evidence with minimal teacher prompting.", "responsibility": "learners carry the central reasoning independently", "evidence": "Individual aligned product/response with reasoning.", "possible_supports": ["accessibility tools that do not supply reasoning", "optional self-monitoring checklist"]}
}

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def get_gradual_release_framework(grade_level: str, learning_target: str, instructional_minutes: int = 45) -> dict:
    """Retrieve LQT's authored four-phase framework for a specified grade and learning target. Returns phase purposes, evidence checks, guidance and scaffold types for ChatGPT to adapt; does not auto-generate a standards-verified lesson."""
    logger.info("LQT TOOL CALLED: get_gradual_release_framework")
    if not grade_level.strip() or not learning_target.strip():
        return {"error": "Grade level and learning target are required."}
    if not 5 <= instructional_minutes <= 240:
        return {"error": "Instructional minutes must be between 5 and 240."}
    return {"grade_level": grade_level.strip(), "learning_target": learning_target.strip(), "instructional_minutes": instructional_minutes, "phases": PHASES, "guidance": {"sequence": "Flexible; phases are not fixed-length or mandatory one-way blocks", "time": "Time suggestions are flexible estimates, not equal quarters", "teacher_decision": "Use learner reasoning, prevalence and foundational nature of errors, and self-correction to move forward or return to support", "cognitive_demand": "Maintain learning target and learner thinking across phases", "style": "Use learner, not student"}, "source": "LQT Gradual Release Idea Generator author-provided skill and example"}

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def suggest_release_response(learning_target: str, phase: str, evidence_observed: str, misconception_foundational: bool = False, widespread_error: bool = False, self_correction_with_prompt: bool = False) -> dict:
    """Apply transparent, teacher-supplied evidence flags to suggest whether to advance, continue support, or briefly return to modeling. Advisory only; never claims to have assessed real learners."""
    logger.info("LQT TOOL CALLED: suggest_release_response")
    if not learning_target.strip() or not evidence_observed.strip():
        return {"error": "Learning target and a de-identified description of evidence are required."}
    if phase not in PHASES:
        return {"error": "Phase must be one of: " + ", ".join(PHASES)}
    if misconception_foundational and widespread_error:
        move = "Briefly return to focused modeling, then elicit fresh individual evidence."
    elif misconception_foundational or widespread_error:
        move = "Remain in or return to guided practice and check reasoning with a new prompt."
    elif self_correction_with_prompt:
        move = "Fade one prompt and gather individual evidence before releasing further."
    else:
        move = "Consider greater learner independence, but first corroborate with individual evidence."
    return {"learning_target": learning_target.strip(), "current_phase": phase, "suggested_next_move": move, "basis": {"foundational_misconception": misconception_foundational, "widespread_error": widespread_error, "self_corrects_with_prompt": self_correction_with_prompt}, "limitations": "Recommendations use teacher-provided flags and are not automated evaluation of learner work. Do not include identifiable learner information.", "evidence_follow_up": "Collect a brief response that shows each learner's reasoning relative to the target."}

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
