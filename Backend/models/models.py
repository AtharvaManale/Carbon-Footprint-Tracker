from Backend.extensions import db
from datetime import datetime, date
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import Numeric


class users(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(255), nullable = False)
    shop_name = db.Column(db.String(100))
    role = db.Column(db.String(50), default = "vendor")
    created_at = db.Column(db.DateTime, default = datetime.utcnow)

    def create_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
class products(db.Model):
    product_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(200))
    emission_factor = db.Collumn(db.Float)

class sales_data(db.Model):
    sales_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    vendor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id= db.Column(db.Integer, db.ForeignKey("products.product_id"))
    quantity = db.Column(db.Integer, nullable = True)
    sales_date = db.Collumn(db.Date, default = date.today)

class daily_emissions(db.Model):
    emission_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    vendor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    total_co2 = db.Column(Numeric(5,2), nullable = False)
    sales_date = db.Column(db.Date, default = date.today)