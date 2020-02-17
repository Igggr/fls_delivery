import requests
from app import db, FoodCategory, Meal

"""
run once.
script to populate database from sheetdb.
Only FoodCategory and Meal. 
"""

# google_url = "https://docs.google.com/spreadsheets/d/1KDo6kujf1hTPZAqZWa_A-7yEVi7qBhXi5HvBky1DhW8/edit#gid=0"
sheet_db_api = "34l849jqdx33j"
meals_url = f"https://sheetdb.io/api/v1/{sheet_db_api}/?sheet=meals"
categories_url = f"https://sheetdb.io/api/v1/{sheet_db_api}/?sheet=categories"

meals = requests.get(meals_url).json()
food_categories = requests.get(categories_url).json()

print(meals)
print(food_categories)

for ctg in food_categories:
    category = FoodCategory(title=ctg['title'], id=ctg['id'])
    db.session.add(category)

for ml in meals:
    meal = Meal(title=ml['title'], description=ml['description'], picture=ml['picture'],
                price=ml['price'], category_id=ml['category'])
    db.session.add(meal)

try:
    db.session.commit()
except:
    db.session.rollback()
