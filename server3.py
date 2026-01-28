"""
Jira Story Creator - Application Entrypoint

This is the entrypoint for the one-click deployment platform.
Run directly with: python server3.py
"""

from __future__ import annotations

import os

import uvicorn

from app.main import app


def main() -> None:
    """Start the Uvicorn server."""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
