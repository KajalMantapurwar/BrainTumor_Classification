import os
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from database.db import reports_collection

report_bp = Blueprint("report_bp", __name__)


@report_bp.route("/api/reports", methods=["POST"])
def save_report():
    try:
        data = request.get_json()

        required_fields = ["patient_name", "prediction", "confidence", "uploaded_image", "gradcam_image"]

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        report = {
            "report_id": uuid.uuid4().hex,
            "patient_name": data["patient_name"],
            "prediction": data["prediction"],
            "confidence": data["confidence"],
            "uploaded_image": data["uploaded_image"],
            "gradcam_image": data["gradcam_image"],
            "notes": data.get("notes", ""),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        reports_collection.insert_one(report)

        return jsonify({
            "message": "Report saved successfully",
            "report": report
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@report_bp.route("/api/reports", methods=["GET"])
def get_all_reports():
    try:
        reports = list(reports_collection.find({}, {"_id": 0}))
        return jsonify({
            "message": "Reports fetched successfully",
            "reports": reports
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@report_bp.route("/api/reports/<report_id>", methods=["GET"])
def get_single_report(report_id):
    try:
        report = reports_collection.find_one({"report_id": report_id}, {"_id": 0})

        if not report:
            return jsonify({"error": "Report not found"}), 404

        return jsonify({
            "message": "Report fetched successfully",
            "report": report
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@report_bp.route("/api/reports/<report_id>", methods=["DELETE"])
def delete_report(report_id):
    try:
        report = reports_collection.find_one({"report_id": report_id})

        if not report:
            return jsonify({"error": "Report not found"}), 404

        reports_collection.delete_one({"report_id": report_id})

        return jsonify({
            "message": "Report deleted successfully"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500