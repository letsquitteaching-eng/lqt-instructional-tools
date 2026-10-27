"""Let's Quit Teaching — Station Rotations hosted read-only MCP tools."""
import logging
import os
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lqt.station_rotations")
mcp = FastMCP("LQT Station Rotations")

@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def openai_domain_verification(request: Request) -> PlainTextResponse:
    return PlainTextResponse(os.environ.get("OPENAI_DOMAIN_CHALLENGE", ""))

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def get_station_rotation_framework(grade_level: str, learning_target_or_topic: str, total_minutes: int, number_of_stations: int, include_technology: bool, technology_platform: str = "") -> dict:
    """Return the original LQT station rotation format for a freely typed grade, learning target, total time, count of stations, and optional technology. Ask missing intake fields ONE question at a time."""
    logger.info("LQT TOOL CALLED: get_station_rotation_framework")
    if not grade_level.strip():return {"error":"Ask ONE question: What is the learner's grade level? Accept unrestricted free text."}
    if not learning_target_or_topic.strip():return {"error":"Ask ONE question: What is the Learning Target or topic for the lesson?"}
    if total_minutes <= 0:return {"error":"Ask for a positive total station-rotation duration in minutes."}
    if not 1 <= number_of_stations <= 12:return {"error":"Ask how many stations are desired, using a practical positive number up to 12. Do not force a fixed menu."}
    if include_technology and not technology_platform.strip():return {"error":"Ask ONE question: What technology tool or platform would you like learners to use?"}
    return {
        "grade_level":grade_level.strip(), "learning_target_or_topic":learning_target_or_topic.strip(),"total_minutes":total_minutes,"number_of_stations":number_of_stations,
        "include_technology":include_technology,"technology_platform": technology_platform.strip() if include_technology else "Not requested",
        "intake_order":["What is the learner's grade level?","What is the Learning Target or topic for the lesson?","How much total time is available for the station rotation?","How many stations would you like?","Would you like to include a technology-based station?","If yes, what technology tool or platform would you like learners to use?"],
        "intake_rule":"Ask ONE missing question per turn in this order. Skip answers already supplied. Never use restricted grade-level choices or assume a platform. Do not design before all inputs are known. If only topic/standard supplied, provide a concise aligned learner-friendly I can target.",
        "required_overview":["Title","Grade Level","Learning Target","Total Station Time","Number of Stations","Approximate Station Time","Transition Time"],
        "required_per_station":["Station Name","Purpose","Learner Task","Evidence of Learning","Materials / Technology","Teacher Role","Learner Role","Formative Check","Possible Scaffold / Tool to Escape","Possible Extension"],
        "required_after_stations":["Rotation order/chart and explicit time breakdown including transitions","Transition cue and materials routine","Learner expectations for movement, voice and task completion","Simple method for showing where to go next","Flexible grouping recommendations based on evidence, labeled hypothetical when learner data absent","Synthesis of formative evidence, patterns to notice and instructional next moves","Only relevant implementation notes","3–5 teacher reflection questions on alignment, evidence, access versus productive struggle, support fading and next rotation design"],
        "rules":["Every station has a distinct instructional purpose and strengthens the same target; no cosmetic variants of same task.","Each station produces or elicits observable evidence. Include teacher and learner roles plus checks.","Total station time, transitions and any orientation fit strictly inside the educator's time budget; show arithmetic that adds up.","Differentiation varies access, supports and pathways, not the learning destination; preserve productive struggle.","Use Guided Information, Guided Skills and Guided Tools (G.I.S.T.) when appropriate for teacher-led work.","Technology is OPTIONAL: include only when requested; give specific learning purpose, evidence, and offline contingency.","Learner-facing station directions must match the freely typed age/grade context without lowering intended rigor.","Use 'learner'/'learners', not 'student'/'students'.","Preserve recognizably the original Station Rotation Tool Example structure and user skill."],
        "source":"User-provided Station Rotations v1.0.1 skill and Station Rotation Tool Example.docx"
    }

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def review_station_rotation(grade_level: str, learning_target: str, total_minutes: int, station_plan: str) -> dict:
    """Audit a draft station rotation for target alignment, timing, evidence, distinct functions, supports, language and original format; suggest practical repairs."""
    logger.info("LQT TOOL CALLED: review_station_rotation")
    if not grade_level.strip() or not learning_target.strip() or total_minutes <= 0 or not station_plan.strip():
        return {"error":"Provide grade (any free-text level), target, positive time budget, and the existing station plan text or attachment summary for review. Ask only for missing input."}
    return {"grade_level":grade_level,"learning_target":learning_target,"time_budget_minutes":total_minutes,
      "station_plan_to_audit":station_plan,
      "checks":["Every station directly and distinctly advances the same learning target","Required station-profile fields and lesson overview are present","Total minutes INCLUDING transitions do not exceed provided budget","Station tasks elicit specific evidence and have concrete formative checks","Teacher-led work, if present, is responsive to evidence; optional G.I.S.T. use","Grouping is flexible and framed as provisional absent learner data","Scaffolds preserve learner thinking; extensions deepen learning","Technology only if requested and with purposeful task and non-digital backup","Directions fit the given freely typed grade level and say learner not student","Flow includes rotation order, cues, movement/voice expectations and materials routines","Plan ends with evidence-based next moves and 3–5 reflection questions"],
      "output":"Provide concise evidence-based audit of strengths, missing elements and exact revisions. Do not silently claim an unprovided plan passed. Maintain original structure."}

if __name__ == "__main__":
    mcp.run(transport="http",host="0.0.0.0",port=int(os.environ.get("PORT","8000")))
