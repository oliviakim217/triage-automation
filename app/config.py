"""
Configuration - Edit these values directly.

Note: Jira username/password are NOT stored here.
Admin enters them via /login UI, verified against Jira, stored in memory (encrypted).
"""

# =============================================================================
# JIRA CONFIGURATION
# =============================================================================
# Edit these values for your setup

JIRA_BASE_URL = "https://your-actual-jira-server.com"
JIRA_PROJECT_KEY = "EQDTRG"
JIRA_ISSUE_TYPE = "Story"
JIRA_LABELS = ["created-via-app"]
JIRA_DESCRIPTION = "Created via Jira Story Creator."

# =============================================================================
# SERVICENOW CONFIGURATION (Placeholder for future use)
# =============================================================================

SN_INSTANCE_URL = ""
SN_USERNAME = ""
SN_PASSWORD = ""
SN_TABLE_NAME = "incident"
SN_DEFAULT_URGENCY = "2"
SN_DEFAULT_IMPACT = "2"
SN_DEFAULT_CATEGORY = "inquiry"

# =============================================================================
# SHARED CONSTANTS
# =============================================================================

JIRA_TIMEOUT_SECONDS = 20
SN_TIMEOUT_SECONDS = 20
ERROR_MSG_MAX_LENGTH = 500
JIRA_SUMMARY_MIN_LENGTH = 3
