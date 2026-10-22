"""LQT Sort Generator: read-only, teacher-led sorting design tools."""
import os
import logging
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lqt.sort")
mcp = FastMCP("LQT Sort Generator")
OPENAI_DOMAIN_CHALLENGE = os.environ.get("OPENAI_DOMAIN_CHALLENGE", "NOT_CONFIGURED")

@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def openai_domain_verification(request: Request) -> PlainTextResponse:
    return PlainTextResponse(OPENAI_DOMAIN_CHALLENGE)

SORT_TYPES = {'Knowledge Building': ['Sequential Sorts', 'Classification/Category Sorts', 'Examples vs. Non-Examples', 'True/False (Yes/No) Sorts', 'Matching Sorts', 'Prior Knowledge vs. New Learning'], 'Critical Thinking': ['Cause-and-Effect', 'Compare-and-Contrast', 'Fact vs. Opinion', 'Evidence-Based (claim ↔ evidence)', 'Multiple Perspectives', 'Analogical', 'Error Analysis', 'Value/Opinion (Ethical)'], 'Application': ['Problem-Solution', 'Prediction (pre/post)', 'Priority (Ranking)', 'Hypothesis Testing (supports/doesn’t support)']}

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def get_sort_menu(grade_level: str, learning_target: str) -> dict:
    """Retrieve the complete LQT 18-type Sort menu organized by Knowledge Building, Critical Thinking and Application. Requires grade level and learning target; ChatGPT tailors a distinct, grade-aligned title, two sample items, and learner reasoning for each type. No learner data is accessed."""
    logger.info("LQT TOOL CALLED: get_sort_menu")
    if not grade_level.strip() or not learning_target.strip():
        return {"error": "Grade level and learning target/topic are required. Ask these one at a time, grade level first."}
    return {"grade_level":grade_level.strip(), "learning_target":learning_target.strip(),"categories":SORT_TYPES,"menu_requirements":{"coverage":"Give a concise tailored idea for EVERY type, grouped under the three exact category labels", "for_each":"Engaging title, 1–2 sentence description, approximately two grade/content-specific examples, and reasoning/justification learners provide", "ending":"Which Sort should I build out for you now?"},"instructional_principle":"Learners organize information and explain the basis of their decisions; preserve intended learning and rigor.","source":"LQT Sort Generator original instructional skill and example"}

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def get_sort_build_framework(grade_level: str, learning_target: str, sort_type: str, number_of_cards: int = 24) -> dict:
    """Get LQT's classroom-ready Sort-building sequence and guardrails for a chosen sort. Returns required sections, printable card count guidance, evidence and reasoning prompts; ChatGPT authors subject-accurate cards and model answer with teacher review."""
    logger.info("LQT TOOL CALLED: get_sort_build_framework")
    if not grade_level.strip() or not learning_target.strip() or not sort_type.strip():
        return {"error":"Grade level, learning target and selected sort type are required."}
    if not 4 <= number_of_cards <= 60:
        return {"error":"Card count must be between 4 and 60; normally use 18–30 unless the sort requires a different number."}
    names=[n for arr in SORT_TYPES.values() for n in arr]
    if sort_type.casefold() not in [n.casefold() for n in names]:
        return {"error":"Select a sort type from the original 18-type menu.","valid_types":SORT_TYPES}
    return {"grade_level":grade_level.strip(),"learning_target":learning_target.strip(),"selected_sort":sort_type,"suggested_card_count":number_of_cards,"build_sections":["QUICK OVERVIEW: learning objective, time, grouping, materials and observable learning evidence","CARD SET — PRINTABLE: clear headers, concise grade-appropriate items; usually 18–30 unless another count suits the sort","TEACHER DIRECTIONS: setup, learner task, reasoning prompts, sample key/exemplar with defensible reasoning","SCAFFOLDS & ACCESS: front-end support, prompts and tool/criterion cues without removing thinking","EXTENSION / DEEPENING: 2–3 same-target transfer options","CHECKS FOR UNDERSTANDING: 3–5 probes of reasoning","MISCONCEPTIONS TO WATCH FOR: 3–5 content-specific errors","DIGITAL & PHYSICAL OPTIONS: realistic current classroom alternatives","FINISH & TRANSFER: 2 ways learners apply insights to new responses or problems","OPTIONAL 4-LEVEL RUBRIC: accuracy, reasoning, collaboration where applicable, transfer"],"requirements":["Sort card placement alone is insufficient: learner explanation/justification is essential","Preserve complexity and grade-appropriate disciplinary accuracy","Refer to learners, not students","For formats with multiple defensible answers, clarify rationale rather than assert a single universal key","Finish with: Would you like me to turn the card set into a printable PDF?","If requested, create a genuinely printable card-layout PDF; tool returns guidance, not a PDF"],"source":"LQT Sort Generator original instructional skill and example"}

if __name__ == "__main__":
    mcp.run(transport="http",host="0.0.0.0",port=int(os.environ.get("PORT","8000")))
