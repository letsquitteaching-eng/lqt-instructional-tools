# LQT Gradual Release Idea Generator MCP

Read-only educational MCP tools, based on the existing author-provided instructional skill.

- `get_gradual_release_framework`: retrieves the four phases and design constraints.
- `suggest_release_response`: suggests an evidence-responsive move from teacher-supplied flags (not automated grading).

## Deployment in your existing GitHub repository

Upload **the contents** of this package into `gradual-release/` in `letsquitteaching-eng/lqt-instructional-tools`. Do not overwrite the current Opener Generator `server.py`.

Create a **new** Render Web Service connected to the same GitHub repository, with **Root Directory** `gradual-release`, **Build Command** `pip install -r requirements.txt`, **Start Command** `python server.py`, and branch `main`. Free for initial testing; use stable always-on hosting for public launch.

Once Render assigns an HTTPS hostname, the MCP URL will be `https://<your-new-host>.onrender.com/mcp`. Verify it using the ChatGPT MCP connection and invoke both tools. The standard browser GET may return a content-negotiation error.

OpenAI domain verification uses a token provided by its submission page. Do not reuse the older Opener Generator token. Verify the exact new domain and challenge path according to current dashboard instructions. You may alternatively configure a verified custom domain, subject to platform rules.

Use `submission-template/` **only after** replacing its endpoint placeholder with the live URL and adding a real accessible demo recording URL. Do not submit placeholder values.
