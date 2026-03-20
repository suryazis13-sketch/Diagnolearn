import os
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from scanner import scan_both_papers
from analyzer import analyze_mistakes
from planner import generate_study_plan

load_dotenv()

app = Flask(__name__)
app.secret_key = "ai-learning-engine-2024-secret"
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024  # 32MB (two files)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_mime(file):
    """Return correct mime type for a file."""
    name = file.filename.lower()
    if name.endswith(".pdf"):
        return "application/pdf"
    elif name.endswith(".png"):
        return "image/png"
    elif name.endswith(".webp"):
        return "image/webp"
    else:
        return "image/jpeg"


# ── ROUTES ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    """
    Receives both the question paper and answer sheet.
    Pipeline:
      1. Gemini Vision reads BOTH files together
      2. Compares student answers against correct answers
      3. Classifies errors by topic and type
      4. Generates personalised study plan
    """

    # Validate both files are present
    if "question_paper" not in request.files:
        return jsonify({"error": "Question paper is missing"}), 400
    if "answer_sheet" not in request.files:
        return jsonify({"error": "Answer sheet is missing"}), 400

    qp_file = request.files["question_paper"]
    as_file = request.files["answer_sheet"]

    student_name = request.form.get("student_name", "Student").strip()
    subject      = request.form.get("subject", "Mathematics — Class 12")

    if qp_file.filename == "":
        return jsonify({"error": "No question paper selected"}), 400
    if as_file.filename == "":
        return jsonify({"error": "No answer sheet selected"}), 400

    if not allowed_file(qp_file.filename):
        return jsonify({"error": "Question paper: only JPG, PNG, WEBP, PDF allowed"}), 400
    if not allowed_file(as_file.filename):
        return jsonify({"error": "Answer sheet: only JPG, PNG, WEBP, PDF allowed"}), 400

    try:
        qp_bytes    = qp_file.read()
        qp_mime     = get_mime(qp_file)
        as_bytes    = as_file.read()
        as_mime     = get_mime(as_file)

        # Step 1 — Gemini Vision reads both papers together
        scanned = scan_both_papers(
            qp_bytes, qp_mime,
            as_bytes, as_mime,
            subject
        )

        # Step 2 — Analyze mistakes and classify error types
        analysis = analyze_mistakes(scanned, subject)

        # Step 3 — Generate personalised study plan
        plan = generate_study_plan(analysis, student_name, subject)

        result = {
            "student_name": student_name,
            "subject":      subject,
            "scanned":      scanned,
            "analysis":     analysis,
            "plan":         plan,
        }

        session["result"] = result
        return jsonify({"status": "ok"})

    except Exception as e:
        import traceback
        print(f"[App] Pipeline error: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/report")
def report():
    result = session.get("result")
    return render_template("report.html", result=result)


@app.route("/practice")
def practice():
    result = session.get("result")
    return render_template("practice.html", result=result)


@app.route("/demo")
def demo():
    """Loads pre-built demo — works fully offline."""
    from demo_data import DEMO_RESULT
    session["result"] = DEMO_RESULT
    return jsonify({"status": "ok"})


# ── RUN ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("AI Learning Engine starting...")
    print("Upload question paper + answer sheet")
    print("Open http://localhost:5000")
    app.run(debug=True, port=5000)