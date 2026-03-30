from flask import session, jsonify, request, Blueprint
from Backend.models.models import sales_data, products
from Backend.extensions import db
from datetime import date, timedelta

sales = Blueprint("sales", __name__)

@sales.route('/products', methods = ['GET'])
def get_products():
    if "user_id" in session:
        Products = products.query.all()
        return jsonify({"Products": [{
                                        "Product_id": product.product_id, 
                                        "Product_name": product.name
                                      } 
                                    for product in Products
                                ]}), 200
    return jsonify("Not logged in!"), 401

@sales.route('/add', methods = ['POST', 'PUT'])
def add_sales():
    if "user_id" in session:
        if session["user_role"] == "vendor":
            data = request.json

            product_name = data.get('product') #can be name or id depends on android input
            quantity = data.get('quantity')

            product = products.query.filter_by(name = product_name).first()
            today = date.today()
            
            if not product:
                return jsonify({"error": "Selected product is not available to measure!"}), 404

            sale = sales_data.query.filter_by(product_id = product.product_id, vendor_id = session['user_id'], sales_date = today).first()

            if sale:
                sale.quantity += quantity
                db.session.commit()

                return jsonify({"message" : "Sales updated successfully!",
                               "updated_quantity": sale.quantity}), 202
            
            new_sale = sales_data(
                vendor_id = session["user_id"],
                product_id = product.product_id,
                quantity = quantity,
                sales_date = today
            )

            db.session.add(new_sale)
            db.session.commit()

            return jsonify({"message":"new sale added successfully!"}), 201
        
        return jsonify({"error": "Only vendors can add or update sale!"}), 403
    
    return jsonify("Not logged in!"), 401

@sales.route('/update', methods=['PUT'])
def update_sale():
    if "user_id" in session and session["user_role"] == "vendor":
        data = request.json

        product_name = data.get("product")
        quantity = data.get("quantity")
        today = date.today()

        product = products.query.filter_by(name=product_name).first()
        if not product:
            return jsonify({"error": "Invalid product"}), 400

        sale = sales_data.query.filter_by(
            vendor_id=session["user_id"],
            product_id=product.product_id,
            sales_date=today
        ).first()

        if not sale:
            return jsonify({"error": "No existing sale found"}), 404

        sale.quantity = quantity

        db.session.commit()

        return jsonify({"message": "Sale updated successfully!"}), 200

    return jsonify({"error": "Unauthorized"}), 401

@sales.route('/data', methods = ['GET'])
def salesdata():
    if "user_id" in session:
        data = {}
        last_7days = date.today() - timedelta(days=7)

        sales = sales_data.query.filter(sales_data.vendor_id == session["user_id"], sales_data.sales_date >= last_7days).all()

        for sale in sales:
            sdate = sale.sales_date.strftime("%d-%m-%Y")
            product = products.query.get(sale.product_id)
            if sdate not in data:
                data[sdate] = []

            data[sdate].append({
                "product":product.name,
                "quantity":sale.quantity
            })
            
        return jsonify({"message":"sales of last 7 days!",
                        "sales": data}), 200
    
    return jsonify("Not logged in!"), 401
