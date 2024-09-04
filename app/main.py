"""
The main file for FastAPI app.

- /stations/... coverred by routers.stations module

"""

from typing import Dict, Any
from fastapi import FastAPI
import routers.stations


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
            Dict[str, Any]: _description_
        """
        return {"message": "home page"}

    return main_app


app = create_app()
