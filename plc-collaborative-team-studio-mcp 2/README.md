# PLC/Collaborative Team Studio MCP

Stateless MCP server for PLC/Collaborative Team Studio.

## Privacy / state model

This public version does **not** create a server-side database and does **not** save meeting records between conversations. The Studio can create a portable handoff record that the user can keep and paste/upload in a later conversation to continue previous work.

## Render — original LQT workflow

Create **New > Web Service** and connect the existing `lqt-instructional-tools` GitHub repository.

- Branch: `main`
- Root Directory: `plc-collaborative-team-studio-mcp`
- Runtime: Python 3
- Build Command: `pip install -r requirements.txt`
- Start Command: `python server.py`
- Health Check Path: `/health`

Render supplies `PORT` automatically. Do not manually set `PORT`.

After deployment, the MCP endpoint is:
`https://plc-collaborative-team-studio.onrender.com/mcp`

The only optional environment variable needed later is the OpenAI domain-verification token supplied during submission.
