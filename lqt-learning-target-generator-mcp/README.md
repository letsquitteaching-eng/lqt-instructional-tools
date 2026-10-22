# LQT Learning Target Generator MCP

Two read-only tools preserve the original standard-grounded design and review flow.

Set Render Root Directory to `lqt-learning-target-generator-mcp`, build `pip install -r requirements.txt`, run `python server.py`.

MCP endpoint: `https://lqt-learning-target-generator-mcp.onrender.com/mcp`.

For domain verification, set Render environment variable `OPENAI_DOMAIN_CHALLENGE` to the exact token from the OpenAI Platform and redeploy. The `/.well-known/openai-apps-challenge` endpoint then returns it.
