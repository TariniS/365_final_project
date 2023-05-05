from fastapi import FastAPI
from src.api import recipes, users, pkg_util
description = """
Add description about recipes API
"""
tags_metadata = [
    {
        "name": "recipes",
        "description": "Access information about recipes.",
    },
{
        "name": "users",
        "description": "Access information about recipes.",
    }
]

app = FastAPI(
    title="Recipe API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Sameera Balijepalli and Tarini Srikanth",
        "email": "sbalijep@calpoly.edu",
    },
    openapi_tags=tags_metadata,
)
app.include_router(recipes.router)
app.include_router(users.router)
app.include_router(pkg_util.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Recipe API. See /docs for more information."}
