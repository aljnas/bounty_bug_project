from flask import Blueprint, request, jsonify
import subprocess

# Crea un Blueprint para el módulo analyzer
analyzer_bp = Blueprint("analyzer", __name__)

@analyzer_bp.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    target = data.get('target')  # Dirección IP o URL a analizar

    if not target:
        return jsonify({"error": "No target provided"}), 400

    try:
        # Ejecutar un escaneo básico con Nmap (como ejemplo)
        result = subprocess.check_output(["nmap", "-sV", target], universal_newlines=True)
        return jsonify({"target": target, "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
from flask import Blueprint, request, jsonify
from app.models import Scan, db
from flask import current_app as app

analyzer_bp = Blueprint("analyzer", __name__)

@analyzer_bp.route("/scan", methods=["POST"])
def create_scan():
    data = request.get_json()
    if not data or not data.get("target"):
        return jsonify({"error": "Target is required"}), 400

    scan = Scan(target=data["target"], user_id=1)  # Suponemos que el usuario ID 1 es el que ejecuta
    db.session.add(scan)
    db.session.commit()

    return jsonify({"message": "Scan created", "scan_id": scan.id}), 201

@analyzer_bp.route("/scan/<int:scan_id>", methods=["GET"])
def get_scan(scan_id):
    scan = Scan.query.get(scan_id)
    if not scan:
        return jsonify({"error": "Scan not found"}), 404

    return jsonify({
        "id": scan.id,
        "target": scan.target,
        "status": scan.status,
        "result": scan.result,
        "created_at": scan.created_at
    })
@analyzer_bp.route('/scans', methods=['GET'])
def list_scans():
    scans = Scan.query.all()
    if not scans:
        return jsonify({"error": "No scans found"}), 404
    return jsonify({
        "scans": [
            {
                "id": scan.id,
                "target": scan.target,
                "status": scan.status,
                "result": scan.result,
                "created_at": scan.created_at
            }
            for scan in scans
        ]
    }), 200
