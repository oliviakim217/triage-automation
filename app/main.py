"""
FastAPI app with /login and /jira routes.
"""

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.auth import auth_verify_credentials
from app.config import JIRA_PROJECT_KEY, JIRA_SUMMARY_MIN_LENGTH
from app.jira_client import jira_create_story
from app.session import session_is_logged_in, session_set_logged_in, session_clear

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def api_home(request: Request) -> RedirectResponse:
    """Redirect to /jira if logged in, else /login."""
    if session_is_logged_in(request):
        return RedirectResponse("/jira", 303)
    return RedirectResponse("/login", 303)


@app.get("/login", response_class=HTMLResponse)
async def api_login_page(request: Request):
    """Show login page."""
    if session_is_logged_in(request):
        return RedirectResponse("/jira", 303)
    return templates.TemplateResponse(request, "login.html", {"error": None})


@app.post("/login", response_class=HTMLResponse)
async def api_login_submit(request: Request, username: str = Form(""), password: str = Form("")):
    """Process login form."""
    if not username or not password:
        return templates.TemplateResponse(request, "login.html", {"error": "Enter username and password"})
    
    if not auth_verify_credentials(username, password):
        return templates.TemplateResponse(request, "login.html", {"error": "Invalid credentials"})
    
    login_response = RedirectResponse("/jira", 303)
    session_set_logged_in(login_response)
    return login_response


@app.post("/logout")
async def api_logout() -> RedirectResponse:
    """Log out and redirect to login."""
    logout_response = RedirectResponse("/login", 303)
    session_clear(logout_response)
    return logout_response


@app.get("/jira", response_class=HTMLResponse)
async def api_jira_page(request: Request):
    """Show Jira story creation page."""
    if not session_is_logged_in(request):
        return RedirectResponse("/login", 303)
    template_context = {"error": None, "project_key": JIRA_PROJECT_KEY}
    return templates.TemplateResponse(request, "jira.html", template_context)


@app.post("/jira", response_class=HTMLResponse)
async def api_jira_submit(request: Request, summary: str = Form("")):
    """Create Jira story from form submission."""
    if not session_is_logged_in(request):
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
