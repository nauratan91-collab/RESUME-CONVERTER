import os
import uuid
import json
import base64
from pathlib import Path
from flask import Flask, request, jsonify, send_file, render_template

from services.extractor import extract_text_from_file
from services.parser import parse_resume_text
from services.docx_builder import build_resume_docx, COLOR_PALETTES

app = Flask(__name__)
app.config["SECRET_KEY"] = "keydynamics-resume-converter-secret"

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "output"
DEFAULT_LOGO = BASE_DIR / "static" / "images" / "company_logo.png"

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if not file.filename:
        return jsonify({"success": False, "error": "No file selected"}), 400

    api_key = request.form.get("gemini_api_key", "").strip() or os.getenv("GEMINI_API_KEY", "")

    # Save uploaded file
    file_id = str(uuid.uuid4())[:8]
    orig_name = file.filename
    ext = Path(orig_name).suffix.lower()
    saved_filename = f"{file_id}_{orig_name}"
    save_path = UPLOAD_DIR / saved_filename
    file.save(str(save_path))

    # Extract text / structure
    extract_result = extract_text_from_file(str(save_path), gemini_api_key=api_key)

    if not extract_result.get("success"):
        return jsonify(extract_result), 400

    # If AI returned structured data directly
    if extract_result.get("structured_data"):
        structured = extract_result["structured_data"]
    else:
        # Heuristic rule-based parsing
        raw_text = extract_result.get("raw_text", "")
        structured = parse_resume_text(raw_text)

    return jsonify({
        "success": True,
        "file_id": file_id,
        "filename": orig_name,
        "file_type": ext,
        "raw_text": extract_result.get("raw_text", ""),
        "structured_data": structured,
        "ai_parsed": extract_result.get("ai_parsed", False),
        "requires_ocr": extract_result.get("requires_ocr", False)
    })


@app.route("/api/generate-docx", methods=["POST"])
def generate_docx():
    try:
        data = request.get_json(force=True)
        if not data or "resume_data" not in data:
            return jsonify({"success": False, "error": "Missing resume data"}), 400

        resume_data = data["resume_data"]
        header_alignment = data.get("header_alignment", "dual")
        header_tagline = data.get("header_tagline", "CONFIDENTIAL CANDIDATE DOSSIER | KEY DYNAMICS SOLUTIONS")
        palette_name = data.get("palette_name", "key_dynamics")
        logo_width = float(data.get("logo_width", 2.3))

        # Check logo path
        custom_logo_data = data.get("custom_logo_data")
        active_logo_path = str(DEFAULT_LOGO)

        if custom_logo_data and custom_logo_data.startswith("data:image"):
            # Save uploaded custom logo
            try:
                header_part, b64_part = custom_logo_data.split(",", 1)
                logo_bytes = base64.b64decode(b64_part)
                temp_logo_path = UPLOAD_DIR / f"custom_logo_{uuid.uuid4().hex[:6]}.png"
                with open(temp_logo_path, "wb") as f:
                    f.write(logo_bytes)
                active_logo_path = str(temp_logo_path)
            except Exception as e:
                print("Error decoding custom logo:", e)
                active_logo_path = str(DEFAULT_LOGO)

        # Output filename based on candidate name
        raw_name = resume_data.get("full_name", "Candidate").replace(" ", "_")
        safe_name = "".join(c for c in raw_name if c.isalnum() or c == "_") or "Resume"
        doc_filename = f"{safe_name}_KeyDynamics_Resume_{uuid.uuid4().hex[:6]}.docx"
        output_file_path = OUTPUT_DIR / doc_filename

        build_resume_docx(
            resume_data=resume_data,
            output_path=str(output_file_path),
            logo_path=active_logo_path,
            header_alignment=header_alignment,
            header_tagline=header_tagline,
            palette_name=palette_name,
            logo_width_inches=logo_width,
            include_footer=True
        )

        return jsonify({
            "success": True,
            "filename": doc_filename,
            "download_url": f"/download/{doc_filename}"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/download/<path:filename>")
def download_file(filename):
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        return "File not found", 404
    return send_file(str(file_path), as_attachment=True, download_name=filename)


@app.route("/api/upload-logo", methods=["POST"])
def upload_logo():
    if "logo" not in request.files:
        return jsonify({"success": False, "error": "No logo file uploaded"}), 400
    logo_file = request.files["logo"]
    if not logo_file.filename:
        return jsonify({"success": False, "error": "No file selected"}), 400

    ext = Path(logo_file.filename).suffix.lower()
    if ext not in [".png", ".jpg", ".jpeg", ".webp"]:
        return jsonify({"success": False, "error": "Only image formats are supported for the header logo"}), 400

    new_logo_path = BASE_DIR / "static" / "images" / f"custom_logo{ext}"
    logo_file.save(str(new_logo_path))

    return jsonify({
        "success": True,
        "logo_url": f"/static/images/{new_logo_path.name}"
    })


@app.route("/api/palettes", methods=["GET"])
def get_palettes():
    return jsonify({
        "palettes": list(COLOR_PALETTES.keys())
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5055))
    app.run(host="0.0.0.0", port=port, debug=True)
