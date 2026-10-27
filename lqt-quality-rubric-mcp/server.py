"""LQT Quality Rubric Designer: mastery-anchored rubric design guidance."""
import logging
import os
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lqt.quality_rubric")
mcp = FastMCP("LQT Quality Rubric Designer")

@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def openai_domain_verification(request: Request) -> PlainTextResponse:
    return PlainTextResponse(os.environ.get("OPENAI_DOMAIN_CHALLENGE", ""))

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def get_quality_rubric_framework(grade_level: str, learning_target: str, learner_task: str, proficient_expectations: str = "choose for me") -> dict:
    """Support any educator-entered grade level or learning setting. Return the authored LQT framework for building a 2–4 criterion quality rubric. Proficient is the mastery anchor; other levels must describe the same criterion."""
    logger.info("LQT TOOL CALLED: get_quality_rubric_framework")
    if not grade_level.strip() or not learning_target.strip() or not learner_task.strip():
        return {"error": "Grade level, Learning Target, and learner task are required. Ask only one missing question per turn."}
    return {
        "grade_level": grade_level.strip(), "learning_target": learning_target.strip(),
        "learner_task": learner_task.strip(), "proficient_expectations": proficient_expectations.strip() or "choose for me",
        "grade_input_policy": "Always ask the grade level as free-text input. Do not use dropdowns, preset grade choices, grade bands or options such as 3–8 and High School. Accept any educator-entered grade level or learning setting, including Pre-K, kindergarten, K–12, college, adults, mixed grades, and custom labels. Examples are not a menu.",
        "intake": ["What grade level or learning setting are you designing the rubric for? Please type your answer.", "What is the Learning Target?", "What task will learners complete to show this learning?", "For the Proficient level, is there any specific evidence, required element, quality indicator, or expectation you want included? You can also say 'choose for me'."],
        "intake_guidance": "Ask grade level as an open-ended free-text question, never a preset choice list. Do not restrict acceptable grade or learning-setting responses. Ask one question per turn and never repeat known inputs. If an assignment is provided in place of a target, propose an aligned I can target and seek confirmation before continuing. Do not generate the rubric until all four inputs are known.",
        "criteria": {"count": "2–4", "rules": ["Each criterion is observable, distinct, and aligned to target and task", "Focus on quality rather than compliance, formatting or effort", "Do not duplicate the entire Learning Target in every criterion", "Treat required components as quality indicators only when they evidence mastery"]},
        "levels": {"Distinguished": "YES [the full Proficient quality] AND [meaningful deepening of that same quality, not just more]", "Proficient": "YES [criterion-specific mastery evidence]", "Developing": "YES [core Proficient quality] BUT [specific gap, inconsistency or limitation to revise]", "Beginning": "NO [core quality not demonstrated] YET."},
        "design_order": "Write Proficient FIRST for each criterion; then derive Distinguished, Developing, and Beginning from that same criterion-specific mastery quality.",
        "output": {"heading": "Quality Rubric", "sections": ["Learning Target", "Learner Task", "What Proficient Means", "Rubric", "Using the Rubric During Learning", "Feedback Stems"], "columns": ["Criteria", "Distinguished", "Proficient", "Developing", "Beginning"], "rows": "2–4", "learner_prompts": 3, "feedback_stems": 3},
        "scoring": "Do not assign points, percentages, weights or grades unless explicitly requested; preserve Proficient as mastery anchor.",
        "style": "Use learner/learners, never student/students. Keep descriptors concise, age appropriate, specific and revision-useful.",
        "follow_up": "Would you like me to make the rubric more concise, more learner-friendly, or more specific to the task?",
        "source": "LQT Quality Rubric Designer original skill"
    }

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def review_quality_rubric(learning_target: str, learner_task: str, rubric_rows: list[dict], grade_level: str = "unspecified") -> dict:
    """Check a teacher-supplied rubric for structural YES/AND/BUT/YET features and return criteria for human review of alignment and quality. Advisory only."""
    logger.info("LQT TOOL CALLED: review_quality_rubric")
    if not learning_target.strip() or not learner_task.strip() or not rubric_rows:
        return {"error": "A Learning Target, learner task, and at least one rubric row are required."}
    if len(rubric_rows) > 20:
        return {"error": "Review at most 20 rubric rows per request."}
    checks=[]
    for i, row in enumerate(rubric_rows,1):
        vals={k: str(row.get(k, "")).strip() for k in ["Criteria", "Distinguished", "Proficient", "Developing", "Beginning"]}
        d,p,v,b=(vals[k] for k in ["Distinguished","Proficient","Developing","Beginning"])
        checks.append({"row": i, "criterion": vals["Criteria"], "structural_checks": {"criterion_present":bool(vals["Criteria"]), "distinguished_yes_and":d.upper().startswith("YES") and " AND " in d.upper(), "proficient_yes":p.upper().startswith("YES"), "developing_yes_but":v.upper().startswith("YES") and " BUT " in v.upper(), "beginning_no_yet":b.upper().startswith("NO") and b.upper().rstrip(". ").endswith("YET")}, "professional_judgment_checks": ["Does Proficient describe mastery of this distinct criterion?", "Does Distinguished deepen the SAME quality, without introducing a new standard?", "Does Developing give a specific limitation and revision direction?", "Does Beginning identify missing core evidence?", "Is the row aligned to the Learning Target, task, and grade level?"]})
    return {"grade_level":grade_level,"learning_target":learning_target,"learner_task":learner_task,"row_count":len(rubric_rows),"recommended_criteria":"2–4 distinct criteria","rows":checks,"whole_rubric_review":["Are quality criteria distinct and observable, rather than compliance measures?","Do 2–4 criteria cover the intended knowledge and reasoning?","Is Proficient consistently the mastery anchor?","Are no points or percentages added without explicit request?"],"limitations":"Only visible phrase patterns are mechanically checked. Tool does not grade learners or certify semantic alignment."}

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
