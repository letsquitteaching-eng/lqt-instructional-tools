"""LQT integrated lesson design MCP: read-only framework and review tools."""
import logging,os,re
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse
logging.basicConfig(level=logging.INFO)
log=logging.getLogger("lqt.lesson_designer")
mcp=FastMCP("LQT Lesson Designer")
@mcp.custom_route("/.well-known/openai-apps-challenge",methods=["GET"])
async def challenge(request:Request)->PlainTextResponse:
 return PlainTextResponse(os.environ.get("OPENAI_DOMAIN_CHALLENGE",""))

@mcp.tool(annotations={"readOnlyHint":True,"destructiveHint":False,"openWorldHint":False})
def generate_lesson_learning_targets(grade_level:str,state_standard:str)->dict:
 """After asking grade and whether educator already has a target, break an EXACT supplied state standard into numbered focused daily learning targets following LQT Learning Target Generator. Ask user to choose; never auto-select."""
 log.info("LQT TOOL CALLED: generate_lesson_learning_targets")
 if not grade_level.strip():return {"next_question":"What is the learner's grade level?"}
 if not state_standard.strip():return {"next_question":"Please paste the state standard exactly as written (including its code, if available)."}
 return {"grade":grade_level.strip(),"submitted_standard":state_standard.strip(),"procedure":["Identify essential verbs, nouns and intended conceptual rigor from the exact provided standard.","Identify what learners need to KNOW and DO.","Derive a SMALL, sufficient set of coherent one-class-period targets fully addressing standard without adding unsupported requirements.","Write numbered learner-friendly I can statements at entered grade and show for each Know, Do, Connection to Standard.","Invite educator to refine the options if too broad or narrow; do not select a target automatically."],"next_question":"Which numbered learning target would you like to use for this lesson?","do_not_proceed_to_duration_until_selection":True,"source":"LQT Learning Target Generator original uploaded skill"}

@mcp.tool(annotations={"readOnlyHint":True,"destructiveHint":False,"openWorldHint":False})
def get_integrated_lesson_framework(grade_level:str,learning_target:str,class_minutes:int,state_standard:str="")->dict:
 """Produce exact LQT integrated ready-to-teach lesson framework only AFTER user selected/provided learning target, grade and class duration. Preserve named references and criteria format."""
 log.info("LQT TOOL CALLED: get_integrated_lesson_framework")
 if not grade_level.strip():return {"next_question":"What is the learner's grade level?"}
 if not learning_target.strip():return {"next_question":"Do you already have a learning target for this lesson? If yes, please enter it. If no, paste the exact state standard and choose from the generated targets."}
 if class_minutes<=0:return {"next_question":"How long is your class period in minutes?"}
 percentages=[.10,.25,.50,.15];allocated=[int(class_minutes*p) for p in percentages];allocated[2]+=class_minutes-sum(allocated)
 return {"grade":grade_level.strip(),"selected_learning_target":learning_target.strip(),"provided_standard":state_standard.strip() or None,"class_minutes":class_minutes,"minutes":{"Opening":allocated[0],"Mini-Lesson / G.I.S.T.":allocated[1],"Work Session":allocated[2],"Closing":allocated[3]},"framework_sequence":["Learning Target","Opening — actual named strategy from provided Opening Strategies reference; align prompts, teacher/learner directions, evidence","Mini-Lesson / Instruction — Guided Information, Guided Skills, Guided Tools, formative check, model","Work Session — one authentic LQT engaging task with learner prompt, product, at least four demonstrated engagement qualities, feedback, barrier-aware scaffolds/tools to escape and fade, extension","Progressive Success Criteria — precisely two rows x four columns, 4 Exceeds, 3 Meets, 2 Approaching, 1 Beginning, each level's exact I CAN statement plus 2–3 observable bullets tied to THIS task, teacher/learner self-assessment","Closing — actual named strategy from bundled Closing Strategies reference; elicited evidence and concrete instructional response"],"criteria_headers":["4 — Exceeds","3 — Meets","2 — Approaching","1 — Beginning"],"criteria_stems":["I CAN ... AND I ...","I CAN ...","I CAN ... BUT I ...","NO, I CANNOT ... YET."],"constraints":["Use source reference strategies not generic invented titles","Every part aligns to same target and work-session product","Keep learner-facing instructions appropriate to freely typed grade level and preserve rigor","At least four actual engagement qualities are operationalized; no worksheet as main work","Scaffolds provide minimal access, preserve learner thinking and include a fading plan","Time arithmetic equals class period","Say learner not student","Do not claim remote specialized tools were called without making such calls","Use original framework order and exactly 4-3-2-1 success criteria table"],"source":"User-provided original Lesson Designer plus bundled specialized LQT learning-target, opener, scaffold and criteria skill sources"}

@mcp.tool(annotations={"readOnlyHint":True,"destructiveHint":False,"openWorldHint":False})
def review_integrated_lesson(grade_level:str,learning_target:str,class_minutes:int,lesson_plan:str)->dict:
 """Review existing lesson against integrated LQT source framework; return actionable fixes and evidence gaps without asserting unprovided work has passed."""
 log.info("LQT TOOL CALLED: review_integrated_lesson")
 if not grade_level.strip() or not learning_target.strip() or class_minutes<=0 or not lesson_plan.strip():return {"error":"Need grade, learning target, positive class minutes, and lesson plan text or a user-provided summary. Ask only for missing information."}
 return {"grade":grade_level,"target":learning_target,"minutes":class_minutes,"plan":lesson_plan,"checks":["Exact 10/25/50/15 time budget with sums","Opening uses authentic named LQT opening strategy and elicits thinking","G.I.S.T. mini-lesson and formative check prepares worthy task","One authentic work-session task and four actual engagement qualities","Scaffolds address barriers, preserve productive thinking, have fade plan","2-row 4-column success criteria in 4-3-2-1 order with four exact stems and 2–3 observable bullets per level tied to task","Closing uses named LQT closing strategy, evidence and next steps","Learner-friendly grade language and consistent target alignment"],"output":"Strengths, specific omissions, proposed repairs and instructional evidence to monitor; never invent observed results."}
if __name__=="__main__":mcp.run(transport="http",host="0.0.0.0",port=int(os.environ.get("PORT","8000")))
