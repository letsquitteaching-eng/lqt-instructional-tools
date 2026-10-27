# Deployment and testing

1. Upload the `lqt-quality-rubric-mcp` folder into your existing GitHub repository root.
2. Create Render service `lqt-quality-rubric-mcp` on main; Root Directory `lqt-quality-rubric-mcp`; build `pip install -r requirements.txt`; start `python server.py`.
3. Upload companion OpenAI ZIP under Business — Let's Quit Teaching.
4. Connect `https://lqt-quality-rubric-mcp.onrender.com/mcp`.
5. Copy domain challenge to Render `OPENAI_DOMAIN_CHALLENGE`, deploy, verify domain, and rescan.
6. Test the two tools with a browser-based custom MCP connection.
7. After recording a YouTube demonstration, update `extensions.com.openai.review.demo_recording_url` and version in plugin.json, upload new version, submit.
