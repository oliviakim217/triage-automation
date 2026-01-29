"""
Configuration - Loads from environment variables.

Copy .env.example to .env and fill in your values.

Note: Jira username/password are NOT stored here.
Admin enters them via /login, verified against Jira, stored in memory.
"""

import os

# =============================================================================
# JIRA - Jira Configuration
# =============================================================================
# Admin credentials are entered via UI and stored in memory (not here)

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", "")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "")
JIRA_ISSUE_TYPE = os.getenv("JIRA_ISSUE_TYPE", "Story")
JIRA_LABELS = os.getenv("JIRA_LABELS", "created-via-app").split(",")
JIRA_DESCRIPTION = os.getenv("JIRA_DESCRIPTION", "Created via Jira Story Creator.")

# =============================================================================
# SERVICENOW (SN) - ServiceNow Configuration (Placeholder)
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
