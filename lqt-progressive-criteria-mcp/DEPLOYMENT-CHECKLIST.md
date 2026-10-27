# Deploy and submit

1. Extract ZIP and upload its actual `lqt-progressive-criteria-mcp` folder to GitHub, **not** the ZIP file.
2. Create Render Web Service: Python 3, branch main, Root Directory `lqt-progressive-criteria-mcp`, build `pip install -r requirements.txt`, start `python server.py`.
3. Confirm Render is Live and MCP endpoint is `https://lqt-progressive-criteria-mcp.onrender.com/mcp`. A Safari MCP protocol error is expected.
4. Upload companion OpenAI ZIP to Platform under Let’s Quit Teaching. Connect two tools.
5. Copy OpenAI domain token into Render environment variable `OPENAI_DOMAIN_CHALLENGE`. Save/deploy. Verify domain, rescan to 0 findings.
6. Test any entered grade level and correct exact 4→1 table in browser-based ChatGPT plugin.
7. Record demo and provide YouTube URL to add as `extensions.com.openai.review.demo_recording_url` in a version-bumped final ZIP.
