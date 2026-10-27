"""LQT Hexagonal Task Generator: read-only design and reasoning review."""
import logging
import os
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lqt.hexagonal_task")
mcp = FastMCP("LQT Hexagonal Task Generator")

@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def openai_domain_verification(request: Request) -> PlainTextResponse:
    return PlainTextResponse(os.environ.get("OPENAI_DOMAIN_CHALLENGE", ""))

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def get_hexagonal_task_framework(grade_level: str, learning_target: str, hexagon_count: int = 24, content_mode: str = "Mixture of All Three", include_wildcards: bool = True) -> dict:
    """Return the authored LQT hexagonal-task design framework for any educator-typed grade level, learning target and selected deck. Never restrict grade choices or invent a completed printable file."""
    logger.info("LQT TOOL CALLED: get_hexagonal_task_framework")
    if not grade_level.strip() or not learning_target.strip():
        return {"error": "Typed grade level/learning setting and learning target are required."}
    if not 12 <= hexagon_count <= 36:
        return {"error": "The original LQT design supports 12 to 36 hexagons, inclusive."}
    modes = ["Single Words", "Phrases", "Visuals", "Mixture of All Three"]
    if content_mode not in modes:
        return {"error": "Content mode must be one of: " + ", ".join(modes)}
    return {
        "grade_level": grade_level.strip(), "learning_target": learning_target.strip(),
        "hexagon_count": hexagon_count, "content_mode": content_mode,
        "wildcard_count": 3 if include_wildcards else 0,
        "non_wildcard_count": hexagon_count - (3 if include_wildcards else 0),
        "intake": ["What grade level or learning setting are you designing for? Please type your answer.",
                   "What is the Learning Target or topic?",
                   "How many hexagons would you like? You can choose 12–36. The default is 24.",
                   "What would you like on the hexagons: Single Words, Phrases, Visuals, or a Mixture of All Three?"],
        "grade_policy": "Free-text entry for any grade or learning setting, including Pre-K, K-12, higher education, adult and mixed-age learning. No dropdown, grade bands, preset options or grade limitations. Adapt complexity to learner age and target without lowering rigor.",
        "intake_policy": "Ask only the next unanswered question. If multiple answers are supplied together, retain them. Do not generate until all four inputs are known; default of 24 is used only when educator accepts it.",
        "design": [
            "Exactly requested count including three wildcards unless declined",
            "Meaningful cross-connections and multiple defensible arrangements; not one answer key",
            "Words, appropriately sized phrases, actual visuals or intentional mix as requested",
            "At-a-glance setup, numbered exact deck, printable cut-apart separate outlined hexagons",
            "Learner directions (5-8), success criteria (3-5), full teacher guide",
            "Discussion stems (5-8), scaffolds, extensions within same cognitive demand",
            "Single-point assessment columns WHAT I GOT | WHAT SUCCESS LOOKS LIKE | WHAT I NEED, 3-4 rows",
            "6-10 possible explained connections, 2-3 misconceptions and coaching prompts"
        ],
        "printable_guidance": "If the ChatGPT environment has file-creation tools, create and inspect a real PDF or other printable document: each item on its own outlined hexagon, ample cut spacing, centered untruncated text, exact count, genuine visuals for visual tiles. The MCP tool itself does not generate a PDF. Never claim that a printable file exists unless it was created.",
        "source": "LQT Hexagonal Task Generator author-provided instructional skill"
    }

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def review_hexagonal_deck(grade_level: str, learning_target: str, tiles: list[str], requested_count: int, include_wildcards: bool = True) -> dict:
    """Review teacher-supplied hexagon tile labels for count and wildcard consistency and supply a reasoning-focused manual-review checklist. Does not assert content accuracy or assess learner work."""
    logger.info("LQT TOOL CALLED: review_hexagonal_deck")
    if not grade_level.strip() or not learning_target.strip():
        return {"error": "Grade/learning setting and learning target are required."}
    if not 12 <= requested_count <= 36:
        return {"error": "Requested count must be between 12 and 36."}
    if not isinstance(tiles, list) or any(not isinstance(s, str) for s in tiles):
        return {"error": "Tiles must be a list of tile labels."}
    wildcard_indices = [i+1 for i,s in enumerate(tiles) if 'wildcard' in s.casefold()]
    return {
        "grade_level": grade_level.strip(), "learning_target": learning_target.strip(),
        "requested_count": requested_count, "actual_count": len(tiles),
        "exact_count_met": len(tiles) == requested_count,
        "wildcard_indices_by_label": wildcard_indices,
        "expected_wildcard_count": 3 if include_wildcards else 0,
        "wildcard_label_count_met": len(wildcard_indices) == (3 if include_wildcards else 0),
        "duplicate_labels": sorted({t for t in tiles if t.strip() and tiles.count(t)>1}),
        "professional_review": [
            "Are all ideas scientifically/historically/mathematically accurate and aligned with the target?",
            "Do tiles create substantive, non-obvious, defensible connections?",
            "Does language/representation match the entered grade or learning setting?",
            "Are there 6-10 candidate links with explanations, not a fixed answer key?",
            "Are wildcards meaningful opportunities for learner-created ideas?",
            "If visuals are requested, does each printed tile contain a real visual rather than a placeholder?",
            "Does the printable deck contain exactly one separately outlined, legible hexagon per listed tile?"
        ],
        "limitations": "Mechanical checks only; semantic accuracy, legibility of a generated PDF, age alignment and intellectual quality need educator inspection."
    }

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
