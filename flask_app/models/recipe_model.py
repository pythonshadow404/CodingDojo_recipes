from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
import re

class Recipe:
    DB = "recipes"

    def __init__(self, recipe):
        self.id = recipe["id"]
        self.name = recipe["name"]
        self.description = recipe["description"]
        self.instructions = recipe["instructions"]
        self.date_made = recipe["date_made"]
        self.under_30 = recipe["under_30"]
        self.created_at = recipe["created_at"]
        self.updated_at = recipe["updated_at"]
        self.user_id = recipe["user_id"]
        self.user = None

    # CREATE VALID RECIPE
    @classmethod
    def save(cls, recipe_data): #
        # receiving data dictionary from controller in the form of request.form
        #validates data
        # Insert the recipe into the database
        query = """
        insert into recipes (name, description, instructions, date_made, under_30, user_id)
        values (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s, %(user_id)s);
        """
        connectToMySQL(cls.DB).query_db(query,recipe_data)
        # return id? or False if the validations fail

#GET ALL
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM trips;"
        results = connectToMySQL(cls.DB).query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    # GET ONE RECIPE by ID
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        return cls(results[0])
        
    # UPDATE RECIPE
    @classmethod
    def update(cls, recipe_form_data):
        # takes data dictionary from request.form
        # Updates recipe using the id in the format
        query = """UPDATE recipes
        SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, 
        date_made = %(date_made)s, under_30 = %(under_30)s
        WHERE id = %(id)s;"""
        connectToMySQL(cls.DB).query_db(query, recipe_form_data)
        #returns nothing?
    
    #DELETE RECIPE BY ID (55:35)
    @classmethod
    def delete_by_id(cls, recipe_id):
        # Delete recipe using the id
        query="""DELETE from recipes WHERE id = %(id)s"""
        data = {
            "id":recipe_id  # rmbr the dict key is the prepared statment %(var)s; the value is the argument recipe_id
        }
        connectToMySQL(cls.DB).query_db(query,data)
        
    #IS_VALID Method (validator)
    @staticmethod
    def validate_recipe(recipe_dict):
        # Set valid flag variable to True
        is_valid = True
        # No fields blank
        if len (recipe_dict["name"]) == 0:
            flash("Name is required")
            is_valid = False
        if len (recipe_dict["description"]) == 0:
            flash("Description is required")
            is_valid = False
        elif len (recipe_dict["description"]) < 3:
            flash("Description must be at least 3 characters")
            is_valid = False            
        if len (recipe_dict["instructions"]) == 0:
            flash("Instructions is required")
            is_valid = False
        elif len (recipe_dict["instructions"]) < 3:
            flash("Instructions must be at least 3 characters")
            is_valid = False
            
        if len (recipe_dict["date_made"]) == 0:
            flash("Date is required")
            is_valid = False
            
        # under 30... ?? radio buttons:??
        if "under_30" not in recipe_dict:
            flash("Recipe length is required")
            is_valid = False
            
        # At least 3 characters form description and instructions
        # Return whether valid (boolean)
        return is_valid
    



