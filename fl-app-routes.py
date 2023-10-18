"""Blogly application."""
from flask import Flask, url_for, request, render_template, redirect, flash, session, jsonify
from db_models import db, connect_db, DB_ClimbingShoe, DB_Retailer, RetailerShoePrices
from flask_config import SQLALCHEMY_DATABASE_URI, SECRET_KEY, SQLALCHEMY_TRACK_MODIFICATIONS, SQLALCHEMY_ECHO

app = Flask(__name__)

# Load the configuration settings from the config.py file
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_ECHO'] = SQLALCHEMY_ECHO

connect_db(app)

@app.route('/')
def home():
    """home view with posts"""
    
    shoes = DB_ClimbingShoe.query.order_by(DB_ClimbingShoe.brand, DB_ClimbingShoe.name).all()
    retailers = DB_Retailer.query.order_by(DB_Retailer.name).all()
    retailers_and_shoes
    response = {
        shoes: shoes
        }
    print(shoes)
    return jsonify(response)

@app.route()

@app.route('/retailers_and_shoes')
def retailers_and_shoes():
    # Perform an inner join to get retailers and their climbing shoes
    retailers_with_shoes = db.session.query(DB_Retailer, DB_ClimbingShoe).join(RetailerShoePrices).filter(RetailerShoePrices.climbing_shoe_id == DB_ClimbingShoe.id).all()

    return jsonify(retailers_with_shoes)

@app.route('/seed_db')
def seed_db():
    """seed db with seed_blog.py"""
        # Create all tables
    db.drop_all()
    db.create_all()

    # If table isn't empty, empty it
    DB_ClimbingShoe.query.delete()
    DB_Retailer.query.delete()
    RetailerShoePrices.query.delete()

    # Create some retailers
    retailer1 = DB_Retailer(name="Retailer1", country="Country1", currency="USD", current_sale_boolean=True, sale_name="Sale1")
    retailer2 = DB_Retailer(name="Retailer2", country="Country2", currency="CAD", current_sale_boolean=False, sale_name=None)
    retailer3 = DB_Retailer(name="Retailer3", country="Country3", currency="EUR", current_sale_boolean=True, sale_name="Sale3")

    # Create some climbing shoes
    shoe1 = DB_ClimbingShoe(formatted_name="Shoe1", scraped_name="Shoe One", scraped_brand="Brand1", matched_brand="Brand1", web_url="URL1", gender="M", og_rice=100.0, sale_price=80.0, discount_pct=20)
    shoe2 = DB_ClimbingShoe(formatted_name="Shoe2", scraped_name="Shoe Two", scraped_brand="Brand2", matched_brand="Brand2", web_url="URL2", gender="F", og_rice=90.0, sale_price=70.0, discount_pct=22)
    shoe3 = DB_ClimbingShoe(formatted_name="Shoe3", scraped_name="Shoe Three", scraped_brand="Brand3", matched_brand="Brand3", web_url="URL3", gender="M", og_rice=110.0, sale_price=88.0, discount_pct=20)

    # Create retailer-shoe price entries
    price1 = RetailerShoePrices(retailer=retailer1, climbing_shoe=shoe1, msrp=100.0, current_product_price=80.0, sale_or_not=True, sale_price=80.0, sale_pct=20)
    price2 = RetailerShoePrices(retailer=retailer1, climbing_shoe=shoe2, msrp=90.0, current_product_price=70.0, sale_or_not=True, sale_price=70.0, sale_pct=22)
    price3 = RetailerShoePrices(retailer=retailer2, climbing_shoe=shoe1, msrp=100.0, current_product_price=80.0, sale_or_not=True, sale_price=80.0, sale_pct=20)
    price4 = RetailerShoePrices(retailer=retailer2, climbing_shoe=shoe3, msrp=110.0, current_product_price=88.0, sale_or_not=True, sale_price=88.0, sale_pct=20)
    price5 = RetailerShoePrices(retailer=retailer3, climbing_shoe=shoe2, msrp=90.0, current_product_price=70.0, sale_or_not=True, sale_price=70.0, sale_pct=22)
    price6 = RetailerShoePrices(retailer=retailer3, climbing_shoe=shoe3, msrp=110.0, current_product_price=88.0, sale_or_not=True, sale_price=88.0, sale_pct=20)

    # Add objects to the database session
    db.session.add(retailer1)
    db.session.add(retailer2)
    db.session.add(retailer3)
    db.session.add(shoe1)
    db.session.add(shoe2)
    db.session.add(shoe3)
    db.session.add(price1)
    db.session.add(price2)
    db.session.add(price3)
    db.session.add(price4)
    db.session.add(price5)
    db.session.add(price6)

    # Commit the changes to the database
    db.session.commit()
    
    return redirect(url_for('home')) 

########################################################################################################################
# RUN APP 

if __name__ == '__main__':
    app.run()