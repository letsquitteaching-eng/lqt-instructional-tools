"""LQT GMAS ICT Creator: grade-routed Georgia Milestones practice guidance."""
import logging
import os
import socket
import ipaddress
import re
from urllib.parse import urlparse, parse_qs
import httpx
from bs4 import BeautifulSoup
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lqt.gmas_ict")
mcp = FastMCP("LQT GMAS ICT Creator")
VALID_GRADES = {3, 4, 5, 6, 7, 8, 10}

@mcp.custom_route("/.well-known/openai-apps-challenge", methods=["GET"])
async def openai_domain_verification(request: Request) -> PlainTextResponse:
    return PlainTextResponse(os.environ.get("OPENAI_DOMAIN_CHALLENGE", ""))

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def get_gmas_ict_framework(grade_level: int, topic: str, supplemental_extended_writing: bool = False) -> dict:
    """Retrieve author-defined grade-specific Georgia Milestones Interpreting & Constructing Texts practice structure. Designed as original practice, not official GMAS items. Accept grade 3,4,5,6,7,8,10 and a teacher-selected topic."""
    logger.info("LQT TOOL CALLED: get_gmas_ict_framework")
    if grade_level not in VALID_GRADES:
        return {"error": "Supported grades: 3, 4, 5, 6, 7, 8, 10."}
    if not topic or not topic.strip():
        return {"error": "A topic is required after grade selection."}
    peer_revision = grade_level in (4, 6, 7) and not supplemental_extended_writing
    genre = "opinion" if grade_level in (3, 4, 5) else "argument"
    source_count = "2–3" if grade_level == 3 else "3–4" if grade_level in (5, 8, 10) else "grade-appropriate set; no fixed count"
    general = {
        "grade_level": grade_level, "topic": topic.strip(),
        "workflow": "assessment-style peer revision" if peer_revision else "supplemental extended writing practice" if supplemental_extended_writing and grade_level in (4, 6, 7) else "extended writing ICT",
        "genre": genre,
        "intake": ["Which grade level: 3, 4, 5, 6, 7, 8, or 10?", "What topic would you like the ICT task to explore?"],
        "common_design": [
            "Present one continuous classroom-ready learner product with clear headings, without code blocks.",
            "Create an authentic research-and-analysis scenario and credible, clearly labeled sources.",
            "Use grade-appropriate complexity, source load, analysis demand and language.",
            "Choose meaningful multimodal source format for the task; do not lock particular media to a grade.",
            "Use discover_ict_sources for verified external media when enabled; otherwise write clearly labeled original passages. Never invent real media titles, URLs, runtimes, quotes or facts.",
            "If verified external media is unavailable, use an explicitly labeled original self-contained multimodal representation.",
            "Make all source-dependent questions answerable using provided sources.",
            "Do not present generated tasks as official Georgia Milestones items.",
            "No answer key, model response, rubric, teacher commentary or extensions unless requested.",
            "Use original attached Georgia guidance documents as the authority for assessment expectations; Grade 3 example is not a universal template."
        ],
        "final_question": "Would you like to revise the topic, source set, or grade-level complexity?",
        "source": "LQT GMAS ICT Creator original instructional skill"
    }
    if peer_revision:
        general["requirements"] = [
            "Include a scenario, grade-appropriate source set and source-based Interpreting Texts items.",
            "Provide a credible constructed-text draft from a learner at the selected grade; revise it instead of writing an entirely new response.",
            "Make the draft genuinely grade-appropriate with strengths and a few authentic, not exaggerated, revision opportunities.",
            "Write selected-response and technology-enhanced-style peer revision items totaling exactly 8 points, not necessarily a fixed number of questions.",
            "Align revision to Purpose and Organization, Evidence and Elaboration, and Language Usage and Conventions.",
            "Allow some original wording to be effective, or proposed revisions to be worse; require evaluative judgment and preserve learner voice.",
            "Grade 4: clear opinion, grouping, supported reasons and attempted conclusion with credible elementary vocabulary.",
            "Grade 6: credible middle-school claim, source evidence, developing reasoning, transitions, and attempted counterclaim.",
            "Grade 7: stronger cohesion, integrated evidence, tone, nuanced counterclaim and more sophisticated reasoning than Grade 6."
        ]
        general["revision_points"] = 8
    else:
        general["source_count_guidance"] = source_count
        general["requirements"] = [
            "Include three source-based Interpreting Texts questions before writing, mixing selected-response and technology-enhanced-style types.",
            "State Research Question, Purpose, Audience and directions to use source evidence.",
            f"Use {genre} genre with grade-appropriate development and cited source evidence.",
            "Provide a grade-and-genre-specific first-person Writer's Checklist around Purpose and Organization, Evidence and Elaboration, and Language Usage and Conventions.",
            "Grades 4, 6 and 7: label extended writing as supplemental practice when specifically requested, not end-of-year Section 1 format.",
            "Grade 3: accessible vocabulary, concrete context and manageable paragraph/developed short response.",
            "Grade 5: independent comparison, elaboration, reasons and evidence.",
            "Grade 8: claim, multi-source reasoning, organization and counterclaim.",
            "Grade 10: nuanced synthesis, attribution and more sophisticated counterclaim reasoning."
        ]
    return general

