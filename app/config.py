"""
Configuration - Loads from environment variables.

Copy .env.example to .env and fill in your values.
"""

import os

# =============================================================================
# AUTH - Login Credentials
# =============================================================================
# Password is bcrypt hashed. To generate:
#   python -c "import bcrypt; print(bcrypt.hashpw(b'your-password', bcrypt.gensalt()).decode())"

AUTH_USERNAME = os.getenv("AUTH_USERNAME", "admin")
AUTH_PASSWORD_HASH = os.getenv("AUTH_PASSWORD_HASH", "")

# =============================================================================
# SESSION
# =============================================================================
# Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"

SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "")
SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", "session")
SESSION_MAX_AGE_SECONDS = int(os.getenv("SESSION_MAX_AGE_SECONDS", "3600"))

# =============================================================================
# JIRA - Atlassian Jira Configuration
# =============================================================================

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", "")
JIRA_EMAIL = os.getenv("JIRA_EMAIL", "")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "")
JIRA_ISSUE_TYPE = os.getenv("JIRA_ISSUE_TYPE", "Story")
JIRA_LABELS = os.getenv("JIRA_LABELS", "created-via-app").split(",")
JIRA_DESCRIPTION = os.getenv("JIRA_DESCRIPTION", "Created via Jira Story Creator.")

# =============================================================================
# SERVICENOW (SN) - ServiceNow Configuration
# =============================================================================

SN_INSTANCE_URL = os.getenv("SN_INSTANCE_URL", "")
SN_USERNAME = os.getenv("SN_USERNAME", "")
SN_PASSWORD = os.getenv("SN_PASSWORD", "")
SN_TABLE_NAME = os.getenv("SN_TABLE_NAME", "incident")

# Default values for ServiceNow records
SN_DEFAULT_URGENCY = os.getenv("SN_DEFAULT_URGENCY", "2")
SN_DEFAULT_IMPACT = os.getenv("SN_DEFAULT_IMPACT", "2")
SN_DEFAULT_CATEGORY = os.getenv("SN_DEFAULT_CATEGORY", "inquiry")

# =============================================================================
# SHARED CONSTANTS
# =============================================================================

JIRA_TIMEOUT_SECONDS = int(os.getenv("JIRA_TIMEOUT_SECONDS", "20"))
SN_TIMEOUT_SECONDS = int(os.getenv("SN_TIMEOUT_SECONDS", "20"))
ERROR_MSG_MAX_LENGTH = 500
JIRA_SUMMARY_MIN_LENGTH = 3
