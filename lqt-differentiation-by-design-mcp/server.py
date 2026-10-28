"""LQT Differentiation by Design. Read-only instructional support."""
import os
import logging
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("lqt.differentiation")
mcp = FastMCP("LQT Differentiation by Design")

@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def domain_challenge(request: Request) -> PlainTextResponse:
    return PlainTextResponse(os.environ.get("OPENAI_DOMAIN_CHALLENGE", ""))

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def get_differentiation_framework(grade_level: str = "", learning_target_or_standard: str = "", learner_task: str = "", differentiation_need: str = "", focus: str = "") -> dict:
    """Guide educators one question at a time and return the original LQT differentiation design framework after all five inputs. Never restrict grade-level text."""
    log.info("LQT TOOL CALLED: get_differentiation_framework")
    if not grade_level.strip():
        return {"next_question": "What is the learner's grade level?", "grade_entry": "Unrestricted free text, any grade, course or adult setting."}
    if not learning_target_or_standard.strip():
        return {"next_question": "What is the Learning Target or standard?"}
    if not learner_task.strip():
        return {"next_question": "What will learners be doing to learn or demonstrate this target?"}
    if not differentiation_need.strip():
        return {"next_question": "What is the main differentiation need you want to address: readiness, enrichment, engagement, language/literacy access, executive functioning/attention, or another need?"}
    if not focus.strip():
        return {"next_question": "Would you like me to focus primarily on Content Access, Process, Product, Environment & Supports, or choose the best fit for you?"}
    return {
        "grade_level": grade_level.strip(), "learning_target_or_standard": learning_target_or_standard.strip(),
        "learner_task": learner_task.strip(), "differentiation_need": differentiation_need.strip(), "focus": focus.strip(),
        "source": "Original LQT Differentiation by Design v0.3.1 skill", 
        "core_principles": [
            "Keep ONE shared Learning Target and the full intended rigor for every pathway; infer a focused I can target when a standard was provided.",
            "Differentiate access, process, product, environment/supports based on evidence of need, not fixed learner categories.",
            "Typically generate 2–3 neutral, purpose-named manageable pathways, not separate lessons per learner.",
            "Do not give learners who need support easier intellectual work, and do not give learners ready for enrichment simply more work.",
            "Avoid static low/middle/high labels or permanent ability grouping.",
            "Use learner/learners, never student/students. Make learner-facing directions readable at the freely typed grade level without lowering rigor.",
            "Do not make up learner data; suggest what evidence to gather where it is not supplied."],
        "ordered_output": [
            "Learning Anchor: grade, common Learning Target, core task, 2–4 observable success criteria for ALL pathways",
            "Differentiation Plan: 2–3 purposeful pathways with Why, Learner Moves, Teacher Moves, Scaffolds/Tools, Evidence of Learning, How Support Changes",
            "Optional Evidence-Based Flexible Grouping: only if useful; name evidence, purpose, and when to regroup or dissolve",
            "Quick Check for Understanding aligned to the common success criteria",
            "If access blocked / partial understanding / secure: concrete instructional response guidance",
            "Materials & Prep: short realistic list",
            "Teacher Language: 2–3 brief examples when useful",
            "Follow-up: Would you like me to strengthen the scaffolds, enrichment, learner choice, or formative evidence?"],
        "need_specific_guidance": {
            "readiness": "Adjust representation, examples, modeling, prompts, pacing and supports without changing target.",
            "enrichment": "Deepen same target using complexity, transfer, critique, competing explanations, constraints, precision or reasoning; never extra volume alone.",
            "engagement": "Use meaningful choice, relevance, audience, role, context, collaboration or ownership only if they serve learning.",
            "language/literacy": "Use vocabulary, visuals, models, frames, talk, chunking, appropriate audio/read-aloud while maintaining conceptual demand.",
            "executive functioning/attention": "Use visible steps, checklists, time markers, manageable chunks and organizational supports without removing thinking.",
            "product": "Alternative formats must all validly measure identical success criteria."},
        "design_instruction": "Generate a complete practical learner-centered differentiation plan using the supplied task. Do not ask for additional optional constraints unless essential. If educator already supplied inputs, do not repeat them."
    }

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def review_differentiation_plan(grade_level: str = "", learning_target: str = "", learner_task: str = "", draft_plan: str = "") -> dict:
    """Audit a draft for shared rigor, real evidence, responsive supports, meaningful enrichment, access and learner-friendly language."""
    log.info("LQT TOOL CALLED: review_differentiation_plan")
    if not grade_level.strip(): return {"next_question": "What is the learner's grade level?"}
    if not learning_target.strip(): return {"next_question": "What is the Learning Target?"}
    if not learner_task.strip(): return {"next_question": "What is the core learning task?"}
    if not draft_plan.strip(): return {"next_question": "Please paste or describe the differentiation plan to review."}
    return {"grade_level": grade_level, "learning_target": learning_target, "learner_task": learner_task, "draft_plan": draft_plan,
       "quality_checks": ["One shared, unchanged target and intended cognitive rigor across ALL options", "Each option is justified by a specific access or learning need, grounded in current evidence or clearly proposed evidence to collect", "Two to three manageable, neutral purpose-named pathways", "Each pathway includes learner moves, teacher moves, supports, evidence and how/when to adjust or fade", "Two to four common observable success criteria and an aligned check for understanding", "Supports preserve the difficult thinking; enrichment adds complexity or transfer, not extra worksheets", "Product alternatives measure the same target and criteria", "Grouping, if included, uses current evidence and explicit regroup/dissolve triggers rather than fixed labels", "Learner-facing language fits freely entered grade level; uses learner not student", "Teacher prep and three evidence-based next responses are practical"],
       "instruction": "Give evidence-grounded strengths, unmet criteria and concrete revisions. Do not claim the plan passes checks unless draft demonstrates it."}

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
