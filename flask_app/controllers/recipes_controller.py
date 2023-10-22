from flask import Flask, render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe

#from flask_app.models.recipe import Recipe


######## GET ROUTES ########

# Render Page Details Page for One Recipe
@app.route('/recipes/<recipe_id>')
def recipe_details(recipe_id):
    print("In details: ", recipe_id)
    # Need to get that recipe from the database
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    recipe = Recipe.get_one_by_id(recipe_id)
    # Pass recipe into template
    return render_template('recipe_detail.html', recipe = recipe)

# Render Page with Create Form
@app.route('/recipes/new')
def create_page():
    print("In create route: ")
    data ={
        "id":session['user_id']
    }
    user_id = User.get_by_id(data)
    return render_template('create_recipe.html')

# Render Page with Edit Form
@app.route('/recipes/edit/<recipe_id>')
def edit_page(recipe_id):
    print("In edit page: ", recipe_id)
    # Need to get that recipe from the database
    recipe = Recipe.get_one_by_id(recipe_id)
    # Pass recipe into template
    return render_template('edit_recipe.html', recipe = recipe)

# GET Action Routes:
#    Delete Route (GET request)
@app.route('/recipes/delete/<recipe_id>')
def delete_recipe(recipe_id):
    print("In delete page: ", recipe_id)
    #call delete method
    Recipe.delete_by_id(recipe_id)
    return redirect('/recipes')

########## POST Routes ############

# CREATE (Process form)
@app.route('/recipes', methods =['POST'])
def create_recipe():
    print("In the create process POST route: ", request.form)
    # Before we save...the information
    # Pass the form data into a validator (55:00)
    is_valid = Recipe.validate_recipe(request.form)
    print('#############################')
    print(is_valid)
    # If the form info data is good... then save and go to the dashboard
    if is_valid:
        Recipe.save(request.form)
        return redirect('/recipes')
    # else -- redirect tothe new page to show errors to users for correction.
    return redirect('/recipes/new')

# UPDATE (Process form)
@app.route('/recipes', methods =['POST'])
def update_recipe():
    print("In update POST route: ", request.form)
    is_valid = Recipe.validate_recipe(request.form)
    # If the form info data is good... then save and go to the dashboard
    if is_valid:
        Recipe.update(request.form)
        return redirect('/recipes')
    return redirect(f"/recipes/edit/{request.form['id']}")

