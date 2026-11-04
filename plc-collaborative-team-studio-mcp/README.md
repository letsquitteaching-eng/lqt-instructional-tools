# PLC/Collaborative Team Studio MCP

GitHub/Render deployment folder for the PLC/Collaborative Team Studio plugin.

## Render — original LQT workflow
Create **New > Web Service** and connect the GitHub repository.

- Branch: `main`
- Root Directory: `plc-collaborative-team-studio-mcp`
- Runtime: Python 3
- Build Command: `pip install -r requirements.txt`
- Start Command: `python server.py`
- Health Check Path: `/health`

Render supplies `PORT` automatically. Do not manually set `PORT`.

After deployment, the MCP endpoint is:
`https://YOUR-RENDER-SERVICE.onrender.com/mcp`

Do not build/upload the OpenAI listing ZIP until this endpoint is live and tested.
