# Deployment checklist

1. Extract deployment ZIP and upload the actual `lqt-real-world-relevance-mcp` directory to GitHub repository `letsquitteaching-eng/lqt-instructional-tools`. Do not upload ZIP or overwrite root `server.py`.
2. New Render Web Service, name/root directory `lqt-real-world-relevance-mcp`, build `pip install -r requirements.txt`, start `python server.py`.
3. Confirm Live, connect MCP URL `https://lqt-real-world-relevance-mcp.onrender.com/mcp` in OpenAI plugin.
4. Add `OPENAI_DOMAIN_CHALLENGE` from OpenAI in Render environment, deploy, verify domain, rescan.
5. Test grade-level adaptivity, first five authentic connections, second five meaningfully different activities and selected-activity expansion. Record demo and update review ZIP.
