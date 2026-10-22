# Deployment and review checklist

- [ ] GitHub root contains `lqt-check-for-understanding-mcp/server.py` (no `server 2.py`).
- [ ] Render Root Directory is `lqt-check-for-understanding-mcp`.
- [ ] Live `https://<service>.onrender.com/mcp` responds as MCP.
- [ ] Test both tools in ChatGPT; find logged tool names on Render.
- [ ] Add OpenAI-issued token (exact case) to `OPENAI_DOMAIN_CHALLENGE` Render environment variable and redeploy.
- [ ] Confirm `/.well-known/openai-apps-challenge` returns token exactly; verify domain.
- [ ] Finalize submission-template `mcp.json` real host, `plugin.json` actual video URL.
- [ ] Upload new MCP-backed ZIP; connect/scan with zero findings.
- [ ] Confirm five positive and three negative activation test cases, review video and release notes.
- [ ] Submit for review when all blockers clear.
