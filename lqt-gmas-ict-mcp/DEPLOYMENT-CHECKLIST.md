# Deploy and verify
1. Upload the whole `lqt-gmas-ict-mcp` folder to repository root.
2. Render name: `lqt-gmas-ict-mcp`; Python 3; branch `main`; Root Directory `lqt-gmas-ict-mcp`.
3. Build: `pip install -r requirements.txt`; Start: `python server.py`.
4. MCP URL: `https://lqt-gmas-ict-mcp.onrender.com/mcp`.
5. Upload companion OpenAI ZIP in Plugins, select Let's Quit Teaching business identity, connect MCP.
6. Render > Environment: `OPENAI_DOMAIN_CHALLENGE` set to OpenAI token; Save and Deploy; verify domain with blank Challenge Base URL.
7. Rescan MCPs and check for 0 findings; test in browser with Custom MCP plugin.
8. Share demo video URL to add to `extensions.com.openai.review.demo_recording_url` in final ZIP; upload new version and submit for review.
