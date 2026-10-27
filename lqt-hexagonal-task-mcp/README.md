# LQT Hexagonal Task Generator MCP

Two read-only tools preserve the four-question intake, exact deck count and teacher reasoning guidance. Users enter any grade level or learning setting as free text.

### Deploy
- Repository folder: `lqt-hexagonal-task-mcp`
- Render service: `lqt-hexagonal-task-mcp`
- Root Directory: `lqt-hexagonal-task-mcp`
- Build: `pip install -r requirements.txt`
- Start: `python server.py`
- Endpoint: `https://lqt-hexagonal-task-mcp.onrender.com/mcp`

Domain verification: set `OPENAI_DOMAIN_CHALLENGE` in Render Environment to the exact OpenAI token and deploy; visit `/.well-known/openai-apps-challenge`. Never commit secrets. The MCP provides design guidance and validations but does not itself create a PDF; ChatGPT can create the actual printable artifact if file tools are available.
