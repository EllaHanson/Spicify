from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from . import profile
from . import recipe
from . import update_profile
from . import favorites
from . import rating
from . import comments
import json
import logging
import sys
from starlette.middleware.cors import CORSMiddleware

description = """
Best recipe blog
"""

app = FastAPI(
    title="Spicify",
    description=description,
    version="0.0.1",
    
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Ella Hanson",
        "email": "ellahanson.126@gmail.com",
    },
)

origins = ["https://potion-exchange.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(profile.router)
app.include_router(recipe.router)
app.include_router(update_profile.router)
app.include_router(favorites.router)
app.include_router(rating.router)
app.include_router(comments.router)


@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)

@app.get("/")
async def root():
    return {"message": "Welcome to Spicify."}
