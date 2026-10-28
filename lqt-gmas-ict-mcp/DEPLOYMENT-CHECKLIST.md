# Upgrade existing GMAS ICT Creator to YouTube-specific video search

1. Replace the existing `lqt-gmas-ict-mcp` folder files in your GitHub repository (do not create a second Render service).
2. In Google Cloud, enable YouTube Data API v3 and create an API key. Configure key restrictions as compatible with server-side requests and API restrictions to YouTube Data API v3.
3. Render → existing `lqt-gmas-ict-mcp` → Environment: add `YOUTUBE_API_KEY`.
4. For article search, retain/add `BRAVE_SEARCH_API_KEY`. If you want only video search for now, Brave is optional.
5. Preserve `OPENAI_DOMAIN_CHALLENGE`. Deploy latest commit, confirm Live.
6. Test `discover_ict_sources(grade_level=5,topic="wetland habitats",source_type="videos")` and `check_ict_source_links` against a returned YouTube URL. Then test articles separately when Brave key is available.
7. Open existing OpenAI Platform GMAS ICT plugin → Upload new version with companion v1.2.0 ZIP; reconnect/refresh tools, verify domain if requested, rescan.
8. Add a demo video URL to `extensions.com.openai.review.demo_recording_url` before final review submission.

ICT output starts with SCENARIO and RESEARCH QUESTION; Lit Comp II EOC is a supported grade/course choice.
