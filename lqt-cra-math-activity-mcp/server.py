"""LQT CRA Math Activity Generator: evidence-responsive CRA design helpers."""
import logging
import os
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lqt.cra_math")
mcp = FastMCP("LQT CRA Math Activity Generator")

@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def openai_domain_verification(request: Request) -> PlainTextResponse:
    return PlainTextResponse(os.environ.get("OPENAI_DOMAIN_CHALLENGE", ""))

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def get_cra_activity_framework(grade_level: str, learning_target: str, purpose: str, manipulatives: str) -> dict:
    """Return LQT's authored Concrete-Representational-Abstract activity design requirements with evidence checks, bridges, scaffolds, and teacher moves. Requires all four inputs; does not fetch standards or assess learners."""
    logger.info("LQT TOOL CALLED: get_cra_activity_framework")
    if not grade_level.strip() or not learning_target.strip() or not manipulatives.strip():
        return {"error": "Grade level, math standard or learning target, and manipulatives (or 'choose for me') are required."}
    normalized = purpose.strip().lower()
    if normalized not in {"introduce", "practice", "reteach", "extend"}:
        return {"error": "Purpose must be Introduce, Practice, Reteach, or Extend."}
    return {
        "grade_level": grade_level.strip(), "standard_or_learning_target": learning_target.strip(),
        "purpose": normalized.title(), "manipulatives": manipulatives.strip(),
        "intake": ["Ask grade level first", "Then math standard or Learning Target", "Then purpose: Introduce, Practice, Reteach, Extend", "Then manipulatives or choose for me", "Ask only one missing question per turn"],
        "learning_target_guidance": "If given a standard, make a grade-appropriate I can target without reducing rigor; do not claim to verify a standard externally.",
        "overview": ["Grade level", "Learning target", "Instructional purpose", "Manipulatives", "Flexible total time", "Conceptual mathematical idea"],
        "success_criteria": "2-4 concise learner-friendly criteria describing understanding or performance",
        "vocabulary_and_misconceptions": "Only essential vocabulary and 2-4 content-specific misconceptions",
        "concrete": {"goal": "Physical model reveals mathematical structure", "required": ["Purpose", "Materials", "Teacher Moves", "Learner Task", "2-3 progressively more complex examples", "Evidence Check", "Decision Point: advance or support further"]},
        "representational": {"goal": "Explicitly bridge drawing, diagram, array, number line, area model or other visual to prior concrete actions", "required": ["Representation", "Bridge From Concrete", "Learner Task", "2-3 connected examples", "Evidence Check", "Decision Point: ready for symbols or return to model"]},
        "abstract": {"goal": "Symbols express the same mathematics modeled concretely and visually", "required": ["Symbolic Connection", "4-6 grade-appropriate problems", "At least one justification item", "At least one error-analysis item", "At least one connection back to model", "Evidence Check", "Responsive Move if procedures are correct but reasoning is absent"]},
        "additional_sections": ["Scaffolds & Access that preserve thinking", "1-3 Extension/Transfer opportunities that deepen the same target", "Aligned formative checkpoint with answer or exemplar", "Teacher Notes: flexible pacing, moves forward/back, reteach and retained scaffold"],
        "design_principles": ["Progression is flexible, never automatic equal-time stages", "Use actual learner evidence to decide moves", "Maintain the same learning target throughout", "Concrete manipulatives must express math structure, not decoration", "Prefer common low-cost substitute only when useful", "Use learner/learners terminology", "Ask which of the concrete model, representational bridge, scaffolds or abstract reasoning to strengthen at end"],
        "source": "Original LQT CRA Math Activity Generator provided by author"
    }

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def suggest_cra_instructional_move(phase: str, evidence_observed: str, target: str, misconception_foundational: bool = False, learner_can_explain_model: bool = False) -> dict:
    """Use teacher-described, de-identified evidence to recommend a CRA teaching move, including a specific next check. Advisory only; does not access learner records or assess learner work."""
    logger.info("LQT TOOL CALLED: suggest_cra_instructional_move")
    if not target.strip() or not evidence_observed.strip():
        return {"error": "Learning target and de-identified learner evidence are required."}
    valid={"concrete", "representational", "abstract"}
    p=phase.strip().lower()
    if p not in valid:
        return {"error": "Phase must be Concrete, Representational, or Abstract."}
    if misconception_foundational:
        move="Stay with or return to a targeted concrete example and have learners explain the structure before advancing."
    elif not learner_can_explain_model:
        move="Continue or return to an aligned visual model and have learners connect its features to the manipulatives and symbols."
    elif p=="concrete":
        move="Try a learner-created representation tied explicitly to the concrete actions; check individual reasoning."
    elif p=="representational":
        move="Fade drawing support selectively and connect a symbolic expression to the representation; check individual reasoning."
    else:
        move="Maintain or extend independent symbolic reasoning, requiring an explanation of its model connection."
    return {"current_phase":p.title(), "learning_target":target.strip(), "teacher_reported_evidence":evidence_observed.strip(), "suggested_move":move,
            "next_evidence_to_collect":"Ask each learner to represent the same relationship another way and explain what each part means.",
            "limitations":"Advisory using teacher-reported descriptions; do not imply an automated evaluation of actual learners or access to identifiable records."}

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
