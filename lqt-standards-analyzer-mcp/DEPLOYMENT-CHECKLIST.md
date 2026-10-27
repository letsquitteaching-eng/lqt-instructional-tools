# Deployment checklist
1. Extract the ZIP. Upload the `lqt-standards-analyzer-mcp` **folder and files** into `letsquitteaching-eng/lqt-instructional-tools`; do not overwrite root server.py.
2. Create a Render Web Service named `lqt-standards-analyzer-mcp`, root directory `lqt-standards-analyzer-mcp`.
3. Build `pip install -r requirements.txt`, start `python server.py`; wait for Live.
4. In OpenAI upload the companion plugin ZIP, under Business — Let's Quit Teaching.
5. Connect `https://lqt-standards-analyzer-mcp.onrender.com/mcp`; two tools should appear.
6. Copy exact domain challenge token to Render Environment as `OPENAI_DOMAIN_CHALLENGE`, save/deploy.
7. Verify domain in OpenAI (blank Challenge Base URL) and rescan for zero findings.
8. Test grade question, standard verbatim intake, all five outputs, and fidelity. Record demo and add link to review manifest in new version.
