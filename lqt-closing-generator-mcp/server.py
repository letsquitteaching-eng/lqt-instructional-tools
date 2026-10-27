"""LQT Closing Generator: read-only instructional MCP tools."""
import logging
import os
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger("lqt.closing_generator")
mcp=FastMCP("LQT Closing Generator")

@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def openai_domain_verification(request: Request) -> PlainTextResponse:
    return PlainTextResponse(os.environ.get("OPENAI_DOMAIN_CHALLENGE", ""))

@mcp.tool(annotations={"readOnlyHint":True,"destructiveHint":False,"openWorldHint":False})
def get_closing_strategies(grade_level: str, learning_target_or_topic: str, lesson_minutes: int = 0, previously_suggested_strategies: str = "") -> dict:
    """Return the original LQT framework for five purposeful lesson closings; grade and target are unrestricted free text, and optional time informs feasible closings. Ask for grade and target ONE QUESTION AT A TIME. When asked for more, pass previously suggested names to avoid duplicates."""
    logger.info("LQT TOOL CALLED: get_closing_strategies")
    if not grade_level.strip():return {"next_question":"What is the learner's grade level?","rule":"Accept any grade or learning setting as free text; no fixed grade list."}
    if not learning_target_or_topic.strip():return {"next_question":"What is the learning target for the lesson? If you don't have one, provide the topic or standard."}
    return {"grade_level":grade_level.strip(),"learning_target_or_topic":learning_target_or_topic.strip(),"lesson_minutes":lesson_minutes if lesson_minutes>0 else "Not specified; do not require this input", "previously_suggested_strategies":previously_suggested_strategies,
      "intake":["Ask grade first, one question only","Ask learning target second; accept topic or standard and derive an appropriate I can target","Do not require time, content platform or other intake details"],
      "primary_sources":["Bundled original Closing Strategies.pdf (primary strategy bank)","Bundled Additional Closing Framework.md (author's broader repertoire)","Original Closing Generator v1.0.3 skill"],
      "three_purposes":["Give learners an opportunity to summarize the learning and clarity","Praise pitfalls and progress by reflecting on the learning process","Provide formative evidence teachers can use to inform next steps"],
      "required_output":{"count":5,"for_each":["Closing Strategy — established strategy name in references","How It Works — concrete, grade-appropriate learner directions and example prompts","Evidence of Learning — what learner response reveals about target","How to Use the Evidence — actionable instructional next move"],"follow_up":"Would you like more suggestions? If yes, provide five NEW meaningfully different referenced strategies."},
      "rules":["Use Closing Strategies.pdf as PRIMARY repertoire; draw from Additional Closing Framework when better aligned (for example Necessary Nine, Drawing the Journey, Thought/Sought/Ought).","Do not invent a named closing format if a suitable established approach is in the references.","Select five meaningfully distinct strategies; avoid five variants of exit tickets, 3-2-1 or generic summaries.","Keep established strategy's structure recognizable while varying prompt, grouping, complexity, number of items and timing.","If duration provided, a closing takes roughly 15 percent of total lesson time; otherwise make closings brief and feasible.","For each, show target-aligned evidence, rather than asking only what learners liked or did.","Learner-facing wording fits ANY educator-typed grade or adult learning setting without watering down cognitive rigor.","Use learner/learners, not student/students.","If given a topic/standard, derive a concise grade-appropriate I can learning target first.","On more suggestions, exclude previously named strategies and show five genuinely different options."],
      "source":"Original user-supplied Closing Generator v1.0.3 package and its reference materials"}

@mcp.tool(annotations={"readOnlyHint":True,"destructiveHint":False,"openWorldHint":False})
def develop_closing_strategy(grade_level: str, learning_target: str, strategy_name: str, lesson_minutes: int = 0, instructional_context: str = "") -> dict:
    """Develop one user-selected established closing strategy as a complete ready-to-teach activity, aligned to learner evidence, without inventing unverified references."""
    logger.info("LQT TOOL CALLED: develop_closing_strategy")
    if not grade_level.strip():return {"next_question":"What is the learner's grade level?"}
    if not learning_target.strip():return {"next_question":"What is the learning target for the lesson?"}
    if not strategy_name.strip():return {"next_question":"Which of the suggested closing strategies would you like developed?"}
    return {"grade_level":grade_level.strip(),"learning_target":learning_target.strip(),"strategy_name":strategy_name.strip(),"lesson_minutes":lesson_minutes if lesson_minutes>0 else "Use a brief feasible closing", "instructional_context":instructional_context,
    "required_output":["Purpose and direct alignment to learning target and one or more of 3 LQT closing purposes","Estimated minutes, materials, preparation","Exact teacher facilitation steps and prompts","Ready-to-use learner-facing directions tailored to specified grade","Example learner response or exemplar where appropriate","Specific observable formative evidence and likely misconceptions","What teacher should do next in response to different evidence","Accessibility supports that keep learner thinking intact"],
    "rules":["Preserve the established strategy's recognizable structure and source title","Don't falsely quote or attribute an invented named strategy","Use learner rather than student","Roughly 15 percent of lesson time when provided","Don't substitute a generic opinion-based exit question for evidence of target attainment"]}

if __name__=="__main__":
    mcp.run(transport="http",host="0.0.0.0",port=int(os.environ.get("PORT","8000")))
