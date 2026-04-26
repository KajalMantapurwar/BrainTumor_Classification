import os
import uuid
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename

from utils.preprocess import preprocess_image
from utils.predict import predict_tumor
from utils.gradcam import generate_gradcam

predict_bp = Blueprint("predict_bp", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@predict_bp.route("/api/predict", methods=["POST"])
def predict():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        file = request.files["image"]

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Only PNG, JPG, JPEG files are allowed"}), 400

        # Create upload folder if not exists
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_folder, exist_ok=True)

        # Save uploaded file
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        image_path = os.path.join(upload_folder, unique_filename)
        file.save(image_path)

        # Preprocess image
        processed_image = preprocess_image(image_path)

        # Predict
        prediction_result = predict_tumor(processed_image)

        predicted_class = prediction_result["prediction"]
        confidence = prediction_result["confidence"]

        # Generate Grad-CAM
        gradcam_folder = current_app.config["GRADCAM_FOLDER"]
        os.makedirs(gradcam_folder, exist_ok=True)

        gradcam_filename = f"gradcam_{uuid.uuid4().hex}.png"
        gradcam_path = os.path.join(gradcam_folder, gradcam_filename)

        generate_gradcam(image_path, gradcam_path)

        return jsonify({
            "message": "Prediction successful",
            "prediction": predicted_class,
            "confidence": confidence,
            "uploaded_image": f"/api/uploads/{unique_filename}",
            "gradcam_image": f"/api/gradcam/{gradcam_filename}"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@predict_bp.route("/api/uploads/<filename>", methods=["GET"])
def get_uploaded_image(filename):
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(upload_folder, filename)


@predict_bp.route("/api/gradcam/<filename>", methods=["GET"])
def get_gradcam_image(filename):
    gradcam_folder = current_app.config["GRADCAM_FOLDER"]
    return send_from_directory(gradcam_folder, filename)