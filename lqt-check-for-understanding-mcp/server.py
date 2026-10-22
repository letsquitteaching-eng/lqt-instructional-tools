"""LQT Check for Understanding: evidence-led, bounded, read-only MCP tools."""
import logging
import os
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lqt.cfu")
mcp = FastMCP("LQT Check for Understanding")
# Paste the exact case-sensitive token supplied in the OpenAI Platform dashboard here.
# Never reuse a token from another plugin. Deploy after replacing the placeholder.
OPENAI_DOMAIN_CHALLENGE = os.getenv("OPENAI_DOMAIN_CHALLENGE", "REPLACE_WITH_OPENAI_TOKEN")

@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def openai_domain_verification(request: Request) -> PlainTextResponse:
    return PlainTextResponse(OPENAI_DOMAIN_CHALLENGE)

CATEGORIES = {
    "Before": [
        {"category":"Baseline Activation","purpose":"Elicit current relevant knowledge and representations.","formats":["individual short response","mini whiteboard"],"evidence":"prior concepts and explanatory reasoning"},
        {"category":"Prediction / Anticipation","purpose":"Surface initial hypotheses and their rationales.","formats":["predict, justify, revise"],"evidence":"basis for a prediction and likely misconceptions"},
        {"category":"Readiness / Prerequisite Check","purpose":"Identify prerequisite understandings needed for the target.","formats":["brief worked example","label or sketch"],"evidence":"whether prerequisite steps and concepts are secure"},
        {"category":"Concept Connection","purpose":"Relate the target to familiar ideas.","formats":["compare examples","connection map"],"evidence":"specific similarities, differences and relationships"},
        {"category":"Misconception Probe","purpose":"Detect likely misunderstandings before instruction.","formats":["choose and justify","correct an example"],"evidence":"justification revealing the misconception"}
    ],
    "During": [
        {"category":"Recognition / Concept Check","purpose":"Check conceptual interpretation during teaching.","formats":["response cards and justification"],"evidence":"accurate identification with justification"},
        {"category":"Procedural Step Check","purpose":"Expose the reasoning behind a critical step.","formats":["complete and explain one step"],"evidence":"valid step and reason for choosing it"},
        {"category":"Misconception Probe","purpose":"Distinguish correct thinking from a common error.","formats":["diagnose a worked error"],"evidence":"accurate explanation of why the error occurs"},
        {"category":"Analytical What-If","purpose":"Reveal cause-and-effect or conditional reasoning.","formats":["predict effect of a change"],"evidence":"reasoned explanation of changing conditions"},
        {"category":"Compare & Contrast","purpose":"Distinguish related concepts, procedures or examples.","formats":["two-case comparison"],"evidence":"accurate criteria for comparison"},
        {"category":"Explain Your Reasoning","purpose":"Expose how learners reached an answer.","formats":["written justification","individual response followed by partner talk"],"evidence":"coherent reasoning tied to the target"},
        {"category":"Error Analysis","purpose":"Reveal understanding through correction of a plausible error.","formats":["critique a worked response"],"evidence":"clear diagnosis and defensible correction"}
    ],
    "After": [
        {"category":"Application / Transfer","purpose":"Determine whether learning can be applied appropriately.","formats":["new but aligned application"],"evidence":"independent application and justification"},
        {"category":"Explanation / Justification","purpose":"Elicit a consolidated explanation of the target.","formats":["individual written or oral reasoning"],"evidence":"accurate reasoning and important relationships"},
        {"category":"Error Analysis","purpose":"Test understanding of a non-obvious error.","formats":["correct a flawed example"],"evidence":"diagnosis and repaired reasoning"},
        {"category":"Peer Explanation","purpose":"Have learners explain and critique while retaining individual evidence.","formats":["individual response then peer explanation"],"evidence":"each learner's explanation or revision"},
        {"category":"Retrieval Check","purpose":"Check what learners can recall and use independently.","formats":["short closed-resource response"],"evidence":"retrieval tied to the target"},
        {"category":"Self-Assessment WITH Evidence","purpose":"Pair self-perception with actual learning evidence.","formats":["confidence plus worked example"],"evidence":"content response; confidence alone is insufficient"}
    ]
}

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def get_cfu_options(grade_level: str, learning_target: str, timing: str, limit: int = 5) -> dict:
    """Retrieve LQT's authored Check for Understanding categories for Before, During or After instruction. Returns bounded category/response/evidence guidance; ChatGPT adapts them into 3–5 explicit, grade-appropriate tasks for the learning target."""
    logger.info("LQT TOOL CALLED: get_cfu_options")
    if not grade_level.strip() or not learning_target.strip():
        return {"error":"Grade level and Learning Target are required."}
    timing_normalized = timing.strip().capitalize()
    if timing_normalized not in CATEGORIES:
        return {"error":"Timing must be Before, During, or After."}
    if not 3 <= limit <= 5:
        return {"error":"Return between three and five options."}
    return {"grade_level":grade_level.strip(),"learning_target":learning_target.strip(),"timing":timing_normalized,"categories":CATEGORIES[timing_normalized],"option_count":limit,"design_instructions":"Select 3–5 meaningfully different categories. Give concrete prompts aligned with the actual target, all-learner participation, secure/partial/misconception indicators, targeted reteach/clarify/extend responses, a content-specific probe, and an exit/next-lesson check. Use ELICIT → INTERPRET → RESPOND. Do not treat confidence alone as evidence.","sources":["LQT author-provided Check for Understanding skill","Original Check for Understanding Options Tool Example.md","CfU-2.pdf (supporting reference)"]}

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def suggest_cfu_response(learning_target: str, timing: str, evidence_observed: str, understanding_pattern: str) -> dict:
    """Suggest the next teaching response using a teacher-reported evidence pattern: widespread_misunderstanding, mixed_evidence, or secure_understanding. Does not inspect actual learner work, score attainment, or access learner records."""
    logger.info("LQT TOOL CALLED: suggest_cfu_response")
    if not learning_target.strip() or not evidence_observed.strip():
        return {"error":"Learning Target and de-identified observed evidence are required."}
    if timing.strip().capitalize() not in CATEGORIES:
        return {"error":"Timing must be Before, During, or After."}
    responses={
        "widespread_misunderstanding": {"decision":"RETEACH","next_move":"Model or explain the specific missing concept in 1–3 minutes, then elicit a fresh individual response.","check":"Use a parallel prompt requiring an explanation rather than a confidence rating."},
        "mixed_evidence": {"decision":"CLARIFY","next_move":"Use a contrastive example, targeted prompt, or brief guided correction. Sample all learners again.","check":"Ask learners to justify a choice or diagnose a closely related example."},
        "secure_understanding": {"decision":"EXTEND","next_move":"Provide a 2–4 minute application, reasoning, or transfer challenge while checking who can apply independently.","check":"Use a new situation aligned to the same learning target."}
    }
    key=understanding_pattern.strip().lower()
    if key not in responses:
        return {"error":"understanding_pattern must be widespread_misunderstanding, mixed_evidence, or secure_understanding."}
    return {"learning_target":learning_target.strip(),"timing":timing.strip().capitalize(),"teacher_reported_evidence":evidence_observed.strip(),"pattern":key,**responses[key],"caution":"Teacher-selected pattern, not independent assessment. Review learner responses and adapt; never provide identifiable learner details."}

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
