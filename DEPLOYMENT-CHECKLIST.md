# Next steps (no command-line required)

1. Open your private GitHub repository in a browser.
2. Choose **Add file → Upload files**.
3. Upload **server.py**, **requirements.txt**, **render.yaml**, **strategies.json**, **README.md**, and **DEPLOYMENT-CHECKLIST.md** from the unzipped folder. Also upload the two files inside **references/**, preserving the folder.
4. Select **Commit changes**.
5. Open https://dashboard.render.com/ and create a **New → Web Service**.
6. Connect GitHub, select `lqt-instructional-tools`, and choose the `main` branch.
7. Select Python. Use build `pip install -r requirements.txt` and start `python server.py`. Choose the instance tier for testing.
8. Deploy; copy the Render URL shown for your service.
9. Verify the MCP URL with an MCP Inspector or client before considering plugin packaging.

**Do not upload ZIP itself into the repository as the only file.** GitHub needs the extracted source files. Do not share any API keys or passwords here.