@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False})
def review_gmas_ict_design(grade_level: int, workflow: str, topic: str, revision_points: int = 0, has_original_sources: bool = True, has_grade_authentic_draft: bool = False, contains_unverified_external_media: bool = False) -> dict:
    """Return transparent checks for a teacher-provided ICT practice draft. Only reviews supplied design flags, not actual essay content or official Georgia alignment."""
    logger.info("LQT TOOL CALLED: review_gmas_ict_design")
    if grade_level not in VALID_GRADES:
        return {"error": "Supported grades: 3, 4, 5, 6, 7, 8, 10."}
    if not topic.strip():
        return {"error": "A topic is required."}
    peer = grade_level in (4,6,7)
    workflow_lower = workflow.strip().lower()
    selected_peer = "peer" in workflow_lower
    notes = []
    if peer and not selected_peer and "supplemental" not in workflow_lower:
        notes.append("Grades 4,6,7 default to assessment-style peer revision; extended writing must be explicitly labeled supplemental.")
    if not peer and selected_peer:
        notes.append("Grades 3,5,8,10 follow extended-writing ICT practice.")
    if selected_peer and revision_points != 8:
        notes.append("Peer revision items must total exactly 8 points.")
    if selected_peer and not has_grade_authentic_draft:
        notes.append("Peer revision requires a credible grade-level learner draft with real strengths and purposeful revision opportunities.")
    if not has_original_sources:
        notes.append("Use source material with permissions or original self-contained text, not unattributed copied passages.")
    if contains_unverified_external_media:
        notes.append("Remove or verify external media details; do not invent titles, links, runtimes or content.")
    return {"grade_level": grade_level, "topic": topic.strip(), "reported_workflow": workflow,
        "flagged_checks": notes, "always_review": [
          "Questions must be answerable with supplied source materials.",
          "Grade-level complexity, genre and draft authenticity require educator judgment.",
          "Multimodal resources may vary by topic, not fixed by grade.",
          "No official GMAS endorsement or item status should be implied.",
          "No model answer or answer key unless requested."
        ], "limitations": "This check applies stated flags only; it does not inspect actual source text or verify official standards."}



