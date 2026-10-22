# Deployment checklist

- [ ] Upload the `gradual-release/` directory inside the existing GitHub repository (keep original Opener Generator root intact).
- [ ] Create a separate Render Web Service using Root Directory `gradual-release`.
- [ ] Confirm the service is Live and copy its real HTTPS URL.
- [ ] Connect the actual `/mcp` URL in ChatGPT; confirm both tool names and call both.
- [ ] Check Render log lines `LQT TOOL CALLED:` for both functions.
- [ ] Replace placeholders in submission-template/mcp.json and plugin.json (video).
- [ ] ZIP only the contents of `submission-template/` to upload to OpenAI.
- [ ] Complete OpenAI's domain verification challenge for the actual host/domain.
- [ ] Scan tools; ensure zero findings.
- [ ] Verify 5 positive and 3 negative test cases.
- [ ] Verify video and required legal pages. Submit only after all dashboard checks pass.
