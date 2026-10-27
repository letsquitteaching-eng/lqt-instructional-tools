"""LQT When Will I EVER Use This? — authentic relevance tools."""
import logging
import os
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lqt.real_world_relevance")
mcp = FastMCP("When Will I EVER Use This?")

@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def openai_domain_verification(request: Request) -> PlainTextResponse:
    return PlainTextResponse(os.environ.get("OPENAI_DOMAIN_CHALLENGE", ""))

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def get_real_world_relevance_framework(grade_level: str, learning_target_or_content: str) -> dict:
    """Retrieve the original LQT 5+5 real-world relevance format for any freely typed grade level and a learning target, standard, skill or topic."""
    logger.info("LQT TOOL CALLED: get_real_world_relevance_framework")
    if not grade_level.strip() or not learning_target_or_content.strip():
        return {"error": "Ask only for the first missing item: free-text learner grade level, then learning target or content. Do not produce examples until both are available."}
    return {
        "grade_level":grade_level.strip(),"learning_target_or_content":learning_target_or_content.strip(),
        "intake":"Ask ONE question per turn, first 'What is the learner’s grade level?', then 'What is the Learning Target or content you are teaching?' Skip supplied answers. Accept all freely typed grades including Pre-K, Kindergarten, any K-12, mixed, college, adult; no menu or restrictive choices. A standard, skill, or topic is sufficient; do not demand a rewritten target.",
        "output_order":[
          {"part":"PART 1 — 5 REAL-WORLD CONNECTIONS","count":5,"each":"Engaging short title, authentic situation described in learner-friendly language, and explicit HOW/WHY the exact knowledge or skill is used there. Vary life, community, hobbies, work, science, creative or civic contexts where truly relevant."},
          {"part":"PART 2 — 5 WAYS TO MAKE IT RELEVANT RIGHT NOW","count":5,"each":"Engaging activity name, 2–4 sentences describing exactly what learners do, clear authentic purpose or connection, and a requirement to apply the target knowledge or skill. Activities must be meaningfully different, inexpensive and feasible."}
        ],
        "design_rules":["Exactly five distinct connections PLUS five distinct experiences, in that order, numbered separately 1–5 in each section.","Adapt learner-facing wording to educator-entered grade: understandable vocabulary and sentence length without reducing disciplinary rigor.","Connections must be true and substantive, not made-up jobs or decorative themes. Explain HOW or WHY content is used.","Avoid a list consisting only of careers; choose useful varied real-world settings.","Real application activities should require thinking, explaining, investigating, designing, deciding, solving, communicating or analyzing as appropriate.","Preserve learning-target rigor and avoid equipment-heavy or high-prep tasks unless requested.","Use 'learner' and 'learners'; never 'student' or 'students'.","Do not imply every learner will use every example. Never fabricate unverifiable real-world claims or sources."],
        "exact_followup":"Would you like me to develop one of these five classroom activities? If so, tell me the number.",
        "if_selected":"Invoke develop_relevance_activity with the selected Part 2 activity number, its activity title and summary; expand ONLY the chosen activity unless educator requests more.",
        "source":"User-provided When Will I EVER Use This? v1.0.1 skill and Original Tool Example.md"
    }

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def develop_relevance_activity(grade_level: str, learning_target_or_content: str, activity_number: int, activity_title: str, activity_summary: str) -> dict:
    """Expand only one of the five previously offered classroom experiences into the author's original ready-to-teach activity format."""
    logger.info("LQT TOOL CALLED: develop_relevance_activity")
    if not grade_level.strip() or not learning_target_or_content.strip() or not activity_title.strip() or not activity_summary.strip():
        return {"error":"Provide a freely typed grade, target/content and the previously selected classroom activity name and summary; do not invent missing selections."}
    if not 1 <= activity_number <= 5:
        return {"error":"Select a classroom activity number from 1 to 5, not one of the real-world connection examples."}
    return {"grade_level":grade_level,"learning_target_or_content":learning_target_or_content,"selected_classroom_activity":activity_number,"activity_title":activity_title,"activity_summary":activity_summary,
      "only_expand_selected_activity":True,
      "required_sections":["Activity Title","Connection to the Learning Target/content","Purpose / Real-World Connection","Materials","Clear learner directions","Suggested grouping","Approximate time","Evidence of Learning","Teacher role","Possible scaffold that preserves learner thinking","Possible extension that deepens or transfers the same learning","Brief closing/reflection prompt connecting the activity back to why the learning is useful"],
      "requirements":["Classroom-ready, economical, realistic time and resources; no unspecified access assumptions.","Directions and outputs readable by learners of the entered grade; maintain cognitive rigor.","The real-world use must be authentic, explicit and essential to the task, not a label pasted onto standard practice.","Use 'learner' and 'learners' rather than 'student' or 'students'.","Do not expand all five activities or manufacture details of activity not supplied."],
      "exact_followup":"Would you like more real-world examples or another activity developed?"}

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
