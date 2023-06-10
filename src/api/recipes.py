import sqlalchemy
from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db

router = APIRouter()


@router.get("/recipes/{id}", tags=["recipes"])
def get_recipe(id: int):
    """
    This endpoint returns a single recipe by its identifier.
    For each recipe it returns:
    * `Recipe Name`: The name of the recipe.
    * `Cooking Time`: The overall rating of the recipe.
    * 'Servings': The total serving size of the recipe
    * `Spice Level`: The spice level of recipe.
    * 'Cooking Level': The cooking level of the recipe
    * 'Description': a short description of the recipe
    * 'Ingredients': list of all ingredients needed for recipe
    * 'Steps': list of instructions for recipe in order
    * 'User Comments': list of comments left by other users for recipe
    * 'Avg Rating': average rating for the recipe
    """

    query = """WITH steps AS (
  SELECT instructions.recipe_id,
         ARRAY_AGG(CONCAT(instructions.step_order, '. ', instructions.step_name) ORDER BY instructions.step_order) AS steps_with_order
  FROM instructions
  GROUP BY instructions.recipe_id
),
            comments AS (
              SELECT recipe_ratings.recipe_id, 
                     ARRAY_AGG(recipe_ratings.recipe_comment) AS comments
              FROM recipe_ratings
              GROUP BY recipe_ratings.recipe_id),
              
            ingre AS (
              SELECT recipe_ingredients.recipe_id, 
                     ARRAY_AGG(ingredients.name) AS ingredients
              FROM recipe_ingredients
              JOIN ingredients ON 
                    recipe_ingredients.ingredient_id = ingredients.ingredient_id
              GROUP BY recipe_ingredients.recipe_id),
              
            recipe_tags AS (
              SELECT recipe_tags.recipe_id,
                     ARRAY_AGG(tags.tag) AS tags
              FROM recipe_tags
              JOIN tags ON recipe_tags.tag_id = tags.tag_id
              GROUP BY recipe_tags.recipe_id),
            
            average_rating AS (
              SELECT recipe_id, AVG(recipe_rating) AS avg_rating
              FROM recipe_ratings
              GROUP BY recipe_id)
              
            SELECT recipe.recipe_id, recipe.recipe_name, recipe.user_id, 
                    recipe.total_time, recipe.servings, recipe.spice_level, 
                    recipe.cooking_level, recipe.recipe_type, steps.steps_with_order AS steps, 
                    comments, ingredients, average_rating.avg_rating, tags
            FROM recipes AS recipe
            JOIN steps ON steps.recipe_id = recipe.recipe_id
            LEFT JOIN comments ON comments.recipe_id = recipe.recipe_id
            JOIN ingre ON ingre.recipe_id = recipe.recipe_id
            LEFT JOIN average_rating ON average_rating.recipe_id = recipe.recipe_id
            LEFT JOIN recipe_tags ON recipe_tags.recipe_id = recipe.recipe_id
            WHERE recipe.recipe_id =:id
            """
    result = db.conn.execute(sqlalchemy.text(query), {'id': id})
    json = []
    for row in result:
        json.append({
            "Recipe Name": row.recipe_name,
            "Cooking Time": row.total_time,
            "Servings": row.servings,
            "Spice Level": row.spice_level,
            "Cooking Level": row.cooking_level,
            "Recipe Type": row.recipe_type,
            "Ingredients": row.ingredients,
            "Steps": row.steps,
            "User Comments": row.comments,
            "Avg Rating": row.avg_rating,
            "Tags": row.tags
        })
    if json == []:
        raise HTTPException(status_code=404, detail="recipe not found.")
    return json


