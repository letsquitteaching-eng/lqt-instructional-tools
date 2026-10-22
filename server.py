"""LQT Opener Generator MCP server: curated strategy lookup and alignment checks."""
import json
import logging
import os
import re
from pathlib import Path
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lqt.opener")

mcp = FastMCP("LQT Opener Generator")

# Public domain ownership proof requested by OpenAI Platform.
# The response is plain text at the domain-root well-known path.
OPENAI_DOMAIN_CHALLENGE = "gcSiPxaVQj06v3wGGA5DBuVTIPjeKnvoRMAy3GqCX80"

@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def openai_domain_verification(request: Request) -> PlainTextResponse:
    return PlainTextResponse(OPENAI_DOMAIN_CHALLENGE)

STRATEGIES = json.loads((Path(__file__).parent / "strategies.json").read_text(encoding="utf-8"))
PURPOSES = {"prior knowledge", "curiosity", "collaboration", "prerequisite", "vocabulary", "misconceptions"}

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def find_opening_strategies(learning_target: str, grade_level: str, purpose: str = "prior knowledge", exclude_names: list[str] | None = None, limit: int = 12) -> dict:
    """Search LQT's author-curated opening strategies by instructional purpose. Inputs: grade, learning target and optional purpose. Returns original strategy names and descriptions, not invented activities. Use results to write five adapted classroom-ready opener options."""
    logger.info("LQT TOOL CALLED: find_opening_strategies")
    if not learning_target.strip() or not grade_level.strip():
        return {"error": "Grade level and learning target are required before choosing strategies."}
    requested = {x.strip().lower() for x in re.split(r"[,;/]", purpose) if x.strip()}
    allowed = requested & PURPOSES
    excluded = {x.casefold().strip() for x in (exclude_names or [])}
    available = [s for s in STRATEGIES if s["name"].casefold() not in excluded]
    scored = sorted(available, key=lambda s: (-len(set(s["tags"]) & allowed),s["name"].lower()))
    limit = max(1,min(int(limit),25))
    return {"grade_level":grade_level.strip(),"learning_target":learning_target.strip(),"purpose":purpose,"available_purposes":sorted(PURPOSES),"strategies":scored[:limit],"source":"LQT Opening Strategies-2.pdf (original names and condensed descriptions)","guidance":"Choose five meaningfully different formats. Adapt their prompts to the actual target and grade; do not treat relevance scores as a validation of content alignment. Opening duration about 10% of lesson."}

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def check_opener_alignment(learning_target: str, opener_description: str, lesson_minutes: int = 50, opener_minutes: int = 5, activates_prior_knowledge: bool = False, ignites_curiosity: bool = False, includes_collaboration: bool = False, explicitly_links_to_target: bool = False, previews_prerequisites: bool = False, evidence_to_notice: str = "") -> dict:
    """Apply the author's Opening framework as a transparent checklist to a draft opener. Boolean inputs are teacher-verified, not automatically inferred; output flags missing evidence and duration concerns, without claiming to assess actual learner impact."""
    logger.info("LQT TOOL CALLED: check_opener_alignment")
    if not learning_target.strip() or not opener_description.strip():
        return {"error":"Learning target and draft opener are required."}
    if lesson_minutes <= 0 or opener_minutes <= 0:
        return {"error":"Durations must be positive."}
    ratio = round(100*opener_minutes/lesson_minutes,1)
    checks={"activates_prior_knowledge":activates_prior_knowledge,"ignites_curiosity":ignites_curiosity,"includes_collaboration_when_useful":includes_collaboration,"explicitly_links_to_target":explicitly_links_to_target,"previews_prerequisite_when_needed":previews_prerequisites,"teacher_identified_evidence":bool(evidence_to_notice.strip())}
    suggestions=[]
    if not explicitly_links_to_target: suggestions.append("State how the opening connects to the learning target.")
    if not (activates_prior_knowledge or ignites_curiosity or previews_prerequisites): suggestions.append("Choose a specific learning purpose: prior knowledge, curiosity, or prerequisites.")
    if not evidence_to_notice.strip(): suggestions.append("Identify what learner responses will help the teacher decide what to do next.")
    if ratio>15: suggestions.append("Opening is longer than the approximate 10% guideline; consider shortening it.")
    return {"checks":checks,"opening_percent_of_lesson":ratio,"time_guideline":"approximately 10% of the lesson, not a rigid limit","recommendations":suggestions,"interpretation":"Checklist reflects user-reported attributes; this is not a validated quality score or a claim that learning occurred."}

if __name__ == "__main__":
    port=int(os.environ.get("PORT","8000"))
    mcp.run(transport="http",host="0.0.0.0",port=port)
