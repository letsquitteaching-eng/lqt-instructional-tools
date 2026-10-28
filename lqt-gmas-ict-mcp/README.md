# LQT GMAS ICT Creator MCP, v1.2.0

Four MCP tools: get_gmas_ict_framework, review_gmas_ict_design, discover_ict_sources, check_ict_source_links.

## Search configuration

- `YOUTUBE_API_KEY`: **Google Cloud YouTube Data API v3** key for video-only searches on YouTube and video-ID verification. Enable YouTube Data API v3 in Google Cloud and create an API key. Never commit a key to GitHub.
- `BRAVE_SEARCH_API_KEY`: **Brave Search API** key for published article search only. If omitted, video search remains available; if YouTube key is omitted, articles can still be searched.
- `OPENAI_DOMAIN_CHALLENGE`: OpenAI Platform domain verification token.

Google's YouTube APIs use quota; `search.list` is more expensive than `videos.list`. Costs/quotas depend on the account. Both APIs are called only when the tool is invoked. YouTube results are limited to videos, safeSearch strict, and embeddable results. Verification checks public video IDs, not geographic availability, classroom playback, or the video's factual content. Articles are searched through Brave and HTTP-checked independently. Brief extracted excerpts are not full-text reproduction.

**Render**: existing service `lqt-gmas-ict-mcp`; Root Directory `lqt-gmas-ict-mcp`; Build Command `pip install -r requirements.txt`; Start Command `python server.py`. Preserve the existing Render service and environment variables. Update files in the existing GitHub folder, then deploy the latest commit.

## Security

Requests to arbitrary article URLs use a conservative public-address guard; redirects are not followed. The results must not be represented as classroom access tests or a substitute for reading source material.

## v1.3.1 intake
Grade, topic and media selection are now required; media is additional to complete reading passages. Existing YOUTUBE_API_KEY / BRAVE_SEARCH_API_KEY are retained. Audio clips require trustworthy discoverable source links or clearly disclose that none was verified.

ICT output starts with SCENARIO and RESEARCH QUESTION; Lit Comp II EOC is a supported grade/course choice.
