import os
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from helpers import split_dict, stringify, lookup, readable_list
import requests
import random
import string
import json

# Configure app
app = Flask(__name__)

# Set API key and ID
os.environ['API_KEY'] = '51bc41f2ca1657d3ee7e76e0e360ba85'
os.environ['API_ID'] = '910f2a02'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem instead of signed cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'
app.config['SESSION_FILE_THRESHOLD'] = 100
Session(app)

# Make sure API_KEY and API_ID are set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")
elif not os.environ.get("API_ID"):
    raise RuntimeError("API_ID not set")

@app.after_request
def after_request(response):
    # Ensure responses aren't cached
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Dictionaries ############################################################


dietlabels = {
    "balanced": "Balanced",
    "high-fiber": "High Fiber",
    "high-protein": "High Protein",
    "low-carb": "Low Carb",
    "low-fat": "Low Fat",
    "low-sodium": "Low Sodium",
}

healthlabels = {
    "pescatarian": "Pescatarian",
    "shellfish-free": "Shellfish-Free",
    "alcohol-free": "Alcohol-Free",
    "celery-free": "Celery-Free",
    "soy-free": "Soy-Free",
    "sugar-free": "Sugar-Free",
    "pork-free": "Pork-Free",
    "red-meat-free": "Red-Meat-Free",
    "sesame-free": "Sesame-Free",
    "sulfite-free": "Sulfite-Free",
    "tree-nut-free": "Tree-Nut-Free",
    "vegan": "Vegan",
    "sugar-conscious": "Sugar-Conscious",
    "vegetarian": "Vegetarian",
    "wheat-free": "Wheat-Free",
    "alcohol-cocktail": "Alcohol-Cocktail",
    "crustacean-free": "Crustacean-Free",
    "dairy-free": "Dairy-Free",
    "lupine-free": "Lupine-Free",
    "mediterranean": "Mediterranean",
    "dash": "DASH",
    "kidney-friendly": "Kidney-Friendly",
    "egg-free": "Egg-Free",
    "fish-free": "Fish-Free",
    "fodmap-free": "FODMAP-Free",
    "gluten-free": "Gluten-Free",
    "mollusk-free": "Mollusk-Free",
    "peanut-free": "Peanut-Free",
    "immuno-supportive": "Immuno-Supportive",
    "keto-friendly": "Keto-Friendly",
    "low-sugar": "Low-Sugar",
    "mustard-free": "Mustard-Free",
    "kosher": "Kosher",
    "low-potassium": "Low-Potassium",
    "no-oil-added": "No oil added",
    "paleo": "Paleo",
}

cuisinetype = {
    "chinese": "Chinese",
    "eastern europe": "Eastern Europe",
    "british": "British",
    "caribbean": "Caribbean",
    "asian": "Asian",
    "central europe": "Central Europe",
    "american": "American",
    "french": "French",
    "kosher": "Kosher",
    "indian": "Indian",
    "korean": "Korean",
    "italian": "Italian",
    "greek": "Greek",
    "japanese": "Japanese",
    "mediterranean": "Mediterranean",
    "south east asian": "South East Asian",
    "mexican": "Mexican",
    "south american": "South American",
    "world": "World",
    "nordic": "Nordic",
    "middle eastern": "Middle Eastern",
}

dishtype = {
    "starter": "Starter",
    "main course": "Main Course",
    "side dish": "Side Dish",
    "drinks": "Drinks",
    "desserts": "Desserts",
    # 'alcohol cocktail': 'Alcohol Cocktail',
    # 'biscuits and cookies': 'Biscuit and Cookies',
    # 'bread': 'Bread',
    # 'cereals': 'Cereals',
    # 'condiments and sauces': 'Condiments and Sauces',
    # 'desserts': 'Desserts',
    # 'drinks': 'Drinks',
    # 'egg': 'Egg',
    # 'ice cream and custard': 'Ice Cream and Custard',
    # 'main course': 'Main Course',
    # 'pancake': 'Pancake',
    # 'pasta': 'Pasta',
    # 'pastry': 'Pastry',
    # 'pies and tarts': 'Pies and Tarts',
    # 'pizza': 'Pizza',
    # 'preps': 'Preps',
    # 'preserve': 'Preserve',
    # 'salad': 'Salad',
    # 'sandwiches': 'Sandwiches',
    # 'seafood': 'Seafood',
    # 'side dish': 'Side Dish',
    # 'soup': 'Soup',
    # 'special occasions': 'Special Occasions',
    # 'starter': 'Starter',
    # 'sweets': 'Sweets'
}

