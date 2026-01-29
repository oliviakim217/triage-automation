"""
Jira Story Creator - Application Entrypoint

"""

from __future__ import annotations

import os

from dotenv import load_dotenv
import uvicorn

# Load .env file before importing app (which reads config)
load_dotenv()

from app.main import app  # noqa: E402


def main() -> None:
    """Start the Uvicorn server."""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
