1. Upload `lqt-sort-generator-mcp` intact to the **repository main directory**. Do not overwrite root `server.py` used by Opener.
2. Create Render Web Service `lqt-sort-generator-mcp`, root directory `lqt-sort-generator-mcp`; build `pip install -r requirements.txt`; start `python server.py`.
3. Confirm Render Live and MCP URL `https://lqt-sort-generator-mcp.onrender.com/mcp`.
4. Upload **separate OpenAI submission ZIP**. It targets this URL.
5. On Platform MCPs tab Connect. Copy exact domain challenge token into Render Environment `OPENAI_DOMAIN_CHALLENGE`; deploy. Verify challenge URL then press Verify Domain.
6. Reconnect, scan, aim for 0 findings. Browser test in ChatGPT with Add Custom MCP Server (no auth), rather than desktop-only plugin link.
7. Record demo video. Provide YouTube URL; update `extensions.com.openai.review.demo_recording_url` in plugin.json and repackage only the OpenAI ZIP.
8. Review 5 positive/3 negative cases, upload final ZIP to existing Platform listing, submit for review.
