# LQT Task Choice Generator MCP

Two read-only tools: `get_task_choice_framework` and `assess_task_choice_alignment`. Original five-choice task design preserved.

Deploy as a Python web service in Render with root directory `lqt-task-choice-generator-mcp`, build command `pip install -r requirements.txt`, start command `python server.py`. Add `OPENAI_DOMAIN_CHALLENGE` as a Render environment variable using the exact OpenAI token. The verification endpoint is `/.well-known/openai-apps-challenge`.
