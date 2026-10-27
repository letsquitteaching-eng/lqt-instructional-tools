"""LQT Standards Analyzer — read-only hosted MCP."""
import logging
import os
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lqt.standards_analyzer")
mcp = FastMCP("LQT Standards Analyzer")

@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def openai_domain_verification(request: Request) -> PlainTextResponse:
    return PlainTextResponse(os.environ.get("OPENAI_DOMAIN_CHALLENGE", ""))

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def get_standards_analysis_framework(grade_level: str = "", standard_text: str = "") -> dict:
    """Retrieve the five-section LQT Standards Analyzer framework. Ask grade first and the standard exactly as written second, one question per turn. Accept any freely typed grade level; don't invent unprovided standard wording."""
    logger.info("LQT TOOL CALLED: get_standards_analysis_framework")
    if not grade_level.strip():
        return {"next_question": "What is the learner's grade level?", "rule": "Accept any grade description as free text, including Pre-K, adult, or mixed grades; do not offer restricted grade lists."}
    if not standard_text.strip():
        return {"next_question": "Please provide the standard exactly as written.", "grade_level": grade_level.strip()}
    return {
        "grade_level": grade_level.strip(), "standard_as_provided": standard_text.strip(),
        "scope": "Analyze the supplied standard as written, NOT a lesson plan, assessment, task, rubric or success criteria unless explicitly requested afterward.",
        "format": "Respond using exactly five numbered sections in this order, with substantive, standards-grounded reasoning.",
        "sections": [
            {"heading": "1. Mastery Expectations", "requirements": "Explain what learners at the input grade should know, understand, and be able to do. Unpack all relevant verbs, concepts, conditions and depth of thinking. Separate components when the standard is compound; do not add unsupported requirements."},
            {"heading": "2. Evidence of Learning", "requirements": "Describe concrete things learners could say, write, create, show, solve, analyze, explain, justify or demonstrate to reveal genuine understanding, not just completion. Link each type of evidence to the standard's thinking."},
            {"heading": "3. Instructional Strategies", "requirements": "Provide practical grade-appropriate instructional approaches directly matched to the actual demands and cognitive level of the provided standard. Do not automatically produce a full lesson plan."},
            {"heading": "4. Prior Knowledge and Fundamentals", "requirements": "Identify genuinely necessary prior skills, concepts, vocabulary and understandings; distinguish prerequisites from merely helpful background when possible."},
            {"heading": "5. Daily Learning Targets", "requirements": "Provide no more than FIVE clear, focused, distinct 'I can' targets that jointly cover the standard's full intent and logically progress as required; each should express learning, not tasks/assignments, at the learner's entered grade level, without sacrificing rigor."}
        ],
        "rules": ["Ask ONE missing intake question at a time; never ask again for supplied information.", "Grade is unrestricted educator free text; adapt learner-facing target language, vocabulary and sentence structure to it.", "Keep state standard wording faithful. Do not identify a state or jurisdiction unless supplied. Do not invent standards, codes or learning requirements.", "If standard wording appears partial, analyze only supplied text and label any material uncertainty; don't silently expand it.", "Use 'learner' not 'student' in generic references.", "Only analyze the standard unless further work is explicitly requested."],
        "source": "Original uploaded Standards Analyzer v1.0.1 SKILL.md"
    }

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def review_standards_analysis(grade_level: str = "", standard_text: str = "", analysis_text: str = "") -> dict:
    """Review an existing Standards Analyzer output for fidelity, exact five-section order, grade-appropriate targets, full standards coverage, and absence of added demands."""
    logger.info("LQT TOOL CALLED: review_standards_analysis")
    if not grade_level.strip(): return {"next_question": "What is the learner's grade level?"}
    if not standard_text.strip(): return {"next_question": "Please provide the standard exactly as written."}
    if not analysis_text.strip(): return {"next_question": "Please paste or describe the standards analysis you want reviewed."}
    return {"grade_level": grade_level.strip(), "standard_as_provided": standard_text.strip(), "analysis_to_review": analysis_text.strip(),
        "checks": ["All standard verbs, concepts, conditions and intended rigor are addressed without added unsupported requirements", "Exactly five sections: Mastery Expectations; Evidence of Learning; Instructional Strategies; Prior Knowledge and Fundamentals; Daily Learning Targets", "Evidence reveals understanding beyond task completion", "Strategies align with demands and grade", "True prerequisites are distinguishable from optional helpful knowledge", "No more than five focused learner-friendly I can targets", "Learning targets collectively cover the full standard and preserve its cognitive level", "Unrestricted grade adaptation and learner terminology", "No unsolicited full lesson plan/rubric/worksheet"],
        "instruction": "Provide a concise evidence-based audit listing accurate strengths, specific omissions or scope drift, and corrected sections/targets as needed. Do not invent requirements or claim accuracy without support."}

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
