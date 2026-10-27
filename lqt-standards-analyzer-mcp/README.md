# LQT Standards Analyzer — hosted MCP

This is a read-only MCP server based on the user's original Standards Analyzer v1.0.1.

Tools: `get_standards_analysis_framework`, `review_standards_analysis`. Both have read-only, nondestructive, closed-world annotations and log invocations.

Intake: ask for learner grade (free text), then request the standard **exactly as written**; one question at a time. Produce the five prescribed analysis sections with no more than five I can daily learning targets.

## Render
Service / root folder: `lqt-standards-analyzer-mcp`
Build: `pip install -r requirements.txt`
Start: `python server.py`
MCP: `https://lqt-standards-analyzer-mcp.onrender.com/mcp` (assuming Render assigns this hostname)

Verify domain by setting environment variable `OPENAI_DOMAIN_CHALLENGE` to exact supplied token, redeploying, and leaving OpenAI Challenge Base URL blank.

Privacy: https://letsquitteaching.com/ai-tools-privacy-policy/
Terms: https://letsquitteaching.com/ai-tools-terms-of-service/
