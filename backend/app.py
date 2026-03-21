from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from gnn_logic import get_recommendations, items_female, items_male

app = Flask(__name__, static_folder="../frontend", static_url_path="")
app.config['PROPAGATE_EXCEPTIONS'] = True 
CORS(app)

# Serve frontend index page
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Serve other static files (CSS, JS, images)
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# Provide dropdown options dynamically
@app.route("/get-options/<gender>", methods=["GET"])
def get_options(gender):
    if gender == "female":
        return jsonify(items_female)
    elif gender == "male":
        return jsonify(items_male)
    else:
        return jsonify({"error": "Invalid gender"}), 400

# Provide GNN-based recommendations
@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.json
        gender = data.get("gender")
        selections = data.get("selections", {})
        if not gender:
            return jsonify({"error": "Gender not provided"}), 400
        
        result = get_recommendations(gender, selections)
        return jsonify(result)
    except Exception as e:
        print("Error in /recommend:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🚀 Flask server running at: http://127.0.0.1:5000/")
    app.run(debug=True)
