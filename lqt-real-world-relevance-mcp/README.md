# LQT When Will I EVER Use This? MCP

Upload the extracted folder to the GitHub repository as `lqt-real-world-relevance-mcp/`. Set Render Root Directory to that exact folder, build command `pip install -r requirements.txt` and start command `python server.py`. The endpoint is `https://lqt-real-world-relevance-mcp.onrender.com/mcp` if Render assigns the requested service name.

Tools: `get_real_world_relevance_framework` and `develop_relevance_activity`. Both are read-only, logged, and accept unrestricted free-text grade input. For domain verification set Render environment variable `OPENAI_DOMAIN_CHALLENGE` to the exact token given by OpenAI.
