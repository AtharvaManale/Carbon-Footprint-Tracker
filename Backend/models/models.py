from Backend.extensions import db
from datetime import datetime, date
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import Numeric

class vendors(db.Model):
    vendor_id = db.Collumn(db.Integer, primary_key = True, autoincrement = True)
    username = db.Collumn(db.String(100), nullable = False)
    password = db.Collumn(db.String(255), nullable = False)
    auditor = db.column(db.Boolean, default = False, nullable = False)
    created_at = db.Collumn(db.DateTime, default = datetime.now())

    def create_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    

class sales_data(db.Model):
    sales_id = db.Collumn(db.Integer, primary_key = True, autoincrement = True)
    vendor_id = db.Collumn(db.Integer, db.ForeignKey("vendors.vendor_id"), nullable=False)
    product_category = db.Collumn(db.String(100), nullable = False)
    quantity = db.Collumn(db.Integer, nullable = True)
    sales_date = db.Collumn(db.Date, default = date.now())

class daily_emissions(db.Model):
    emission_id = db.Collumn(db.Integer, primary_key = True, autoincrement = True)
    vendor_id = db.Collumn(db.Integer, db.ForeignKey("vendors.vendor_id"), nullable=False)
    total_co2 = db.Collumn(Numeric(5,2), nullable = False)
    sales_date = db.Collumn(db.Date, nullable = False)