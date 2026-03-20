import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def analyze_mistakes(scanned, subject):
    questions = scanned.get("questions", [])
    if not questions:
        return _empty_analysis("No questions found.")

    wrong = [q for q in questions if not q.get("is_correct", True)]
    right = [q for q in questions if q.get("is_correct", False)]

    if not wrong:
        return {
            "overall_diagnosis": "Excellent! The student answered all questions correctly.",
            "weak_topics": [],
            "strong_topics": [{"topic": q.get("topic","Unknown"), "mastery_percent": 100, "correct_count": 1} for q in right[:3]],
            "error_patterns": [], "priority_topic": None, "total_errors": 0,
            "error_breakdown": {"conceptual_gap":0,"calculation_error":0,"formula_forgotten":0,"incomplete_answer":0}
        }

    prompt = f"""You are an expert {subject} teacher. Analyze these wrong answers and return ONLY JSON, no explanation.

Wrong answers:
{json.dumps(wrong, indent=2)}

Correct answers for context:
{json.dumps(right[:5], indent=2)}

Return ONLY this JSON:
{{
  "overall_diagnosis": "3-4 sentence diagnosis of root causes",
  "weak_topics": [
    {{"topic": "Trigonometry", "mastery_percent": 25, "error_count": 2,
      "error_types": ["conceptual_gap"],
      "specific_gaps": ["Does not know principal value range of inverse trig"],
      "priority": "high"}}
  ],
  "strong_topics": [
    {{"topic": "Algebra", "mastery_percent": 90, "correct_count": 4}}
  ],
  "error_patterns": [
    {{"pattern": "Conceptual gap in inverse functions", "frequency": 2, "affected_topics": ["Trigonometry"]}}
  ],
  "priority_topic": "The single most important topic to fix first",
  "total_errors": {len(wrong)},
  "error_breakdown": {{"conceptual_gap": 0, "calculation_error": 0, "formula_forgotten": 0, "incomplete_answer": 0}}
}}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2, max_tokens=2000,
        )
        raw = response.choices[0].message.content.strip()
        if "```" in raw:
            for part in raw.split("```"):
                part = part.strip().lstrip("json").strip()
                if part.startswith("{"):
                    raw = part
                    break
        return json.loads(raw.strip())
    except Exception as e:
        print(f"[Analyzer] Error: {e}")
        return _fallback_analysis(questions, wrong, right)


def _fallback_analysis(questions, wrong, right):
    topic_errors, topic_correct = {}, {}
    for q in questions:
        t = q.get("topic", "Unknown")
        if q.get("is_correct"):
            topic_correct[t] = topic_correct.get(t, 0) + 1
        else:
            topic_errors[t] = topic_errors.get(t, 0) + 1

    weak = []
    for t, errs in sorted(topic_errors.items(), key=lambda x: -x[1]):
        total = errs + topic_correct.get(t, 0)
        mastery = int((topic_correct.get(t, 0) / total) * 100) if total else 0
        weak.append({"topic": t, "mastery_percent": mastery, "error_count": errs,
                     "error_types": ["conceptual_gap"],
                     "specific_gaps": [f"Review {t} from NCERT"],
                     "priority": "high" if errs >= 2 else "medium"})

    strong = [{"topic": t, "mastery_percent": 90, "correct_count": c}
              for t, c in topic_correct.items() if t not in topic_errors]

    eb = {"conceptual_gap":0,"calculation_error":0,"formula_forgotten":0,"incomplete_answer":0}
    for q in wrong:
        et = q.get("error_type","conceptual_gap")
        if et in eb: eb[et] += 1

    return {
        "overall_diagnosis": "Student needs to focus on the weak topics identified below.",
        "weak_topics": weak[:5], "strong_topics": strong[:3],
        "error_patterns": [], "priority_topic": weak[0]["topic"] if weak else None,
        "total_errors": len(wrong), "error_breakdown": eb
    }


def _empty_analysis(reason):
    return {
        "overall_diagnosis": reason, "weak_topics": [], "strong_topics": [],
        "error_patterns": [], "priority_topic": None, "total_errors": 0,
        "error_breakdown": {"conceptual_gap":0,"calculation_error":0,"formula_forgotten":0,"incomplete_answer":0}
    }