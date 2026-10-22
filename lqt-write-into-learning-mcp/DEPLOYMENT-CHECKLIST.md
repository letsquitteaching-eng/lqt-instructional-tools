# Deployment and Submission Checklist

1. Upload the entire `lqt-write-into-learning-mcp` folder to the GitHub repository root.
2. Create Render Python Web Service `lqt-write-into-learning-mcp` (root directory same), build `pip install -r requirements.txt`, start `python server.py`.
3. Upload separate OpenAI Platform plugin ZIP under Let's Quit Teaching Business developer identity.
4. Connect tools through MCP URL, get domain token and set `OPENAI_DOMAIN_CHALLENGE` in Render Environment; save/deploy and verify.
5. Rescan for zero findings. Create browser-accessible Custom MCP plugin for demo (avoid desktop-only imported plugin flow).
6. Supply YouTube video link to insert into review.demo_recording_url. Upload updated version, confirm review info, submit.
