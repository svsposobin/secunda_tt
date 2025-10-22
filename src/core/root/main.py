from sys import path as sys_path
from os import getcwd as os_getcwd

sys_path.append(os_getcwd())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as uvicorn_run

from src.core.root.lifespan import lifespan
from src.core.common.constants import API_DOC_METADATA
from src.core.exc.handlers import single_exception_handler

from src.domains.organizations.apis import ORGANIZATION_API_V1_ROUTER

# Models for correct app work:
from src.domains.organizations.core.models import (  # noqa
    Organizations,
    Phones,
    Buildings,
    Activities
)
from src.domains.auth.core.models import AuthKeys  # noqa

app: FastAPI = FastAPI(
    lifespan=lifespan,
    title=API_DOC_METADATA["title"],
    description=API_DOC_METADATA["description"],
    version=API_DOC_METADATA["version"]
)

# Exc handlers:
app.add_exception_handler(Exception, single_exception_handler)

# Middlewares
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        # Либо свой тестовый домен
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# Routes
app.include_router(ORGANIZATION_API_V1_ROUTER)

if __name__ == "__main__":
    uvicorn_run(app, host="0.0.0.0", port=8000)
