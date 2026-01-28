"""
Jira API client.

Naming convention:
- Functions: jira_* (e.g., jira_create_story)
- Constants: JIRA_* (in config.py)
"""

import base64

import httpx

from app.config import (
    JIRA_BASE_URL,
    JIRA_EMAIL,
    JIRA_API_TOKEN,
    JIRA_PROJECT_KEY,
    JIRA_ISSUE_TYPE,
    JIRA_LABELS,
    JIRA_DESCRIPTION,
    JIRA_TIMEOUT_SECONDS,
    ERROR_MSG_MAX_LENGTH,
)


def _jira_build_auth_header() -> str:
    """Create Basic Auth header for Jira."""
    credentials = f"{JIRA_EMAIL}:{JIRA_API_TOKEN}".encode()
    return "Basic " + base64.b64encode(credentials).decode()


async def jira_create_story(summary: str) -> tuple[str, str]:
    """
    Create a Jira story.
    
    Returns (issue_key, browse_url).
    Raises RuntimeError on failure.
    """
    jira_api_url = f"{JIRA_BASE_URL}/rest/api/3/issue"
    request_headers = {
        "Authorization": _jira_build_auth_header(),
        "Content-Type": "application/json",
    }
    request_payload = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": summary,
            "issuetype": {"name": JIRA_ISSUE_TYPE},
            "labels": JIRA_LABELS,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [{"type": "paragraph", "content": [{"type": "text", "text": JIRA_DESCRIPTION}]}],
            },
        }
    }

    async with httpx.AsyncClient(timeout=JIRA_TIMEOUT_SECONDS) as http_client:
        response = await http_client.post(jira_api_url, headers=request_headers, json=request_payload)
        
        if response.status_code >= 400:
            error_detail = response.text[:ERROR_MSG_MAX_LENGTH]
            raise RuntimeError(f"Jira error: {error_detail}")
        
        response_data = response.json()
        issue_key = response_data.get("key")
        if not issue_key:
            raise RuntimeError("No issue key returned")

    browse_url = f"{JIRA_BASE_URL}/browse/{issue_key}"
    return issue_key, browse_url
