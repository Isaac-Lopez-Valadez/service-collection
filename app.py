from flask import Flask, render_template, make_response, jsonify, request

app = Flask(__name__)

PORT = 3000
HOST = "0.0.0.0"

INFO = {
    "lenguages": {
        "es": "Spanish",
        "en": "English",
        "fr": "French",
    },
    "colors": {
        "r": "Red",
        "b": "Blue",
        "g": "Green",
    },
    "clouds": {
        "AMAZON": "Amazon Web Services",
        "MICROSOFT": "Azure",
        "GOOGLE": "Google Cloud",
        "IBM": "IBM Cloud",
    }
}

#GET METHODS
@app.route("/")
def home():
    # return render_template("index.html")
    return "<h1 style='color:blue'>This is Home</h1>"

@app.route("/temp")
def template():
    return render_template("index.html")

@app.route("/qstr")
def query_string():
    if request.args:
        req = request.args
        res = {}
        for key, value in req.items():
            res[key] = value
        res = make_response(jsonify(res), 200)
        return res
    else:
        return make_response(jsonify({"error": "No query string"}), 400)

@app.route("/json")
def get_json():
    res = make_response(jsonify(INFO), 200)
    return res

@app.route("/json/<collection>/<member>")
def get_data(collection, member):
    if collection in INFO:
        member = INFO[collection].get(member)
        if member:
            res = make_response(jsonify({"res": member}), 200)
            return res
        
        return make_response(jsonify({"error": "Member Not found"}), 400)
    
    return make_response(jsonify({"error": "Collection Not found"}), 400)

#POST METHODS
@app.route("/json/<collection>", methods=["POST"])
def create_colection(collection):
    req = request.get_json()

    if collection in INFO:
        return make_response(jsonify({"error": "Collection already exists"}))

    INFO.update({collection: req})
    return make_response(jsonify({"message": "Collection created"}), 200)

#PUT METHODS
@app.route("/json/<collection>/<member>", methods=["PUT"])
def update_colection(collection, member):
    req = request.get_json()

    if collection in INFO:
        if member:
            INFO[collection][member] = req["new"]
            res = make_response(jsonify({"res": INFO[collection]}), 200)
            return res
        
        return make_response(jsonify({"error": "Member not found"}), 400)
    
    return make_response(jsonify({"error": "Collection not found"}), 400)

#DELETE METHODS
@app.route("/json/<collection>", methods=["DELETE"])
def delete_collection(collection):

    if collection in INFO:
        del INFO[collection]
        return make_response(jsonify({"messsage": "Collection deleted", "collections": INFO}), 200)
    
    return make_response(jsonify({"error": "Collection not found"}), 400)

if __name__ == "__main__":
    print(f"Server running in port {PORT}")
    app.run(host=HOST, port=PORT)