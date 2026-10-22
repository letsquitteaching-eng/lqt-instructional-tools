"""LQT GMAS ICT Creator: grade-routed Georgia Milestones practice guidance."""
import logging
import os
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lqt.gmas_ict")
mcp = FastMCP("LQT GMAS ICT Creator")
VALID_GRADES = {3, 4, 5, 6, 7, 8, 10}

@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def openai_domain_verification(request: Request) -> PlainTextResponse:
    return PlainTextResponse(os.environ.get("OPENAI_DOMAIN_CHALLENGE", ""))

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def get_gmas_ict_framework(grade_level: int, topic: str, supplemental_extended_writing: bool = False) -> dict:
    """Retrieve author-defined grade-specific Georgia Milestones Interpreting & Constructing Texts practice structure. Designed as original practice, not official GMAS items. Accept grade 3,4,5,6,7,8,10 and a teacher-selected topic."""
    logger.info("LQT TOOL CALLED: get_gmas_ict_framework")
    if grade_level not in VALID_GRADES:
        return {"error": "Supported grades: 3, 4, 5, 6, 7, 8, 10."}
    if not topic or not topic.strip():
        return {"error": "A topic is required after grade selection."}
    peer_revision = grade_level in (4, 6, 7) and not supplemental_extended_writing
    genre = "opinion" if grade_level in (3, 4, 5) else "argument"
    source_count = "2–3" if grade_level == 3 else "3–4" if grade_level in (5, 8, 10) else "grade-appropriate set; no fixed count"
    general = {
        "grade_level": grade_level, "topic": topic.strip(),
        "workflow": "assessment-style peer revision" if peer_revision else "supplemental extended writing practice" if supplemental_extended_writing and grade_level in (4, 6, 7) else "extended writing ICT",
        "genre": genre,
        "intake": ["Which grade level: 3, 4, 5, 6, 7, 8, or 10?", "What topic would you like the ICT task to explore?"],
        "common_design": [
            "Present one continuous classroom-ready learner product with clear headings, without code blocks.",
            "Create an authentic research-and-analysis scenario and credible, clearly labeled sources.",
            "Use grade-appropriate complexity, source load, analysis demand and language.",
            "Choose meaningful multimodal source format for the task; do not lock particular media to a grade.",
            "Write original source passages. Do not invent real media titles, URLs, runtimes, quotes, transcripts, QR codes or facts.",
            "If verified external media is unavailable, use an explicitly labeled original self-contained multimodal representation.",
            "Make all source-dependent questions answerable using provided sources.",
            "Do not present generated tasks as official Georgia Milestones items.",
            "No answer key, model response, rubric, teacher commentary or extensions unless requested.",
            "Use original attached Georgia guidance documents as the authority for assessment expectations; Grade 3 example is not a universal template."
        ],
        "final_question": "Would you like to revise the topic, source set, or grade-level complexity?",
        "source": "LQT GMAS ICT Creator original instructional skill"
    }
    if peer_revision:
        general["requirements"] = [
            "Include a scenario, grade-appropriate source set and source-based Interpreting Texts items.",
            "Provide a credible constructed-text draft from a learner at the selected grade; revise it instead of writing an entirely new response.",
            "Make the draft genuinely grade-appropriate with strengths and a few authentic, not exaggerated, revision opportunities.",
            "Write selected-response and technology-enhanced-style peer revision items totaling exactly 8 points, not necessarily a fixed number of questions.",
            "Align revision to Purpose and Organization, Evidence and Elaboration, and Language Usage and Conventions.",
            "Allow some original wording to be effective, or proposed revisions to be worse; require evaluative judgment and preserve learner voice.",
            "Grade 4: clear opinion, grouping, supported reasons and attempted conclusion with credible elementary vocabulary.",
            "Grade 6: credible middle-school claim, source evidence, developing reasoning, transitions, and attempted counterclaim.",
            "Grade 7: stronger cohesion, integrated evidence, tone, nuanced counterclaim and more sophisticated reasoning than Grade 6."
        ]
        general["revision_points"] = 8
    else:
        general["source_count_guidance"] = source_count
        general["requirements"] = [
            "Include three source-based Interpreting Texts questions before writing, mixing selected-response and technology-enhanced-style types.",
            "State Research Question, Purpose, Audience and directions to use source evidence.",
            f"Use {genre} genre with grade-appropriate development and cited source evidence.",
            "Provide a grade-and-genre-specific first-person Writer's Checklist around Purpose and Organization, Evidence and Elaboration, and Language Usage and Conventions.",
            "Grades 4, 6 and 7: label extended writing as supplemental practice when specifically requested, not end-of-year Section 1 format.",
            "Grade 3: accessible vocabulary, concrete context and manageable paragraph/developed short response.",
            "Grade 5: independent comparison, elaboration, reasons and evidence.",
            "Grade 8: claim, multi-source reasoning, organization and counterclaim.",
            "Grade 10: nuanced synthesis, attribution and more sophisticated counterclaim reasoning."
        ]
    return general

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def review_gmas_ict_design(grade_level: int, workflow: str, topic: str, revision_points: int = 0, has_original_sources: bool = True, has_grade_authentic_draft: bool = False, contains_unverified_external_media: bool = False) -> dict:
    """Return transparent checks for a teacher-provided ICT practice draft. Only reviews supplied design flags, not actual essay content or official Georgia alignment."""
    logger.info("LQT TOOL CALLED: review_gmas_ict_design")
    if grade_level not in VALID_GRADES:
        return {"error": "Supported grades: 3, 4, 5, 6, 7, 8, 10."}
    if not topic.strip():
        return {"error": "A topic is required."}
    peer = grade_level in (4,6,7)
    workflow_lower = workflow.strip().lower()
    selected_peer = "peer" in workflow_lower
    notes = []
    if peer and not selected_peer and "supplemental" not in workflow_lower:
        notes.append("Grades 4,6,7 default to assessment-style peer revision; extended writing must be explicitly labeled supplemental.")
    if not peer and selected_peer:
        notes.append("Grades 3,5,8,10 follow extended-writing ICT practice.")
    if selected_peer and revision_points != 8:
        notes.append("Peer revision items must total exactly 8 points.")
    if selected_peer and not has_grade_authentic_draft:
        notes.append("Peer revision requires a credible grade-level learner draft with real strengths and purposeful revision opportunities.")
    if not has_original_sources:
        notes.append("Use source material with permissions or original self-contained text, not unattributed copied passages.")
    if contains_unverified_external_media:
        notes.append("Remove or verify external media details; do not invent titles, links, runtimes or content.")
    return {"grade_level": grade_level, "topic": topic.strip(), "reported_workflow": workflow,
        "flagged_checks": notes, "always_review": [
          "Questions must be answerable with supplied source materials.",
          "Grade-level complexity, genre and draft authenticity require educator judgment.",
          "Multimodal resources may vary by topic, not fixed by grade.",
          "No official GMAS endorsement or item status should be implied.",
          "No model answer or answer key unless requested."
        ], "limitations": "This check applies stated flags only; it does not inspect actual source text or verify official standards."}

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
