# Deployment

1. Upload this folder to the root of GitHub repository.
2. Render Python service name: `lqt-learning-target-generator-mcp`.
3. Root Directory: `lqt-learning-target-generator-mcp`.
4. Build command: `pip install -r requirements.txt`.
5. Start command: `python server.py`.
6. Upload companion OpenAI plugin ZIP and connect MCP.
7. Copy challenge token into Render `OPENAI_DOMAIN_CHALLENGE`, save/deploy, verify domain, rescan.
8. Test both tools through browser-based custom MCP plugin. Add YouTube demo link to `extensions.com.openai.review.demo_recording_url` in final manifest, then upload new version and submit.
