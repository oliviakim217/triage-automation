"""
ServiceNow API client (placeholder).

Naming convention:
- Functions: sn_* (e.g., sn_create_incident, sn_fetch_records)
- Constants: SN_* (in config.py)
"""

import httpx

from app.config import (
    SN_INSTANCE_URL,
    SN_USERNAME,
    SN_PASSWORD,
    SN_TABLE_NAME,
    SN_DEFAULT_URGENCY,
    SN_DEFAULT_IMPACT,
    SN_DEFAULT_CATEGORY,
    SN_TIMEOUT_SECONDS,
    ERROR_MSG_MAX_LENGTH,
)


def _sn_get_auth_credentials() -> tuple[str, str]:
    """Return (username, password) for Basic Auth."""
    return (SN_USERNAME, SN_PASSWORD)


async def sn_create_incident(
    short_description: str,
    description: str = "",
) -> tuple[str, str]:
    """
    Create a ServiceNow incident.
    
    Returns (incident_number, incident_url).
    Raises RuntimeError on failure.
    """
    sn_api_url = f"{SN_INSTANCE_URL}/api/now/table/{SN_TABLE_NAME}"
    
    request_payload = {
        "short_description": short_description,
        "description": description,
        "urgency": SN_DEFAULT_URGENCY,
        "impact": SN_DEFAULT_IMPACT,
        "category": SN_DEFAULT_CATEGORY,
    }

    request_headers = {"Content-Type": "application/json", "Accept": "application/json"}

    async with httpx.AsyncClient(timeout=SN_TIMEOUT_SECONDS) as http_client:
        response = await http_client.post(
            sn_api_url,
            auth=_sn_get_auth_credentials(),
            json=request_payload,
            headers=request_headers,
        )
        
        if response.status_code >= 400:
            error_detail = response.text[:ERROR_MSG_MAX_LENGTH]
            raise RuntimeError(f"ServiceNow error: {error_detail}")
        
        response_data = response.json().get("result", {})
        incident_number = response_data.get("number")
        incident_sys_id = response_data.get("sys_id")
        
        if not incident_number:
            raise RuntimeError("No incident number returned")

    incident_url = f"{SN_INSTANCE_URL}/nav_to.do?uri=incident.do?sys_id={incident_sys_id}"
    return incident_number, incident_url


async def sn_fetch_incident(incident_number: str) -> dict:
    """
    Fetch an incident by number.
    
    Returns incident data as dict.
    Raises RuntimeError on failure.
    """
    sn_api_url = f"{SN_INSTANCE_URL}/api/now/table/{SN_TABLE_NAME}"
    query_params = {"sysparm_query": f"number={incident_number}", "sysparm_limit": "1"}
    request_headers = {"Accept": "application/json"}

    async with httpx.AsyncClient(timeout=SN_TIMEOUT_SECONDS) as http_client:
        response = await http_client.get(
            sn_api_url,
            auth=_sn_get_auth_credentials(),
            params=query_params,
            headers=request_headers,
        )
        
        if response.status_code >= 400:
            error_detail = response.text[:ERROR_MSG_MAX_LENGTH]
            raise RuntimeError(f"ServiceNow error: {error_detail}")
        
        response_results = response.json().get("result", [])
        if not response_results:
            raise RuntimeError(f"Incident {incident_number} not found")
        
        return response_results[0]
