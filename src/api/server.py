from fastapi import FastAPI
from src.api import recipes, users, pkg_util, post_recipes, post_rating, pairing_suggestions, edit_steps, put_rating
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
app.include_router(post_recipes.router)
app.include_router(post_rating.router)
app.include_router(pairing_suggestions.router)
app.include_router(pkg_util.router)
app.include_router(edit_steps.router)
app.include_router(put_rating.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Recipe API. See /docs for more information."}