def _public_http_url(url: str) -> bool:
    """Conservative SSRF guard. Do not make requests to local/private addresses."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username or parsed.password:
            return False
        hostname = parsed.hostname.rstrip(".").lower()
        if hostname in {"localhost", "localhost.localdomain"} or hostname.endswith((".local", ".internal", ".test")):
            return False
        try:
            addrs = socket.getaddrinfo(hostname, parsed.port or (443 if parsed.scheme == "https" else 80), type=socket.SOCK_STREAM)
            if not addrs:
                return False
            return all(ipaddress.ip_address(a[4][0]).is_global for a in addrs)
        except (OSError, ValueError):
            return False
    except (ValueError, TypeError):
        return False


def _probe_url(url: str, include_article_excerpt: bool = False) -> dict:
    if not _public_http_url(url):
        return {"status": "blocked_or_unresolvable", "working_link_verified": False}
    try:
        # Do not follow redirects: a redirect destination would require a separate SSRF check.
        with httpx.Client(timeout=7.0, follow_redirects=False, headers={"User-Agent": "LQT-GMAS-ICT-SourceChecker/1.1"}, trust_env=False) as client:
            response = client.head(url)
            if response.status_code in (403, 405, 429) or (include_article_excerpt and response.status_code == 200):
                response = client.get(url, headers={"Range": "bytes=0-131071"})
        code = response.status_code
        good = 200 <= code < 300
        result = {"status": "reachable" if good else "redirect_not_followed" if 300 <= code < 400 else "blocked_by_site" if code in (401,403,429) else "http_error", "http_status": code, "working_link_verified": good, "content_type": response.headers.get("content-type", "")}
        if include_article_excerpt and good and "html" in result["content_type"].lower():
            if len(response.content) <= 200000:
                soup = BeautifulSoup(response.text, "html.parser")
                for tag in soup(["script", "style", "nav", "footer", "header"]): tag.decompose()
                paras=[p.get_text(" ",strip=True) for p in soup.select("article p, main p, p")]
                meaningful=[p for p in paras if len(p)>70]
                if meaningful:
                    result["excerpt"]=" ".join(meaningful)[:900]
                    result["full_text_retrieved"] = False
        return result
    except (httpx.HTTPError, UnicodeError, ValueError, OSError) as exc:
        return {"status": "verification_failed", "working_link_verified": False, "reason": type(exc).__name__}


def _youtube_video_id(url: str) -> str | None:
    """Accept only a video URL on genuine YouTube domains."""
    try:
        p = urlparse(url)
        if p.scheme != "https" or not p.hostname:
            return None
        host = p.hostname.rstrip(".").lower()
        if host in {"youtu.be", "www.youtu.be"}:
            video_id = p.path.strip("/").split("/")[0]
        elif host in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
            video_id = (parse_qs(p.query).get("v") or [""])[0]
            if not video_id and p.path.startswith(("/shorts/", "/embed/")):
                video_id = p.path.split("/")[2]
        else:
            return None
        return video_id if re.fullmatch(r"[A-Za-z0-9_-]{11}",video_id) else None
    except (ValueError,IndexError):
        return None


def _youtube_details(ids: list[str], key: str) -> tuple[dict, str | None]:
    """Verify video IDs against the official videos endpoint, not a page HEAD request."""
    if not ids:
        return {}, None
    try:
        response = httpx.get("https://www.googleapis.com/youtube/v3/videos", params={
            "part":"snippet,contentDetails,status", "id":",".join(ids), "key":key,
        }, timeout=12.0)
        response.raise_for_status()
        hits=response.json().get("items",[])
        return {item["id"]:item for item in hits if item.get("id")},None
    except (httpx.HTTPError,ValueError,KeyError) as exc:
        return {},f"YouTube verification unavailable: {type(exc).__name__}; check API key, quotas and restrictions."


@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": True})
def discover_ict_sources(grade_level: int, topic: str, source_type: str = "both", max_per_type: int = 3) -> dict:
    """Search published articles using Brave and YouTube videos using the official YouTube Data API. Verify article HTTP reachability and YouTube video existence/status; never claim full article reading or video viewing."""
    logger.info("LQT TOOL CALLED: discover_ict_sources")
    if grade_level not in VALID_GRADES or not topic.strip():
        return {"error":"Use grades 3,4,5,6,7,8,10 and a nonempty topic."}
    if source_type not in {"both","articles","videos"} or not 1 <= max_per_type <= 5:
        return {"error":"source_type must be both/articles/videos and max_per_type 1–5."}
    requested = [source_type] if source_type != "both" else ["articles","videos"]
    items, problems = [], []
    query = f"{topic.strip()[:200]} grade {grade_level} educational"
    if "articles" in requested:
        brave=os.environ.get("BRAVE_SEARCH_API_KEY", "").strip()
        if not brave:
            problems.append({"source_type":"articles","error":"BRAVE_SEARCH_API_KEY not configured"})
        else:
            try:
                response=httpx.get("https://api.search.brave.com/res/v1/web/search",params={"q":query,"count":min(12,max_per_type*3),"safesearch":"strict","search_lang":"en"},headers={"Accept":"application/json","X-Subscription-Token":brave},timeout=12.0)
                response.raise_for_status()
                for hit in response.json().get("web",{}).get("results",[]):
                    if len([s for s in items if s["source_type"]=="articles"])>=max_per_type:break
                    url=hit.get("url","")
                    if not url.startswith("https://"):continue
                    items.append({"source_type":"articles","title":hit.get("title",""),"url":url,"publisher_or_domain":urlparse(url).netloc,"search_description":(hit.get("description") or "")[:500],"retrieved_via":"Brave Search API","link_check":_probe_url(url,include_article_excerpt=True)})
            except (httpx.HTTPError,ValueError) as exc:
                problems.append({"source_type":"articles","error":type(exc).__name__,"detail":"Brave article search failed; check API key, quota or network."})
    if "videos" in requested:
        ytkey=os.environ.get("YOUTUBE_API_KEY","").strip()
        if not ytkey:
            problems.append({"source_type":"videos","error":"YOUTUBE_API_KEY not configured"})
        else:
            try:
                search=httpx.get("https://www.googleapis.com/youtube/v3/search",params={"part":"snippet","q":query,"type":"video","videoEmbeddable":"true","safeSearch":"strict","maxResults":min(15,max_per_type*3),"key":ytkey},timeout=12.0)
                search.raise_for_status()
                hits=search.json().get("items",[])
                ids=[h.get("id",{}).get("videoId","") for h in hits]
                ids=[i for i in ids if re.fullmatch(r"[A-Za-z0-9_-]{11}",i)]
                details,error=_youtube_details(ids,ytkey)
                if error:problems.append({"source_type":"videos","error":error})
                for hit in hits:
                    if len([s for s in items if s["source_type"]=="videos"])>=max_per_type:break
                    video_id=hit.get("id",{}).get("videoId","")
                    if video_id not in details:continue
                    detail=details[video_id]
                    status=detail.get("status",{})
                    if status.get("privacyStatus")!="public" or status.get("uploadStatus") not in (None,"processed"):continue
                    snippet=detail.get("snippet") or hit.get("snippet",{})
                    url=f"https://www.youtube.com/watch?v={video_id}"
                    items.append({"source_type":"videos","title":snippet.get("title",""),"url":url,"publisher_or_domain":"youtube.com","channel":snippet.get("channelTitle",""),"search_description":(snippet.get("description") or "")[:500],"published_at":snippet.get("publishedAt"),"duration_iso8601":detail.get("contentDetails",{}).get("duration"),"retrieved_via":"YouTube Data API v3","link_check":{"status":"video_id_verified_public","working_link_verified":True,"verification_method":"YouTube videos.list API","browser_playback_verified":False},"video_watched_or_transcribed":False})
            except (httpx.HTTPError,ValueError) as exc:
                problems.append({"source_type":"videos","error":type(exc).__name__,"detail":"YouTube API request failed; check key, quota, permissions or network."})
    return {"grade_level":grade_level,"topic":topic.strip(),"sources":items,"search_errors":problems,
        "verification_notes":["Articles are checked by HTTP; redirects and anti-bot protections may prevent verification.","YouTube video IDs are checked with the official YouTube videos.list API. Existence and public status do not guarantee playback in every classroom or region.","Video descriptions and durations come from YouTube metadata. Video content was not watched or transcribed.","Search snippets and brief extracted article excerpts are not full article text; do not reproduce copyrighted material or fabricate passages.","Only write source-specific questions when source content or a reliable transcript has actually been supplied and reviewed."],
        "fallback":"If verified content is unavailable, provide clearly labeled original self-contained passages, charts, or tables."}


@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": True})
def check_ict_source_links(urls: list[str]) -> dict:
    """Verify up to five public article links via HTTP and YouTube video URLs via YouTube's official API. Does not review video content, guarantee playback, or grant reproduction rights."""
    logger.info("LQT TOOL CALLED: check_ict_source_links")
    if not 1<=len(urls)<=5:return {"error":"Provide 1–5 URLs."}
    ids={url:_youtube_video_id(url) for url in urls}
    ytids=[v for v in ids.values() if v]
    key=os.environ.get("YOUTUBE_API_KEY","").strip()
    details,error=_youtube_details(list(dict.fromkeys(ytids)),key) if key and ytids else ({},"YOUTUBE_API_KEY not configured" if ytids else None)
    results=[]
    for url in urls:
        if ids[url]:
            info=details.get(ids[url])
            if info and info.get("status",{}).get("privacyStatus")=="public":
                check={"status":"video_id_verified_public","working_link_verified":True,"verification_method":"YouTube videos.list API","browser_playback_verified":False}
            else:
                check={"status":"unverified" if error else "not_public_or_unavailable","working_link_verified":False,"reason":error or "Video ID absent or private in YouTube API response"}
        elif urlparse(url).hostname and urlparse(url).hostname.lower().rstrip(".") in {"youtube.com","www.youtube.com","m.youtube.com","youtu.be","www.youtu.be"}:
            check={"status":"invalid_youtube_video_url","working_link_verified":False}
        else:
            check=_probe_url(url)
        results.append({"url":url,"link_check":check})
    return {"results":results,"limitation":"Video ID availability does not prove classroom playback or content accuracy. Article HTTP status does not prove complete readable text or copyright permission."}

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
