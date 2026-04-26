from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
from dotenv import load_dotenv
load_dotenv()

# Utils (you will create these files later)
from utils.preprocess import preprocess_image
from utils.predict import predict_tumor
from utils.gradcam import generate_gradcam

# ========================
# APP SETUP
# ========================
app = Flask(__name__)
CORS(app)  # allow frontend connection

# ========================
# FOLDERS
# ========================
import os

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
GRADCAM_FOLDER = os.getenv("GRADCAM_FOLDER")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GRADCAM_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["GRADCAM_FOLDER"] = GRADCAM_FOLDER

# ========================
# HOME ROUTE
# ========================
@app.route("/")
def home():
    return jsonify({"message": "Brain Tumor Backend Running 🚀"})

# ========================
# PREDICT ROUTE
# ========================
@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "Empty file"}), 400

        # Save file with unique name
        filename = str(uuid.uuid4()) + "_" + file.filename
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # ========================
        # PROCESS IMAGE
        # ========================
        processed_image = preprocess_image(filepath)

        # ========================
        # PREDICT
        # ========================
        prediction, confidence = predict_tumor(processed_image)

        # ========================
        # GRADCAM
        # ========================
        gradcam_filename = "gradcam_" + filename
        gradcam_path = os.path.join(app.config["GRADCAM_FOLDER"], gradcam_filename)

        generate_gradcam(filepath, gradcam_path)

        # ========================
        # RESPONSE
        # ========================
        return jsonify({
            "prediction": prediction,
            "confidence": float(confidence),
            "gradcam_url": f"http://127.0.0.1:5000/gradcam/{gradcam_filename}",
            "uploaded_file": filename
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ========================
# SERVE GRADCAM IMAGE
# ========================
@app.route("/gradcam/<filename>")
def get_gradcam(filename):
    return send_from_directory(app.config["GRADCAM_FOLDER"], filename)


# ========================
# RUN SERVER
# ========================
if __name__ == "__main__":
    app.run(debug=True)
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp, url_prefix="/api/auth")

if __name__ == "__main__":
    app.run(debug=True)
    from flask import Flask
from flask_cors import CORS
from config import Config
from routes.auth_routes import auth_bp

app = Flask(__name__)
CORS(app)

# Load config
app.config.from_object(Config)

# Register routes
app.register_blueprint(auth_bp, url_prefix="/api/auth")

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])