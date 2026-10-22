"""LQT Write into Learning: read-only instructional writing design support."""
import os
import logging
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger("lqt.write_into_learning")
mcp=FastMCP("LQT Write into Learning")

@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def verify_openai_domain(request: Request) -> PlainTextResponse:
    return PlainTextResponse(os.environ.get("OPENAI_DOMAIN_CHALLENGE", ""))

REFERENCE_STRATEGIES={
    "Quick and Low-Stakes": ["Quick Writes", "Entrance/Exit Tickets", "The Daily Dash", "One-Minute Paper", "Freewrites", "Power Writing", "Quick Write Prompts", "Rambling Autobiography", "Low-Stakes Writing"],
    "Reflective and Metacognitive": ["Learning Logs/Journals", "Self-Assessments", "Letter to a Future Self", "Sketchnoting", "Writing Conferences", "Portfolio Reflections"],
    "Collaborative and Interactive": ["Think-Pair-Share-Write", "Anonymous Reading Questions", "Shared Writing", "WWYW? (What Would You Write?)", "Peer Review and Revision", "Writing Buddies", "Group Storytelling", "Scramble Sentences"],
    "Subject-Specific and Real-World": ['The "How-To" Guide', "Character Studies", "Test Question Design", "RAFT (Role, Audience, Format, Topic)", "Exemplar Texts Imitation", "Retelling Stories or Concepts", "Author's Purpose Analysis"],
    "Prewriting and Planning": ["Brainstorming", "Clustering/Mind Mapping", "Graphic Organizers", "Four-Square Method", "Paragraph Burger", "Character Development Charts", "Daily Writing Prompts"],
    "Revision and Editing": ["Practice Revision Techniques", "Mnemonics for Editing", "Mentor Texts Analysis", "SEEDS Folder System"],
    "Overall Writing Process": ["The Writing Process", "Genre-Specific Instruction", "Reading-Writing Connection"]
}

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def get_writing_opportunities_framework(grade_level: str, content_area: str, learning_target: str, resource_context: str = "none") -> dict:
    """Retrieve author-provided Write into Learning guidance and named reference strategies for designing three distinct learning-target-aligned writing activities. Do not invent source details."""
    logger.info("LQT TOOL CALLED: get_writing_opportunities_framework")
    if not all([grade_level.strip(), content_area.strip(), learning_target.strip()]):
        return {"error": "Grade level, content area, and learning target are required."}
    return {
        "grade_level":grade_level.strip(),"content_area":content_area.strip(),"learning_target":learning_target.strip(),"resource_context":resource_context.strip() or "none",
        "intake_order":["What is the learner's grade level?", "What is the content area?", "What is the Learning Target?", "Is there any text, image, lab, article, data set, notes, problem type, video, graphic, scenario, or other resource you want learners to use? You can also say 'none'."],
        "activity_count":3,
        "distinctness_rule":"Three genuinely different options in purpose, structure, cognitive demand, lesson placement, audience, or evidence. Do not merely write three paragraphs.",
        "strategy_reference":"Writing Strategies.pdf (original author-supplied PDF). Only use a named reference strategy when it appears in reference_strategies; for other tasks choose an accurately labeled functional writing move without attributing it to the reference.",
        "reference_strategies":REFERENCE_STRATEGIES,
        "each_activity_fields":["Engaging title","Writing Strategy","When to Use (Opener, Mid-Lesson, Practice or Closing; approximate time)","Why This Fits","Exact Learner Prompt","Steps for Learners (3–5)","Scaffolds (2–4)","Extension / Transfer","Evidence of Learning","Quick Success Criteria (2–4)"],
        "required_sections":["Teacher Snapshot", "Three Writing Activity Choices", "Pick the Best Fit (specific reasons for each)", "Use the Writing as Evidence (foundational gap, partial understanding, secure understanding)"],
        "design_rules":["Writing is a tool for learning, not a generic add-on", "Preserve content-area cognitive demand", "Ground claims in source actually supplied", "Adjust writing length and writing access supports without doing content reasoning for learners", "Do not overemphasize mechanics unless in target", "Use learner, never student"],
        "follow_up":"Would you like me to strengthen one of the writing options, scaffolds, success criteria, or evidence checks?",
        "limitations":"Instructional guidance based on teacher-provided information; does not access private resources or verify external standards."
    }

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def suggest_writing_evidence_response(learning_target: str, evidence_observed: str, evidence_level: str) -> dict:
    """Apply the original writing-as-evidence response routine to de-identified teacher observations. Advisory only, not a learner assessment."""
    logger.info("LQT TOOL CALLED: suggest_writing_evidence_response")
    if not learning_target.strip() or not evidence_observed.strip():
        return {"error":"Learning target and de-identified observed writing evidence are required."}
    level=evidence_level.strip().lower()
    moves={
        "foundational gap":"Model one essential content idea or representation, use a short supported writing prompt, then elicit fresh individual evidence.",
        "partial understanding":"Give targeted feedback or a guiding question that presses the missing reasoning, then ask learners to revise a specific claim or explanation.",
        "secure understanding":"Increase independence or ask for justified transfer to a related context, without merely adding writing volume."
    }
    if level not in moves:
        return {"error":"evidence_level must be one of: foundational gap, partial understanding, secure understanding."}
    return {"learning_target":learning_target.strip(),"evidence_observed":evidence_observed.strip(),"evidence_level":level,"suggested_instructional_move":moves[level],"next_evidence_to_collect":"Collect a brief, independent written or annotated explanation that reveals reasoning aligned to the learning target.","limitations":"Based solely on teacher descriptions; do not infer unreported learner facts or use identifiable learner records."}

if __name__=="__main__":
    mcp.run(transport="http",host="0.0.0.0",port=int(os.environ.get("PORT","8000")))
