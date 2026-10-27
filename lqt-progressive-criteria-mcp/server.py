"""LQT Progressive Success Criteria: evidence-based, age-adaptive planning tools."""
import logging
import os
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lqt.progressive_criteria")
mcp = FastMCP("LQT Progressive Success Criteria")

@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def openai_domain_verification(request: Request) -> PlainTextResponse:
    return PlainTextResponse(os.environ.get("OPENAI_DOMAIN_CHALLENGE", ""))

LEVELS = [
    {"level": 4, "name": "Exceeds", "stem": "I CAN … AND I …", "meaning": "Extension beyond daily mastery that remains connected to the learning target"},
    {"level": 3, "name": "Meets", "stem": "I CAN …", "meaning": "Complete and independent demonstration of the day's learning target in the task"},
    {"level": 2, "name": "Approaching", "stem": "I CAN … BUT I …", "meaning": "Partial demonstration with specific task-based mistakes or gaps"},
    {"level": 1, "name": "Beginning", "stem": "NO, I CANNOT … YET.", "meaning": "The targeted skill has not yet been demonstrated; describe missing observable evidence without demeaning the learner"},
]

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def get_progressive_criteria_framework(grade_level: str, learning_target: str, learning_task: str) -> dict:
    """Retrieve the author's EXACT 2-row, 4-column Progressive Success Criteria format for any educator-typed grade level, with learner-friendly language and observable evidence."""
    logger.info("LQT TOOL CALLED: get_progressive_criteria_framework")
    if not grade_level.strip() or not learning_target.strip() or not learning_task.strip():
        return {"error": "Need grade level, learning target, and an actual learning task (upload or educator description) before generating criteria. Ask only for the missing information, one question at a time."}
    return {
        "grade_level": grade_level.strip(), "learning_target": learning_target.strip(), "learning_task": learning_task.strip(),
        "intake_questions": ["What is the learner’s grade level?", "What is the learning target?", "Please upload the learning task or describe what learners will create, do, or demonstrate."],
        "intake_policy": "Ask ONE plain-text question per turn in this order: grade, learning target, learning task. Offer upload OR free-text task description; never require a file. Do not generate a criteria table before all three are known. If grade or target has already been provided, skip the corresponding question. If the learner task is missing, ask for it explicitly and stop.",
        "grade_input": "Accept ANY free-text grade or learning setting; never present grade buttons, dropdowns, ranges or restricted choices. Use an already-provided grade without asking again.",
        "table": {"rows": 2, "columns": 4, "headers_left_to_right": ["4", "3", "2", "1"],
                  "levels_left_to_right": LEVELS,
                  "cell_format": "Bold, separate I CAN statement FIRST, followed by 2–3 separate bullet points with concrete, task-specific, observable evidence, errors, or missing skills. Do not turn bullet points into prose paragraphs."},
        "quality_requirements": ["Every success criterion must be anchored to evidence visible in the specified learner task or work product; never fabricate a task when none is described.","Match exactly the author-provided level order and stems.", "Use plain learner-facing language appropriate to the exact user-entered grade and age while retaining intended cognitive rigor.", "Show evidence the learner can locate in their own work, rather than vague adjectives or inferred attitudes.", "Make Meets genuinely fulfill the learning target and Exceeds a connected extension; Approach and Beginning describe honest visible gaps.", "Use learner, not student. Do not assign points unless requested."],
        "next_question": "Would you like some tools and resources for learners to access during their learning for this task?",
        "if_yes": "Suggest optional level-specific scaffolds, tools and resources that support movement toward the next level, without doing the learner's thinking.",
        "if_no": "Is there another Progressive Success Criteria I can help design for you?",
        "source": "User-provided LQT Progressive Success Criteria v1.0.2 instructional skill"
    }

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def review_progressive_criteria(grade_level: str, learning_target: str, learning_task: str, exceeds: str, meets: str, approaching: str, beginning: str) -> dict:
    """Review teacher-supplied four levels for required I CAN stems and 2–3 bullets; flag format gaps and provide evidence-based review questions, without falsely certifying age appropriateness."""
    logger.info("LQT TOOL CALLED: review_progressive_criteria")
    if not all(x.strip() for x in (grade_level,learning_target,learning_task,exceeds,meets,approaching,beginning)):
        return {"error":"Grade level, learning target, task and all four level texts are required."}
    rows = []
    for num,label,value,stem in [(4,"Exceeds",exceeds,"i can"),(3,"Meets",meets,"i can"),(2,"Approaching",approaching,"i can"),(1,"Beginning",beginning,"no, i cannot")]:
        lines = [s.strip() for s in value.splitlines() if s.strip()]
        bullets = [s for s in lines if s.startswith(("- ","* ","• "))]
        rows.append({"level":num,"name":label,"has_expected_stem":any(stem in s.lower() for s in lines),"bullet_count":len(bullets),"has_2_to_3_bullets":2 <= len(bullets) <= 3,"review_questions":["Is each bullet observable in the learner's actual work?", "Is vocabulary understandable for this exact grade while maintaining rigor?", "Does this level truly distinguish the specified kind of evidence from adjacent levels?"]})
    return {"grade_level":grade_level,"learning_target":learning_target,"learning_task":learning_task,"format_checks":rows,"required_table":"2 rows × 4 columns, headers 4, 3, 2, 1 left to right","required_progression":"Exceeds / Meets / Approaching / Beginning","caution":"Mechanical checks only; the educator must judge task alignment, grade-level accessibility, and mastery quality."}

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.environ.get("PORT","8000")))
