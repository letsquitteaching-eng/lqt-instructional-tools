# LQT Sort Generator MCP

Tools: `get_sort_menu` and `get_sort_build_framework`. Tools are read-only; output guidance supports educator judgment.

Render settings: Python, branch `main`, root directory **lqt-sort-generator-mcp**, build `pip install -r requirements.txt`, start `python server.py`. Use a free instance for initial testing if available. Expected endpoint `https://lqt-sort-generator-mcp.onrender.com/mcp` if that service name is available.

Set Render environment variable `OPENAI_DOMAIN_CHALLENGE` to the **exact** per-host token copied using OpenAI's copy button. Save and deploy. Domain verification URL: `https://lqt-sort-generator-mcp.onrender.com/.well-known/openai-apps-challenge`. If token says NOT_CONFIGURED, the environment variable was not loaded. Do not set the token in source code.

A browser opening `/mcp` can show an HTTP 406 text/event-stream error; that is expected and does not substitute for actual MCP tool calls. `/` can return 404. The two MCP tools log `LQT TOOL CALLED`. Do not send identifying learner records.
