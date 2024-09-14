"""
The main module for the FastAPI application.

This module creates and configures the FastAPI app instance, including:
- Defining the root endpoint ("/") which returns a simple welcome message
- Including the router for the "/stations" endpoints from the `routers.stations` module

The FastAPI app instance is created using the `create_app()` function and assigned to the `app` variable.
"""

from typing import Dict, Any
from fastapi import FastAPI
import routers.stations  # pylint: disable=E0401


def create_app() -> FastAPI:
    """
    Create and configure a FastAPI app instance.

    Returns:
        FastAPI: The configured FastAPI app instance.
    """
    main_app = FastAPI()
    main_app.include_router(routers.stations.router_station)

    @main_app.get("/")
    async def main() -> Dict[str, Any]:
        """The root endpoint; Currently returns a simple message

        Returns:
            Dict[str, Any]: JSON object to return
        """
        return {"message": "Home page for Park Info project"}

    return main_app


app = create_app()
