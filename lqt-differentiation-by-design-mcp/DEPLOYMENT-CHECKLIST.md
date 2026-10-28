# Deployment checklist
1. Extract ZIP and upload the actual folder `lqt-differentiation-by-design-mcp` to the existing GitHub repository. Do not replace root server.py.
2. Render new Web Service; Root Directory `lqt-differentiation-by-design-mcp`; Build `pip install -r requirements.txt`; Start `python server.py`.
3. After live, upload OpenAI package and connect MCP URL.
4. Copy domain challenge into Render environment variable `OPENAI_DOMAIN_CHALLENGE`, save and redeploy; verify in OpenAI.
5. Rescan for zero findings; test grade, target, task, need and focus, one question per turn.
6. Record YouTube demo; add URL to final review ZIP later.