@router.get("/findrecipes/", tags=["recipes"])
def get_recipes_by_ingredients(ingredient_list: str):
    """
    This endpoint allows a user to search for recipes based on ingredients
    they have available to them. Additionally, it automatically does substitutions
    for the recipe instructions and ingredients based on a recipe's core ingredients.
    For each matched recipe, it returns:
    * `Recipe Name`: The name of the recipe.
    * `Recipe Id`: The internal id of the recipe.
    The 'ingredient_list' parameter is used to search for recipes that contain
    desired ingredients. The order in which recipes are returned is based on
    the highest match.

    """
    ingredient_list2 = ingredient_list.split(",")
    ingredient_list2 = [ingredient.strip() for ingredient in ingredient_list2]

    query = """
    
    WITH ingredients_modified AS (
    SELECT r.recipe_id, r.recipe_name,
        ARRAY_AGG(
            CASE
                WHEN i.core_ingredient = ANY(:ingredient_list)
                    THEN i.core_ingredient
                ELSE i.name
            END
        ) AS ingredients,
        COUNT(DISTINCT CASE
            WHEN i.core_ingredient = ANY(:ingredient_list)
                THEN i.name
        END) AS num_modified_ingredients
    FROM recipes r
    JOIN recipe_ingredients ri ON r.recipe_id = ri.recipe_id
    JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
    WHERE r.recipe_id IN (
        SELECT DISTINCT recipe_id
        FROM recipe_ingredients ri
        JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
        WHERE i.core_ingredient = ANY(:ingredient_list)
    )
    GROUP BY r.recipe_id, r.recipe_name
),
recipe_ids AS (
    SELECT DISTINCT ri.recipe_id,
        (SELECT ARRAY_AGG(name) FROM unnest(ARRAY_AGG(i.name)) AS name) AS ingredient_names,
        (SELECT ARRAY_AGG(core_ingredient) FROM unnest(ARRAY_AGG(i.core_ingredient)) AS core_ingredient) AS core_ingredients
    FROM recipe_ingredients ri
    JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
    WHERE i.core_ingredient = ANY(:ingredient_list)
    GROUP BY ri.recipe_id
),
instructions_filtered AS (
    SELECT ri.recipe_id,
        ARRAY_AGG(
            CASE
                WHEN EXISTS (
                    SELECT 1
                    FROM unnest(ri.ingredient_names) AS ing_name
                    WHERE ins.step_name ILIKE '%' || ing_name || '%'
                )
                THEN (
                    SELECT REPLACE(ins.step_name, ing_name, ri.core_ingredients[array_position(ri.ingredient_names, ing_name)])
                    FROM unnest(ri.ingredient_names) AS ing_name
                    WHERE ins.step_name ILIKE '%' || ing_name || '%'
                    LIMIT 1
                )

                ELSE ins.step_name
            
            END
        ORDER BY ins.step_order
        ) AS modified_instructions
    FROM instructions ins
    JOIN recipe_ids ri ON ri.recipe_id = ins.recipe_id
    GROUP BY ri.recipe_id
    
)

SELECT
  inf.recipe_id,
  im.recipe_name,
  im.ingredients,
  inf.modified_instructions
FROM
  instructions_filtered inf
  JOIN ingredients_modified im ON im.recipe_id = inf.recipe_id
ORDER BY
  num_modified_ingredients DESC,
  recipe_id;

            """

    result = db.conn.execute(sqlalchemy.text(query),
                             {'ingredient_list': ingredient_list2})
    json = []
    for row in result:
        json.append({
            "Recipe Name": row.recipe_name,
            "Recipe Id": row.recipe_id,
            "Ingredients": row.ingredients,
            "Instructions": row.modified_instructions
        })
    if json == []:
        raise HTTPException(status_code=404, detail="Recipe not found.")
    return json



class recipe_sort_options(str, Enum):
    time = "total_time"
    spiceLevel = "spice_level"
    cookingLevel = "cooking_level"
    servings = "servings"


# Add get parameters
@router.get("/recipes/", tags=["recipes"])
def list_recipes(
        tag: str = "",
        limit: int = 50,
        offset: int = 0,
        sort: recipe_sort_options = recipe_sort_options.time):

    """
    This endpoint returns a list of recipes. For each recipe, it returns:
    * `recipe_id`: the internal id of the recipe. Can be used to query the
      `/recipes/{recipe_id}` endpoint.
    * `recipe name`: The name of the recipe.
    * `Total Time`: The overall rating of the recipe.
    * `Spice Level`: The spice level of recipe.
    * 'Cooking Level': The cooking level of the recipe
    * 'Servings': The total serving size of the recipe
    * 'Tags': The tags associated with the recipe.

    You can filter for recipes whose name contains a string by using the
    `name` query parameter.

    You can also sort the results by using the `sort` query parameter:
    * `total_time` - Sort by recipe time.
    * `spice_level` - Sort by recipe spice level.
    * `cooking_level` - Sort by recipe cooking level.
    * 'servings' - Sort by recipe servings.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """
    if sort == recipe_sort_options.time:
        order_by = db.recipes.c.total_time
    elif sort == recipe_sort_options.spiceLevel:
        order_by = db.recipes.c.spice_level
    elif sort == recipe_sort_options.cookingLevel:
        order_by = db.recipes.c.cooking_level
    elif sort == recipe_sort_options.servings:
        order_by = db.recipes.c.servings
    else:
        assert False

    stmt = (sqlalchemy.select(
        db.recipes.c.recipe_id,
        db.recipes.c.recipe_name,
        db.recipes.c.total_time,
        db.recipes.c.servings,
        db.recipes.c.spice_level,
        db.recipes.c.cooking_level)
        .limit(limit)
        .offset(offset)
        .order_by(order_by, db.recipes.c.recipe_id))

    if tag != "":
        stmt = stmt.where(db.tags.c.tag.ilike(f"%{tag}%"))
        stmt = stmt.select_from(db.recipe_tags.join(db.tags).join(db.recipes))

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        json = []
        for row in result:
            json.append(
                {
                    "recipe_id": row.recipe_id,
                    "recipe_name": row.recipe_name,
                    "total_time": row.total_time,
                    "spice_level": row.spice_level,
                    "cooking_level": row.cooking_level,
                    "servings": row.servings
                }
            )

    return json



