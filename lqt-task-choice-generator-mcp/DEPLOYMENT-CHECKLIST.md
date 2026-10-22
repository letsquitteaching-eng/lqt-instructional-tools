1. Upload entire `lqt-task-choice-generator-mcp` folder into GitHub repo root.
2. Render new web service: name `lqt-task-choice-generator-mcp`, root `lqt-task-choice-generator-mcp`, build `pip install -r requirements.txt`, start `python server.py`.
3. Upload separate OpenAI plugin ZIP to platform, connect endpoint `https://lqt-task-choice-generator-mcp.onrender.com/mcp`.
4. Add exact OpenAI verification token using Render Environment key `OPENAI_DOMAIN_CHALLENGE`, save and deploy. Leave Challenge Base URL blank, verify domain.
5. Scan tools, check 0 findings, create custom browser MCP connection, test tools.
6. Provide YouTube demonstration URL and update `extensions.com.openai.review.demo_recording_url` in final review ZIP before submitting.
