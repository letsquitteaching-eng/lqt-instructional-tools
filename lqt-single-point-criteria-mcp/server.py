"""LQT single-point success criteria: instructional framework and alignment checks."""
import logging
import os
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lqt.single_point")
mcp = FastMCP("LQT Single-Point Success Criteria")

@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def openai_domain_verification(request: Request) -> PlainTextResponse:
    return PlainTextResponse(os.environ.get("OPENAI_DOMAIN_CHALLENGE", ""))

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def get_single_point_framework(grade_level: str, learning_target: str, learner_task: str, specific_evidence: str = "skip") -> dict:
    """Return the authored LQT single-point criteria format for ANY user-typed grade or learning setting; does not assign scores or create performance bands."""
    logger.info("LQT TOOL CALLED: get_single_point_framework")
    if not grade_level.strip() or not learning_target.strip() or not learner_task.strip():
        return {"error":"Grade level or learning setting, learning target, and learner task are required."}
    return {
        "grade_level":grade_level.strip(), "learning_target":learning_target.strip(),
        "learner_task":learner_task.strip(), "specific_evidence":specific_evidence.strip() or "skip",
        "intake_order":["What grade level or learning setting are you designing for? Please type your answer.","What is the Learning Target?","What task will learners complete to show this learning?","Is there any specific evidence of learning you want incorporated? You can also say 'skip'."],
        "grade_policy":"Unrestricted typed input; never present a fixed choice menu, grade range or grade-band selector. Keep the educator's wording exactly, including Pre-K, K-12, college, adult education or mixed-grade classes.",
        "output":{"title":"Single-Point Success Criteria", "columns":["WHAT I GOT","WHAT SUCCESS LOOKS LIKE","WHAT I NEED"],"rows":"3–5 horizontally aligned rows; each describes ONE observable, learner-friendly quality of learning", "center":"One observable quality of success anchored to learning target and task, not procedure or compliance", "left":"2–3 extensions deepening the SAME quality through transfer, stronger reasoning, precision, revision or critique", "right":"2–3 concrete scaffolds for the SAME quality: models, stems, organizers, prompts, vocabulary, guided practice, feedback, peer rehearsal", "feedback_stems":["You've got ___ because...","Next, focus on ___ by...","A scaffold that may help is..."]},
        "rules":["This is NOT a multi-level rubric: no Beginning, Developing, Proficient, Distinguished or Advanced bands.","Align all three cells of each row around the same quality.","Use 'learner' rather than 'student'.", "Keep rigor; do not use extension as more work or scaffolds as lower expectations.","Do not assign scores or points unless explicitly requested.","Do not invent or verify academic standards.","If given a broad standard, adapt to an 'I can' target preserving rigor without inventing new content."],
        "follow_up":"Would you like me to make these criteria more concise, more learner-friendly, or more specific to the task?",
        "source":"LQT Single-Point Success Criteria Tool author-provided skill"}

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def review_single_point_alignment(learning_target: str, learner_task: str, criteria_rows: list[dict]) -> dict:
    """Review teacher-provided single-point rows for structure, aligned supports and extensions; advisory checks, not an automatic semantic grading system."""
    logger.info("LQT TOOL CALLED: review_single_point_alignment")
    if not learning_target.strip() or not learner_task.strip() or not criteria_rows:
        return {"error":"Learning target, task, and at least one row are required."}
    if len(criteria_rows)>15:return {"error":"Review up to 15 rows at a time."}
    checks=[]
    for i,row in enumerate(criteria_rows,1):
        if not isinstance(row,dict):return {"error":"Each row must be an object containing the three column headings."}
        headings=["WHAT I GOT","WHAT SUCCESS LOOKS LIKE","WHAT I NEED"]
        missing=[h for h in headings if not str(row.get(h,"")).strip()]
        checks.append({"row":i,"missing_columns":missing,"teacher_checks":["Is the center an observable learning quality instead of task compliance?","Do all extensions deepen THIS center quality rather than add unrelated work?","Do all supports help the learner demonstrate THIS quality without reducing rigor?","Does each side contain two or three useful, actionable options?"]})
    return {"row_count":len(criteria_rows),"recommended_rows":"3–5", "checks":checks,"whole_rubric_checks":["Does the set address the learning target and task?","Do criteria avoid performance bands and numerical scoring?","Are learner-friendly wording and feedback stems provided?"],"limitations":"Structural and professional review prompts only; this tool does not judge semantic alignment automatically or assign scores."}

if __name__ == "__main__":
    mcp.run(transport="http",host="0.0.0.0",port=int(os.environ.get("PORT","8000")))
