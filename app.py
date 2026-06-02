from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB Connection
client = MongoClient(
    "mongodb+srv://Bandaru:anji1234@cluster0.ab7xbzy.mongodb.net/?appName=Cluster0"
)

# Database
db = client["commerece-crt"]

# Collections
user_collection = db["users"]
product_collection = db["products"]
cart = []

# Home Route
@app.route('/')
def home():
    return "Welcome to Ecommerce"




# GET All Users
@app.route("/users", methods=["GET"])
def get_users():

    users = []

    for user in user_collection.find():

        users.append({
            "_id": str(user["_id"]),
            "name": user.get("name"),
            "email": user.get("email")
        })

    return jsonify(users)


# ADD User
@app.route("/users", methods=["POST"])
def add_user():

    data = request.get_json()

    user = {
        "name": data.get("name"),
        "email": data.get("email")
    }

    result = user_collection.insert_one(user)

    return jsonify({
        "message": "User added successfully",
        "id": str(result.inserted_id)
    })

# GET All Products
@app.route("/products", methods=["GET"])
def get_products():

    products = []

    for product in product_collection.find():

        products.append({
            "_id": str(product["_id"]),
            "name": product.get("name"),
            "cost": product.get("cost")
        })

    return jsonify(products)


# ADD Product
@app.route("/products", methods=["POST"])
def add_product():

    data = request.get_json()

    product = {
        "name": data.get("name"),
        "cost": data.get("cost")
    }

    result = product_collection.insert_one(product)

    return jsonify({
        "message": "Product added successfully",
        "id": str(result.inserted_id)
    })


# GET Single Product
@app.route("/products/<id>", methods=["GET"])
def get_single_product(id):

    product = product_collection.find_one({
        "_id": ObjectId(id)
    })

    if product:

        return jsonify({
            "_id": str(product["_id"]),
            "name": product["name"],
            "cost": product["cost"]
        })

    return jsonify({
        "message": "Product Not Found"
    })




@app.route("/cart", methods=["GET"])
def get_cart():
    return jsonify(cart)


# Run Server
if __name__ == "__main__":
    app.run(debug=True)