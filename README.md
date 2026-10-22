# LQT Instructional Tools — Opener Generator MCP pilot

This repository contains the **Opener Generator** MCP pilot, grounded in LQT's original opening strategy reference bank and instructional framework.

## Tools

- `find_opening_strategies`: retrieves established strategy names/descriptions based on an instructional purpose, grade, and target.
- `check_opener_alignment`: applies an explicit, teacher-reported checklist (not an automated pedagogical evaluation).

## Deploy on Render

1. Create a **Web Service** connected to this private GitHub repo.
2. Select **Python 3** and the `main` branch.
3. Build command: `pip install -r requirements.txt`.
4. Start command: `python server.py`.
5. For initial experimentation, select a free instance if available. Before publication, use a stable always-on instance and confirm current charges.
6. The MCP endpoint should be `https://YOUR-SERVICE.onrender.com/mcp`. Do not treat opening it in a browser as an MCP protocol test.
7. Use MCP Inspector or an MCP client to run `tools/list` and invoke both tools.

Render automatically supplies `PORT`; the server listens on `0.0.0.0`.

## Local setup

Requires Python 3.12+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python server.py
```

Visit `http://localhost:8000/mcp` with an MCP client. A normal browser GET may not yield a human-readable page.

## Instructional conversation

The ChatGPT skill, separately packaged at submission time, should first ask for the grade, then learning target/topic (one question at a time, unless supplied). Search strategies and prepare **five distinct** opening options. For each include strategy, how it works, why it fits, and what evidence to notice. Keep time around 10% of lesson and use **learner**, not student. Ask whether the teacher would like five more and exclude previously used names when searching again.

## References

`references/Opening Strategies-2.pdf` and `references/Additional Opening Framework.md` contain the authored instructional sources. `strategies.json` is a condensed, manually curated index for search, not a verbatim substitute for the PDF.

## Security and production readiness

This is a **public, read-only instructional prototype** with no credentials or personally identifiable learner data required. It does not store requests in a database. Avoid submitting personal learner information. Before directory submission, validate transport security, abuse controls, monitoring, privacy and legal policy URLs, and any authentication requirements in the current OpenAI review process. No directory approval is guaranteed.
