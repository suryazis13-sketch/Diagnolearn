import os
import json
import io
from groq import Groq
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def _extract_text(file_bytes, mime_type, label):
    if mime_type == "application/pdf":
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            text = ""
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text() or ""
                text += f"\n--- Page {i+1} ---\n{page_text}"
            print(f"[Scanner] {label}: {len(text)} chars from {len(reader.pages)} pages")
            return text.strip()
        except Exception as e:
            print(f"[Scanner] PDF extract error for {label}: {e}")
            return ""
    else:
        return f"[Image file uploaded as {label} - text extraction not supported for images with Groq]"


def scan_both_papers(qp_bytes, qp_mime, as_bytes, as_mime, subject):
    print(f"[Scanner] QP: {len(qp_bytes)//1024}KB | AS: {len(as_bytes)//1024}KB")

    qp_text = _extract_text(qp_bytes, qp_mime, "question_paper")
    as_text = _extract_text(as_bytes, as_mime, "answer_sheet")

    if not qp_text or not as_text:
        return _empty_scan("Could not extract text. Make sure both files are PDFs with selectable text.")

    prompt = f"""You are an expert {subject} teacher evaluating a student's answer sheet.

=== QUESTION PAPER ===
{qp_text[:6000]}

=== STUDENT ANSWER SHEET ===
{as_text[:6000]}

Your job:
- Match each question from the question paper with the student's answer
- Check if the answer is correct using your subject knowledge
- Classify the error type for each wrong answer

Return ONLY a valid JSON object, no explanation, no markdown, no code fences:

{{
  "readable": true,
  "total_questions": 18,
  "attempted": 15,
  "correct": 10,
  "score_percent": 56,
  "total_marks": 40,
  "marks_obtained": 22,
  "notes": "Brief observation about the student's performance",
  "questions": [
    {{
      "number": "Q1",
      "question_text": "Short description of question",
      "correct_answer": "A) 2, 3",
      "student_answer": "A) 2, 3",
      "is_correct": true,
      "topic": "Polynomials",
      "error_type": "correct",
      "marks_allocated": 1
    }}
  ]
}}

error_type: "correct", "conceptual_gap", "calculation_error", "formula_forgotten", "incomplete_answer"
topics: Polynomials, Linear Equations, Trigonometry, Circles, Coordinate Geometry, Probability, Statistics, Arithmetic Progressions, Mensuration, Similarity, Differentiation, Integration, Matrices, Vectors, 3D Geometry, Inverse Trigonometry, Sets, Functions, Limits

ONLY return the JSON. Nothing else."""

    try:
        print("[Scanner] Sending to Groq...")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=4000,
        )
        raw = response.choices[0].message.content.strip()
        print(f"[Scanner] Response first 200 chars: {raw[:200]}")

        if "```" in raw:
            for part in raw.split("```"):
                part = part.strip().lstrip("json").strip()
                if part.startswith("{"):
                    raw = part
                    break

        scanned = json.loads(raw.strip())
        print(f"[Scanner] OK - {scanned.get('total_questions',0)} Qs, {scanned.get('score_percent',0)}%")
        return scanned

    except json.JSONDecodeError as e:
        print(f"[Scanner] JSON error: {e}")
        print(f"[Scanner] Raw was: {raw[:500] if 'raw' in locals() else 'N/A'}")
        return _empty_scan("Could not parse AI response.")
    except Exception as e:
        print(f"[Scanner] Error: {type(e).__name__}: {e}")
        return _empty_scan(str(e))


def _empty_scan(reason):
    return {
        "readable": False, "total_questions": 0, "attempted": 0,
        "correct": 0, "score_percent": 0, "questions": [],
        "total_marks": 0, "marks_obtained": 0,
        "notes": f"Scan failed: {reason}"
    }