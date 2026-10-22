1. Upload this entire `lqt-scaffold-designer-mcp` folder to the existing GitHub repo.
2. Render New Web Service: `lqt-scaffold-designer-mcp`; Root Directory `lqt-scaffold-designer-mcp`; Python 3; build `pip install -r requirements.txt`; start `python server.py`.
3. Test `/mcp` (HTTP 406 / session error in normal browser is expected).
4. Upload the separate OpenAI ZIP via Platform Plugins; Connect the MCP.
5. Copy exact verification token into Render `OPENAI_DOMAIN_CHALLENGE`; redeploy; verify origin-root `/.well-known/openai-apps-challenge`.
6. Verify domain, scan for 0 findings; browser-test through Add custom MCP server.
7. Record video, supply URL; update final review ZIP and upload new version; submit.
