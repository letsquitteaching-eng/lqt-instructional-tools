"""LQT Surface, Deep & Transfer MCP. Read-only instructional framework."""
import logging
import os
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse
logging.basicConfig(level=logging.INFO)
log=logging.getLogger("lqt.surface_deep_transfer")
mcp=FastMCP("LQT Surface Deep Transfer")

@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def domain_challenge(request:Request)->PlainTextResponse:
    return PlainTextResponse(os.environ.get("OPENAI_DOMAIN_CHALLENGE", ""))

@mcp.tool(annotations={"readOnlyHint":True,"destructiveHint":False,"openWorldHint":False})
def get_surface_deep_transfer_framework(grade_level:str="",learning_target:str="",product_type:str="")->dict:
    """Return original LQT Surface/Deep/Transfer instructions. Ask grade, target, product (Activities, Questions, Both, Assessment Task) one at a time; unrestricted grade."""
    log.info("LQT TOOL CALLED: get_surface_deep_transfer_framework")
    if not grade_level.strip():return {"next_question":"What is the learner's grade level?","grade_input":"Unrestricted educator-entered free text; no forced menu."}
    if not learning_target.strip():return {"next_question":"What is the Learning Target?"}
    if not product_type.strip():return {"next_question":"What would you like me to create: Activities, Questions, Both, or an Assessment Task?"}
    mode=product_type.strip().lower().replace(" ","")
    if mode not in ("activities","questions","both","assessmenttask"):
        return {"next_question":"Would you like Activities, Questions, Both, or an Assessment Task?","accepted":["Activities","Questions","Both","Assessment Task"]}
    selection={"activities":"Activities","questions":"Questions","both":"Both","assessmenttask":"Assessment Task"}[mode]
    phase_outputs={
      "Surface":{"Activities":"2 activity options: title, setup, learner steps, time, evidence","Questions":"8–10 foundational questions","Both":"2 activity options and 6–8 foundational questions","Assessment Task":"4–6 item Surface checkpoint"},
      "Deep":{"Activities":"2 reasoned activities using comparison, connections, justification, analysis or evaluation","Questions":"8–10 reasoning questions","Both":"2 activity options and 6–8 reasoning questions","Assessment Task":"one Deep task with central prompt and 3–5 reasoning components"},
      "Transfer":{"Activities":"2 genuinely novel-context application activities of SAME learning","Questions":"8–10 novel-context scenarios/questions","Both":"2 activity options and 6–8 novel-context questions","Assessment Task":"one novel-context performance task with scenario, learner directions, product, new constraints and transfer evidence"}}
    return {"grade_level":grade_level.strip(),"learning_target":learning_target.strip(),"product_type":selection,
      "source":"Original LQT Surface Deep Transfer Learning v0.2.1 skill and example",
      "intake":"One question per turn; grade, target, product. Never repeat known answers. If given standard/topic instead, derive accurate concise I can target.",
      "global_requirements":["Use learner/learners, never student/students","Free-text grade, age-appropriate language, unchanged target rigor","Surface, Deep, Transfer are phases, not fixed labels for learners; move based on evidence","Surface builds meaningful foundation, Deep reasons about connections, Transfer applies SAME knowledge in genuinely NEW context","Don't invent resources, citations, files or calls to other tools"],
      "ordered_output":["Learning Target","Success Criteria: 3–5 learner-friendly observable criteria","Essential Knowledge & Prerequisites: up to 5","1. Surface Learning","2. Deep Learning","3. Transfer Learning","Supports & Extensions","Assessment scoring guide only for Assessment Task"],
      "phase_requirements":[
         {"phase":p,"purpose":{"Surface":"Build essential knowledge, vocabulary, concepts, procedures","Deep":"Connect and explain relationships, justify, compare, analyze, evaluate","Transfer":"Apply or adapt the learning to an unfamiliar context, representation, constraint, problem or audience"}[p],
          "selected_output":phase_outputs[p][selection],"teacher_and_evidence_fields":["Teacher Moves","Evidence to Look For","Common Misconception" if p!="Transfer" else "Likely Transfer Breakdown","Responsive Move"]+(["Ready for Deeper Learning When"] if p=="Surface" else ["Ready for Transfer When"] if p=="Deep" else [])} for p in ["Surface","Deep","Transfer"]],
      "supports_and_extensions":"3 scaffolds preserving learner thinking and 3 qualitatively deeper extensions of the SAME learning, not extra volume; show when to fade",
      "assessment_scoring":"For Assessment Task: four performance levels around foundational accuracy, reasoning, authentic transfer and communication as relevant" if selection=="Assessment Task" else "Not required",
      "closing_prompt":"Would you like me to strengthen the Surface foundation, Deep reasoning, Transfer challenge, or supports?"}

@mcp.tool(annotations={"readOnlyHint":True,"destructiveHint":False,"openWorldHint":False})
def review_surface_deep_transfer(grade_level:str="",learning_target:str="",product_type:str="",draft:str="")->dict:
    """Audit a generated Surface Deep Transfer plan for evidence-led phase progression, original format, novelty of transfer and grade suitability."""
    log.info("LQT TOOL CALLED: review_surface_deep_transfer")
    if not grade_level.strip():return {"next_question":"What is the learner's grade level?"}
    if not learning_target.strip():return {"next_question":"What is the Learning Target?"}
    if not product_type.strip():return {"next_question":"Is the product Activities, Questions, Both, or an Assessment Task?"}
    if not draft.strip():return {"next_question":"Please paste or describe the plan you would like me to review."}
    return {"grade_level":grade_level,"learning_target":learning_target,"product_type":product_type,"draft":draft,
      "review_checks":["All 3 phases align to SAME learning target","Correct counts and format for selected product mode","Learning Target, 3–5 success criteria and up to 5 prerequisites present","Surface establishes essential foundation without being defined as easy","Deep demands connections and genuine reasoning, not just more facts","Transfer introduces an actually unfamiliar context, constraint, audience, representation or problem","Each phase supplies Teacher Moves, Evidence to Look For, misconception/breakdown, Responsive Move; readiness indicators for Surface and Deep","Three targeted scaffolds and three meaningful extensions; avoid merely extra quantity","If assessment task, include concise 4-level scoring guide","Grade-appropriate learner-facing language; 'learner' instead of 'student'"],
      "instruction":"Identify observed strengths, gaps and concrete fixes; do not claim the plan passes checks without evidence; preserve original order and product mode."}

if __name__=="__main__":mcp.run(transport="http",host="0.0.0.0",port=int(os.getenv("PORT","8000")))
