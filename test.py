from Backend.models.models import users
from Backend import create_app
from Backend.extensions import db
from Backend.models.models import sales_data, products,daily_emissions
from datetime import date, timedelta
app = create_app()

