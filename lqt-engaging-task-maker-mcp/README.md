# LQT Engaging Task Maker — Hosted MCP

Source: original user-provided Engaging Learning Task Maker v1.0.1.

Tools: `get_engaging_task_framework` and `review_engaging_task`. Both read-only and logged.

Service: `lqt-engaging-task-maker-mcp`; Root directory: `lqt-engaging-task-maker-mcp`; Build: `pip install -r requirements.txt`; Start: `python server.py`; endpoint: `https://lqt-engaging-task-maker-mcp.onrender.com/mcp`.

Intake: unrestricted typed grade, then learning target (or standard/topic) — one question per turn. Output original exact five-part order. At least four purposeful engagement qualities; not a worksheet; learner-friendly language.

To verify domain add Render environment `OPENAI_DOMAIN_CHALLENGE` equal to exactly the token from OpenAI and redeploy; challenge base URL blank in OpenAI. Then connect MCP and rescan.
