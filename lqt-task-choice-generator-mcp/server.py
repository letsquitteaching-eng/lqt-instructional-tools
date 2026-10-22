"""LQT Task Choice Generator: meaningful choices, common target and evidence."""
import os
import logging
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lqt.task_choice")
mcp = FastMCP("LQT Task Choice Generator")

@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def domain_verification(request: Request) -> PlainTextResponse:
    return PlainTextResponse(os.getenv("OPENAI_DOMAIN_CHALLENGE", "Verification token not set"))

CHOICE_PRINCIPLES = {
    "quantity": 5,
    "common_target": "All five choices elicit evidence of the same learning target and success expectations.",
    "cognitive_demand": "No choice should be substantively easier or require less essential thinking.",
    "meaningful_difference": "Vary how learners process, apply, investigate, represent, or justify the learning, beyond merely choosing a poster, slideshow, or video.",
    "practicality": "Every choice must be realistic for the age and a classroom lesson.",
    "required_fields": ["Task", "What Learners Will Do", "Evidence to Look For"],
    "language": "Use learner or learners, not student or students.",
    "intake": ["Ask the learner's grade level first", "Then ask for the lesson learning target"],
    "after_options": "Ask: Would you like more options? If yes, produce five additional genuinely different choices, avoiding prior choices. If no, close briefly."
}

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def get_task_choice_framework(grade_level: str, learning_target: str) -> dict:
    """Retrieve the authored LQT five-choice design requirements for a grade and learning target. Use them to craft five distinct classroom tasks with the same rigor and learner evidence."""
    logger.info("LQT TOOL CALLED: get_task_choice_framework")
    if not grade_level.strip() or not learning_target.strip():
        return {"error":"Grade level and learning target are required."}
    return {
        "grade_level": grade_level.strip(), "learning_target": learning_target.strip(),
        "design_requirements": CHOICE_PRINCIPLES,
        "suggested_task_variation": ["Investigate a case and defend a conclusion", "Solve and justify a novel problem", "Compare contrasting examples using the target", "Construct a model and explain how it works", "Diagnose a mistake and defend a revision"],
        "note": "The five variation examples are optional starting points, not five pre-filled tasks. Adapt each to the target while maintaining comparable evidence and cognitive demand.",
        "source": "Author-supplied LQT Task Choice Generator skill"
    }

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def assess_task_choice_alignment(learning_target: str, proposed_choices: list[str], shared_evidence: str = "") -> dict:
    """Return an evidence-alignment checklist to critique teacher-provided choice descriptions. It does not automatically certify rigor or assess actual learners."""
    logger.info("LQT TOOL CALLED: assess_task_choice_alignment")
    if not learning_target.strip():
        return {"error": "A learning target is required."}
    if not proposed_choices or len(proposed_choices)>10 or any(not isinstance(c,str) or not c.strip() for c in proposed_choices):
        return {"error":"Supply 1-10 nonempty descriptions of proposed choices."}
    return {
        "learning_target":learning_target.strip(), "proposed_choices":proposed_choices,
        "common_evidence_expectation":shared_evidence.strip() or "Specify what reasoning, explanation, application, or product would prove this learning target for every choice.",
        "checks":[
            "Does each choice require learners to demonstrate the full target, rather than tangential knowledge?",
            "Does every choice require comparable reasoning, rigor, independence, and quality of evidence?",
            "Are choices meaningfully different in process or thinking, beyond output format or decoration?",
            "Are materials, time, and learner age appropriate for a normal lesson?",
            "Can the teacher use the same success criteria to judge evidence from all choices?"
        ],
        "response_instruction":"For each provided choice, explain any alignment or rigor risk and recommend a concrete repair; do not claim this tool has independently evaluated learner outcomes.",
        "limitations":"Uses teacher-provided descriptions only. No access to learner records or automatic assessment."
    }

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
