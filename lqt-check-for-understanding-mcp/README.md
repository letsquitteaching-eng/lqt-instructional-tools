# LQT Check for Understanding MCP

Two read-only tools implement the source skill's **ELICIT → INTERPRET → RESPOND** sequence:
- `get_cfu_options`: returns timing-specific instructional categories and evidence guidance.
- `suggest_cfu_response`: recommends Reteach, Clarify or Extend based on an educator-selected pattern.

These tools supply structured resources and decisions, while ChatGPT writes the grade-specific prompts. Do not claim the software has observed or measured learning.

## GitHub / Render
Upload this **entire** `lqt-check-for-understanding-mcp` folder to the existing `lqt-instructional-tools` GitHub repository root. Do **not** replace Opener Generator's root `server.py` or the Gradual Release folder.

Create a separate Render Web Service using repository `letsquitteaching-eng/lqt-instructional-tools`, branch `main`, root directory **`lqt-check-for-understanding-mcp`**, build command `pip install -r requirements.txt`, start command `python server.py`. Test on Free; consider always-on hosting for publication.

Once Render has a confirmed hostname, the MCP endpoint is its HTTPS hostname + `/mcp`. Test both tools in ChatGPT and look for `LQT TOOL CALLED:` in Render Logs.

## Domain verification
The `.well-known/openai-apps-challenge` endpoint is already implemented. OpenAI issues a new, case-sensitive token for this hostname. Set it as the Render environment variable `OPENAI_DOMAIN_CHALLENGE`, and redeploy before pressing Verify Domain. The placeholder is NOT a valid token.

## Submission
Use the `submission-template` only after updating the URL and adding a real demonstration video URL. ZIP the **contents of submission-template**, not the server directory. Review positive/negative cases and scan findings before submitting.
