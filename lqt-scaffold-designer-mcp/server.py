"""LQT Scaffold Designer: authored scaffold categories and evidence-led fading guidance."""
import logging
import os
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lqt.scaffold")
mcp = FastMCP("LQT Scaffold Designer")

@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def openai_domain_verification(request: Request) -> PlainTextResponse:
    return PlainTextResponse(os.environ.get("OPENAI_DOMAIN_CHALLENGE", "NOT_CONFIGURED"))

SCAFFOLD_SECTIONS = [
    {"name":"Goal Setting", "minimum_examples":3, "purpose":"Learners choose controllable process goals tied to the target, not score or task completion."},
    {"name":"Deliberate Practice", "minimum_examples":3, "purpose":"Focused practice on target components, with error noticing and adjustment."},
    {"name":"Front-End Scaffolds", "minimum_examples":3, "purpose":"Prepare access before the task without pre-solving it; label Barrier addressed and Thinking preserved."},
    {"name":"Distributed Scaffolds", "subsections":{"Prompts":3,"Cues":3}, "purpose":"Help a learner continue the thinking during the task; keep prompts separate from cues."},
    {"name":"Back-End Scaffolds", "minimum_examples":3, "purpose":"After an attempt, use evidence to trigger revision or another attempt; name Barrier/evidence and Thinking preserved."},
    {"name":"Peer Scaffolding", "minimum_examples":3, "purpose":"Peers ask, question, compare, and clarify rather than supply answers."},
    {"name":"Fading Scaffolds", "minimum_examples":3, "purpose":"For each fade move name evidence of readiness, support reduced, and responsibility transferred."},
]
PRINCIPLES=[
 "Start from the learning target and worthy task.",
 "Temporary supports increase access without lowering the learning target.",
 "Preserve productive struggle and important learner thinking.",
 "Address an actual or likely barrier with the smallest useful support.",
 "Avoid turning unnecessary support into a ceiling or public label.",
 "Make supports accessible when learners are stuck and fade them as independence grows.",
]

@mcp.tool(annotations={"readOnlyHint": True,"destructiveHint": False,"openWorldHint": False})
def get_scaffold_framework(grade_level: str, learning_target: str, task_context: str = "") -> dict:
    """Retrieve LQT's exact seven-part Scaffold Designer structure and planning requirements for a grade and learning target. ChatGPT uses these requirements to compose contextualized examples; no learner records are accessed."""
    logger.info("LQT TOOL CALLED: get_scaffold_framework")
    if not grade_level.strip() or not learning_target.strip():
        return {"error":"Grade level and learning target are required. Ask for them one question at a time, grade first."}
    return {"grade_level":grade_level.strip(),"learning_target":learning_target.strip(),"task_context":task_context.strip(),
            "sections":SCAFFOLD_SECTIONS,"principles":PRINCIPLES,"intake_order":["What is the learner's grade level?","What is the learning target or skill?"],
            "output_guidance":"Produce all seven sections with >=3 grade-appropriate concrete examples each, except Distributed Scaffolds requires >=3 Prompts AND >=3 Cues. Connect to the target and authentic task. End with the four-part Scaffold Check. Use learner, never student.",
            "scaffold_check":["Does this support increase access without lowering the learning target?","Does the learner still do the important thinking?","Does it address an actual or likely barrier?","Is there a clear path toward independence?"],
            "source":"Author-supplied Scaffold Designer instructions and Scaffolding Framework reference"}

@mcp.tool(annotations={"readOnlyHint": True,"destructiveHint": False,"openWorldHint": False})
def suggest_scaffold_adjustment(learning_target: str, observed_barrier: str, learner_evidence: str, current_support: str = "", ready_for_independence: bool = False) -> dict:
    """Use teacher-described, de-identified learner evidence to suggest an appropriately small scaffold adjustment or fade plan. Advisory only; does not assess learner work or access school records."""
    logger.info("LQT TOOL CALLED: suggest_scaffold_adjustment")
    if not learning_target.strip() or not observed_barrier.strip() or not learner_evidence.strip():
        return {"error":"Learning target, observed barrier, and de-identified evidence are all required."}
    if ready_for_independence:
        move="Fade one element of support, preserve the target's thinking, and gather new independent evidence."
        phase="Fading Scaffolds"
    elif current_support.strip():
        move="Adjust only the portion of the existing scaffold that addresses the barrier; prompt another learner attempt and check reasoning."
        phase="Distributed or Back-End Scaffolds"
    else:
        move="Select the smallest temporary support that removes access confusion without supplying the solution; elicit a new attempt."
        phase="Front-End or Distributed Scaffolds"
    return {"learning_target":learning_target.strip(),"observed_barrier":observed_barrier.strip(),"learner_evidence":learner_evidence.strip(),"current_support":current_support.strip(),
            "suggested_move":move,"candidate_scaffold_category":phase,
            "required_teacher_checks":["Name which barrier the support addresses.","Specify which important thinking remains with the learner.","Collect evidence from the learner's next attempt.","State when and how support will fade."],
            "limitations":"Uses only teacher-reported evidence and cannot verify learning or access identifiable records. Teacher judgment determines use."}

if __name__ == "__main__":
    mcp.run(transport="http",host="0.0.0.0",port=int(os.environ.get("PORT","8000")))
