"""
FastAPI app with /login and /jira routes.

- Admin authenticates via /login (verifies against Jira)
- Once authenticated, anyone can use /jira to create tickets
- Admin logout clears credentials, locking the app
"""

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.admin_credentials import (
    admin_is_authenticated,
    admin_set_credentials,
    admin_clear_credentials,
)
from app.config import JIRA_PROJECT_KEY, JIRA_SUMMARY_MIN_LENGTH
from app.jira_client import jira_create_story, jira_verify_credentials

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def api_home() -> RedirectResponse:
    """Redirect to /jira if admin authenticated, else /login."""
    if admin_is_authenticated():
        return RedirectResponse("/jira", 303)
    return RedirectResponse("/login", 303)


@app.get("/login", response_class=HTMLResponse)
async def api_login_page(request: Request):
    """Show admin login page."""
    if admin_is_authenticated():
        return RedirectResponse("/jira", 303)
    return templates.TemplateResponse(request, "login.html", {"error": None})


@app.post("/login", response_class=HTMLResponse)
async def api_login_submit(request: Request, username: str = Form(""), password: str = Form("")):
    """Process admin login - verify against Jira API."""
    if not username or not password:
        return templates.TemplateResponse(request, "login.html", {"error": "Enter username and password"})
    
    # Verify credentials against Jira
    is_valid = await jira_verify_credentials(username, password)
    if not is_valid:
        return templates.TemplateResponse(request, "login.html", {"error": "Invalid Jira credentials"})
    
    # Store credentials in memory
    admin_set_credentials(username, password)
    
    return RedirectResponse("/jira", 303)


@app.post("/logout")
async def api_logout() -> RedirectResponse:
    """Admin logout - clear credentials and lock the app."""
    admin_clear_credentials()
    return RedirectResponse("/login", 303)


@app.get("/jira", response_class=HTMLResponse)
async def api_jira_page(request: Request):
    """Show Jira story creation page (available to anyone if admin authenticated)."""
    if not admin_is_authenticated():
        return RedirectResponse("/login", 303)
    template_context = {"error": None, "project_key": JIRA_PROJECT_KEY}
    return templates.TemplateResponse(request, "jira.html", template_context)


@app.post("/jira", response_class=HTMLResponse)
async def api_jira_submit(request: Request, summary: str = Form("")):
    """Create Jira story using admin's stored credentials."""
    if not admin_is_authenticated():
        return RedirectResponse("/login", 303)
    
    story_summary = summary.strip()
    if len(story_summary) < JIRA_SUMMARY_MIN_LENGTH:
        template_context = {"error": "Summary too short", "project_key": JIRA_PROJECT_KEY}
        return templates.TemplateResponse(request, "jira.html", template_context)
    
    try:
        issue_key, browse_url = await jira_create_story(story_summary)
    except Exception as create_error:
        template_context = {"error": str(create_error), "project_key": JIRA_PROJECT_KEY}
        return templates.TemplateResponse(request, "jira.html", template_context)
    
    success_context = {"issue_key": issue_key, "browse_url": browse_url}
    return templates.TemplateResponse(request, "success.html", success_context)