# Routes ##################################################################

@app.route("/")
def index():
    hl = split_dict(healthlabels, 3)
    ct = split_dict(cuisinetype, 3)
    return render_template("index.html", dietlabels=dietlabels, hl=hl, len_hl=len(hl), ct=ct, len_ct=len(ct), dishtype=dishtype)

@app.route("/result")
def result():
    i_list = request.args.getlist("ingredients")
    # Remove empty values (if any) with list comprehension
    ingredients_list = [i.lower().strip() for i in (filter(None, i_list))]
    ingredients = str(",".join(ingredients_list))
    # Make ingredients readable for result page's headline
    readable_ingredients = readable_list(ingredients_list)

    dishType = stringify("dishType", "&dishType=")
    dietLabels = stringify("dietLabels", "&diet=")
    healthLabels = stringify("healthLabels", "&health=")
    cuisineType = stringify("cuisineType", "&cuisineType=")
    # Concat all parameters
    param = "".join(ingredients + dishType[1] + dietLabels[1] + healthLabels[1] + cuisineType[1])
    # Make API request
    recipes_list = lookup(param)
    saved_recipes_link = session.get("bookmarks", [])

    return render_template("result.html", recipe=result, readable_ingredients=readable_ingredients, recipes_list=recipes_list, dish_list=dishType[0], diet_list=dietLabels[0], health_list=healthLabels[0], cuisine_list=cuisineType[0], saved_recipes_link=saved_recipes_link, dishtype=dishtype)

@app.route("/add", methods=["POST"])
def add():
    # String
    url = request.form["link"]
    label = request.form.get("label")
    image = request.form.get("image")
    source = request.form.get("source")
    url = request.form.get("url")
    calories = request.form.get("calories")
    totalTime = request.form.get("totalTime")
    # List
    dishType = request.form.get("dishType").strip("[]").strip(",")
    dietLabels = request.form.get("dietLabels").strip("[]").strip(",")
    healthLabels = request.form.get("healthLabels").strip("[]").strip(",")
    cuisineType = request.form.get("cuisineType").strip("[]").strip(",")
    ingredientLines = request.form.get("ingredientLines").strip("[]")

    recipe_info = {
        'link': url,
        'label': label,
        'image': image,
        'source': source,
        'url': url,
        'calories': calories,
        'totalTime': totalTime,
        'dishType': dishType,
        'dietLabels': dietLabels,
        'healthLabels': healthLabels,
        'cuisineType': cuisineType,
        'ingredientLines': ingredientLines
    }

    # Save to session
    saved_recipes_link = session.get("bookmarks", [])
    saved_recipes_link.append(recipe_info)
    session["bookmarks"] = saved_recipes_link

    return redirect("/bookmarks")


@app.route("/bookmarks")
def bookmarks():
    saved_recipes = session.get("bookmarks", [])
    saved_recipes_list = []
    saved_recipes_list = saved_recipes

    return render_template("bookmarks.html", saved_recipes_list=saved_recipes_list, dishtype=dishtype)


@app.route("/remove", methods=["POST"])
def remove():
    link = request.form["link"]
    saved_recipes = session.get("bookmarks", [])

    # Remove any items that have the same link or are not dictionaries
    saved_recipes = [saved_recipe for saved_recipe in saved_recipes if not (isinstance(saved_recipe, dict) and saved_recipe.get("link") == link)]

    session["bookmarks"] = saved_recipes
    return redirect("/bookmarks")

@app.route("/caloric_needs")
def caloric_needs():
    age = int(request.args.get("age"))
    weight = float(request.args.get("weight"))
    height = float(request.args.get("height"))
    activity = float(request.args.get("activity"))
    gender = request.args.get("gender")

    # Calculate BMR using the Mifflin-St Jeor equation
    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Calculate daily caloric needs
    daily_caloric_needs = round(bmr * activity)

    return render_template("caloric_needs.html", daily_caloric_needs=daily_caloric_needs, gender=gender)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/bookmarks_icon')
def bookmarks_icon():
    return render_template('bookmarks.html')

if __name__ == "__main__":
    app.run(debug=True)
