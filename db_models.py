from flask_sqlalchemy import SQLAlchemy
from consts import BRANDS, brandConstDict

db = SQLAlchemy()

# DEFAULT_SHOE_IMAGE_URL = "https://www.flaticon.com/free-icon/climbing-shoes_2163125?term=climbing+shoes&page=1&position=7&origin=tag&related_id=2163125" #MIGHT NOT NEED THIS


def connect_db(app):
    """Connect to the database"""
    db.app = app
    db.init_app(app)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define the association table for the many-to-many relationship between climbing shoes and retailers
retailer_shoe_prices = db.Table(
    "retailer_shoe_prices",
    db.Column("climbing_shoe_id", db.Integer, db.ForeignKey("climbing_shoes.id"), primary_key=True),
    db.Column("retailer_id", db.Integer, db.ForeignKey("retailers.id"), primary_key=True),
    db.Column("currency", db.Integer, db.ForeignKey("retailers.currency")),
    db.Column("msrp", db.Float, nullable=False),
    db.Column("current_product_price", db.Float, nullable=False),
    db.Column("sale_or_not", db.Boolean, nullable=False),
    db.Column("sale_price", db.Float),
    db.Column("sale_pct", db.Float),
    db.Column("current_price_timestamp", db.DateTime, default=db.func.current_timestamp()),
    db.Column("sale_timestamp", db.DateTime, default=db.func.current_timestamp())
)

class DB_ClimbingShoe(db.Model):
    __tablename__ = 'climbing_shoes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    formatted_name = db.Column(db.Text, nullable=False)
    scraped_name = db.Column(db.Text, nullable=False)
    scraped_brand = db.Column(db.Text, nullable=False)
    matched_brand = db.Column(db.Text, nullable=False)
    web_url = db.Column(db.Text, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    og_price = db.Column(db.Float, nullable=False)
    sale_price = db.Column(db.Float, nullable=False)
    discount_pct = db.Column(db.Integer, nullable=False)
    
    # Define the relationship with retailers
    retailers = db.relationship("DB_Retailer", back_populates="climbing_shoes", secondary=retailer_shoe_prices, cascade="all, delete-orphan")
    
    @property
    def shoe_info(self):
        return f"{self.matched_brand} {self.scraped_name} {[retailer.name for retailer in self.retailers]}"

class DB_Retailer(db.Model):
    __tablename__ = 'retailers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(30), nullable=False)
    current_sale_boolean = db.Column(db.Boolean, nullable=False)
    sale_name = db.Column(db.Text)
    currency = db.Column(db.String(3), nullable=False)
    climbing_shoes = db.relationship('DB_ClimbingShoe', back_populates='retailers', secondary=retailer_shoe_prices)

    @property
    def friendly_date(self):
        return self.current_price_timestamp.strftime("%a %b %-d %Y, %-I:%M %p")

    @property
    def current_sale_details(self):
        if self.current_sale_boolean:
            return f"Sale: {self.sale_name}"
        else:
            return "No current sale"

    def __repr__(self):
        return f"<Retailer {self.id} | {self.name} | {self.current_sale_details} | {[shoe.scraped_name for shoe in self.climbing_shoes]}"
