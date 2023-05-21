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
recipes = sqlalchemy.Table("recipes", metadata_obj, autoload_with=engine)
ingredients = sqlalchemy.Table("ingredients", metadata_obj, autoload_with=engine)
recipe_ingredients = sqlalchemy.Table("recipe_ingredients", metadata_obj, autoload_with=engine)
instructions = sqlalchemy.Table("instructions", metadata_obj, autoload_with=engine)
users = sqlalchemy.Table("users", metadata_obj, autoload_with=engine)
tags = sqlalchemy.Table("tags", metadata_obj, autoload_with=engine)
recipe_tags = sqlalchemy.Table("recipe_tags", metadata_obj, autoload_with=engine)
recipe_rating = sqlalchemy.Table("recipe_ratings", metadata_obj, autoload_with=engine)
