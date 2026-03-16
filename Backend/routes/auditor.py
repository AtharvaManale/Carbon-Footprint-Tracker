from flask import session, request, jsonify, Blueprint
from Backend.extensions import db
from Backend.models.models import users, daily_emissions, sales_data, products
from datetime import date, timedelta

auditor = Blueprint("auditor", __name__)

@auditor.route("/vendors", methods = ["GET"])
def panel():
    if "user_id" in session:
        if session["role"] == "auditor":
            vendors = users.query.filter_by(role = "vendor").all()
            vendors_data = []
            for vendor in vendors:
                vendors_data.append({"vendor": vendor.username,
                                     "shop": vendor.shop_name,
                                     "end": vendor.ending_at})
        
            return jsonify({"message":"Vendors data for dashboard!",
                           "vendors": vendors_data }), 200
        
        return jsonify({"error": "Only auditors can access this panel!"}), 403
    
    return jsonify("Not logged in!"), 401

@auditor.route("/sales/<int:id>", methods = ["GET"])
def vendors_sales_data(id):
    if "user_id" in session:
        if session["role"] == "auditor":
            limit_date = date.today() - timedelta(days=7)
            sales = sales_data.query.filter(sales_data.vendor_id == id, sales_data.sales_date >= limit_date).all()

            data = {}

            for sale in sales:
                sdate = sale.sales_date.strftime("%d-%m-%Y")
                product = products.query.get(sale.product_id)
                if sdate not in data:
                    data[sdate] = []

                data[sdate].append({
                    "product":product.name,
                    "quantity":sale.quantity
                })

            emissions = daily_emissions.query.filter(daily_emissions.vendor_id == id, daily_emissions.sales_date >= limit_date)

            daily_emissions_data = []

            for emission in emissions:
                edate = emission.sale_date.strftime("%d-%m-%Y")
                daily_emissions_data.append({edate : emission.total_co2})

            return jsonify({"message":"sales of last 7 days!",
                        "sales": data,
                        "daily_emissions": daily_emissions_data}), 200
        
        return jsonify({"error": "Only auditors can access this panel!"}), 403

    return jsonify("Not logged in!"), 401
