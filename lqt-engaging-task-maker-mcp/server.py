"""Let's Quit Teaching — Engaging Task Maker hosted read-only MCP."""
import logging
import os
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lqt.engaging_task")
mcp = FastMCP("LQT Engaging Task Maker")

@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def openai_domain_verification(request: Request) -> PlainTextResponse:
    return PlainTextResponse(os.environ.get("OPENAI_DOMAIN_CHALLENGE", ""))

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def get_engaging_task_framework(grade_level: str, learning_target_or_standard_or_topic: str) -> dict:
    """Retrieve mandatory original LQT Engaging Task Maker format; gather grade first, then target, standard or topic, one question at a time. Create one substantial five-section task, not a worksheet."""
    logger.info("LQT TOOL CALLED: get_engaging_task_framework")
    if not grade_level.strip():
        return {"next_question":"What is the learner's grade level?","rule":"Accept any unrestricted free-text grade or learning context."}
    if not learning_target_or_standard_or_topic.strip():
        return {"next_question":"What is the learning target for the lesson? If you don't have one, provide the standard or topic."}
    return {
      "grade_level":grade_level.strip(),"learning_target_or_standard_or_topic":learning_target_or_standard_or_topic.strip(),
      "intake":["Ask what is the learner's grade level","Ask what is the learning target; accept standard or topic instead"],
      "intake_rule":"Ask one missing question per turn, and never repeat known answers. No grade menus or restricted grade choices. If supplied only a standard or topic, derive one concise grade-appropriate I can learning target, honoring actual rigor and content; do not invent jurisdiction or standard wording.",
      "output":"Produce exactly ONE meaningful learning task in five numbered sections in this order.",
      "sections":[
        {"heading":"1. Learning Task","requirements":"Give compelling task title, specific learner-facing steps, what learners think/do/create/explain/justify and submit or demonstrate; feasible materials and format; clear alignment to I can target; educator implementation cues. Task must elicit observable evidence. A worksheet must not be the primary task."},
        {"heading":"2. Engagement Qualities","requirements":"Identify at least FOUR purposeful engagement qualities actually operating in this task; for each, explain how it advances target-aligned thinking, evidence or agency, not just entertainment; avoid gimmicks, novelty without learning, artificial competition or busywork."},
        {"heading":"3. Possible Success Criteria","requirements":"Concise TASK-SPECIFIC observable list; describe the quality of the learner product/performance at success. Do NOT create a four-level progressive success criteria table unless specifically requested."},
        {"heading":"4. Possible Scaffolds","requirements":"Practical grade-appropriate access supports for challenged learners; preserve intellectual demand, thinking and ownership; identify when to fade supports."},
        {"heading":"5. Possible Extension","requirements":"One authentic, qualitatively deeper or transferable challenge, not more of the same work."}
      ],
      "global_rules":["Use learner and learners, never student/students.","Learner-facing directions, examples and vocabulary must fit freely entered grade level without diluting rigor.","Task meaningful and manageable; no worksheet as primary activity.","No unsupported factual claims or fabricated resources.","If educator asks another task, design a meaningfully DIFFERENT option rather than cosmetic rewrite.","Don't claim to invoke other tools or create actual downloadable assets unless performed.","Close by inviting educator to ask for another task or a complete ready-to-teach expansion."],
      "source":"Original user-provided Engaging Learning Task Maker v1.0.1 SKILL.md"}

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def review_engaging_task(grade_level: str, learning_target: str, task_description: str) -> dict:
    """Audit an existing engaging learning task against original five-part framework, four purposeful qualities, observable evidence, rigor, accessibility and grade-friendly language."""
    logger.info("LQT TOOL CALLED: review_engaging_task")
    if not grade_level.strip(): return {"next_question":"What is the learner's grade level?"}
    if not learning_target.strip(): return {"next_question":"What is the learning target or standard/topic?"}
    if not task_description.strip(): return {"next_question":"Please paste or describe the task you want me to review."}
    return {"grade_level":grade_level,"learning_target":learning_target,"task_description":task_description,
      "review_checks":["Original ordered five-section design", "Meaningful task generates directly observable evidence of learning", "Worksheet not primary task", "At least four engagement qualities are purposeful and explained", "Success criteria describe quality of task-specific evidence and are observable", "Scaffolds support access without doing learners' thinking or lowering rigor", "Extension deepens or transfers rather than adds volume", "Learner-facing directions fit entered grade and terminology says learners", "Directions, product and logistical details are implementable"],
      "response_instruction":"Identify strengths, unmet criteria, and concrete repairs with revised learner directions where useful. Do not claim a check passes without evidence. Preserve five sections; do not introduce four-level success table unless asked."}

if __name__ == "__main__":
    mcp.run(transport="http",host="0.0.0.0",port=int(os.environ.get("PORT","8000")))
