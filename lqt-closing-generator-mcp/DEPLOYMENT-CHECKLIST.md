# Deployment checklist
1. Extract ZIP and upload the **lqt-closing-generator-mcp folder** to the existing GitHub repository, not the ZIP.
2. Render service: `lqt-closing-generator-mcp`; root directory: `lqt-closing-generator-mcp`.
3. Build: `pip install -r requirements.txt`; start: `python server.py`.
4. MCP endpoint: `https://lqt-closing-generator-mcp.onrender.com/mcp` if Render uses requested name.
5. OpenAI domain token: Render Environment `OPENAI_DOMAIN_CHALLENGE`, save and deploy; leave Challenge Base URL blank.
6. Connect MCP on OpenAI Platform; scan for 0 findings; browser-test grade, learning target, five distinct closings and develop option.
7. After recording a demonstration video, update OpenAI review ZIP with review.demo_recording_url, increment version and submit.
