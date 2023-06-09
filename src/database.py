import sqlalchemy
import dotenv
import os

# DO NOT CHANGE THIS TO BE HARDCODED. ONLY PULL FROM ENVIRONMENT VARIABLES.
dotenv.load_dotenv()

def database_connection_url():
    dotenv.load_dotenv()
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"


engine = sqlalchemy.create_engine(database_connection_url())
conn = engine.connect()
metadata_obj = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata_obj,
    sqlalchemy.Column("user_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("firstname", sqlalchemy.String),
    sqlalchemy.Column("lastname", sqlalchemy.String),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String))


ingredients = sqlalchemy.Table(
    "ingredients",
    metadata_obj,
    sqlalchemy.Column("ingredient_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("core_ingredient", sqlalchemy.String))


recipes = sqlalchemy.Table(
    "recipes",
    metadata_obj,
    sqlalchemy.Column("recipe_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.user_id")),
    sqlalchemy.Column("recipe_name", sqlalchemy.String),
    sqlalchemy.Column("total_time", sqlalchemy.Integer),
    sqlalchemy.Column("servings", sqlalchemy.Integer),
    sqlalchemy.Column("spice_level", sqlalchemy.String),
    sqlalchemy.Column("cooking_level", sqlalchemy.String),
    sqlalchemy.Column("recipe_type", sqlalchemy.String))


recipe_ingredients = sqlalchemy.Table(
    "recipe_ingredients",
    metadata_obj,
    sqlalchemy.Column("recipe_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("recipes.recipe_id"), primary_key=True),
    sqlalchemy.Column("ingredient_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("ingredients.ingredient_id"), primary_key=True),
    sqlalchemy.Column("quantity", sqlalchemy.Float),
    sqlalchemy.Column("measurements", sqlalchemy.String))

recipe_rating= sqlalchemy.Table(
    "recipe_ratings",
    metadata_obj,
    sqlalchemy.Column("rating_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("recipe_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("recipes.recipe_id")),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.user_id")),
    sqlalchemy.Column("recipe_rating", sqlalchemy.Float),
    sqlalchemy.Column("recipe_comment", sqlalchemy.String),
    sqlalchemy.Column("time_stamp", sqlalchemy.DateTime))

instructions = sqlalchemy.Table(
    "instructions",
    metadata_obj,
    sqlalchemy.Column("instruction_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("recipe_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("recipes.recipe_id")),
    sqlalchemy.Column("step_order", sqlalchemy.Integer),
    sqlalchemy.Column("step_name", sqlalchemy.String))

tags = sqlalchemy.Table(
    "tags",
    metadata_obj,
    sqlalchemy.Column("tag_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("tag", sqlalchemy.String))

recipe_tags = sqlalchemy.Table(
    "recipe_tags",
    metadata_obj,
    sqlalchemy.Column("tag_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("tags.tag_id"), primary_key=True),
    sqlalchemy.Column("recipe_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("recipes.recipe_id"), primary_key=True),
    sqlalchemy.Column("tag", sqlalchemy.String))



# recipes = sqlalchemy.Table("recipes", metadata_obj, autoload_with=engine)
# ingredients = sqlalchemy.Table("ingredients", metadata_obj, autoload_with=engine)
# recipe_ingredients = sqlalchemy.Table("recipe_ingredients", metadata_obj, autoload_with=engine)
# instructions = sqlalchemy.Table("instructions", metadata_obj, autoload_with=engine)
# users = sqlalchemy.Table("users", metadata_obj, autoload_with=engine)
# tags = sqlalchemy.Table("tags", metadata_obj, autoload_with=engine)
# recipe_tags = sqlalchemy.Table("recipe_tags", metadata_obj, autoload_with=engine)
# recipe_rating = sqlalchemy.Table("recipe_ratings", metadata_obj, autoload_with=engine)
