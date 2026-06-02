from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB Connection
client = MongoClient(
    'mongodb+srv://Bandaru:anji1234@cluster0.ab7xbzy.mongodb.net/?appName=Cluster0'
)


# Database Name
db = client["users-crt"]

# Collection Name
user_collection = db["users"]


# -----------------------------
# Home Route
# -----------------------------
@app.route("/")
def home():
    return jsonify({
        "message": "Flask MongoDB CRUD API Running"
    })


# -----------------------------
# GET ALL USERS
# -----------------------------
@app.route("/users", methods=["GET"])
def get_users():

    users = []

    for user in user_collection.find():

        users.append({
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        })

    return jsonify(users)


# -----------------------------
# GET SINGLE USER
# -----------------------------
@app.route("/users/<id>", methods=["GET"])
def get_single_user(id):

    user = user_collection.find_one({
        "_id": ObjectId(id)
    })

    if user:

        return jsonify({
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        })

    return jsonify({
        "message": "User Not Found"
    })


# -----------------------------
# ADD USER
# -----------------------------
@app.route("/users", methods=["POST"])
def add_user():

    data = request.get_json()

    user = {
        "name": data.get("name"),
        "email": data.get("email")
    }

    result = user_collection.insert_one(user)

    return jsonify({
        "message": "User Inserted Successfully",
        "id": str(result.inserted_id)
    })


# -----------------------------
# UPDATE USER
# -----------------------------
@app.route("/users/<id>", methods=["PUT"])
def update_user(id):

    data = request.get_json()

    updated_user = {
        "name": data.get("name"),
        "email": data.get("email")
    }

    result = user_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": updated_user}
    )

    if result.modified_count > 0:

        return jsonify({
            "message": "User Updated Successfully"
        })

    return jsonify({
        "message": "User Not Found or No Changes Made"
    })


# -----------------------------
# DELETE USER
# -----------------------------
@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):

    result = user_collection.delete_one({
        "_id": ObjectId(id)
    })

    if result.deleted_count > 0:

        return jsonify({
            "message": "User Deleted Successfully"
        })

    return jsonify({
        "message": "User Not Found"
    })


# -----------------------------
# RUN FLASK SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)