import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def generate_study_plan(analysis, student_name, subject):
    weak_topics = analysis.get("weak_topics", [])
    if not weak_topics:
        return {
            "study_plan": [], "practice_questions": [], "resources": [],
            "motivational_note": "Great work! Keep practicing to maintain your scores."
        }

    prompt = f"""You are an expert {subject} teacher creating a personalised study plan for {student_name}.

Weak areas:
{json.dumps(weak_topics, indent=2)}

Return ONLY this JSON object, no explanation:
{{
  "study_plan": [
    {{"day": 1, "focus_topic": "Topic name", "duration_minutes": 45,
      "tasks": ["Read NCERT Chapter X examples", "Solve Exercise X.1 Q1-5", "Write formulas on paper"],
      "goal": "What the student will achieve today"}}
  ],
  "practice_questions": [
    {{"id": 1, "question": "An actual practice question", "topic": "Topic",
      "difficulty": "Medium", "hint": "Helpful hint without giving answer",
      "answer": "The correct answer",
      "explanation": "Step by step solution"}}
  ],
  "resources": [
    {{"topic": "Topic", "ncert_chapter": "Chapter X - Name",
      "exercises": ["Exercise X.1", "Exercise X.2"],
      "tip": "Specific study tip"}}
  ],
  "motivational_note": "One encouraging sentence for {student_name}"
}}

Rules:
- Exactly 4 days in study_plan, day 1 = highest priority topic
- 1-2 practice questions per weak topic, max 6 total
- All CBSE/NCERT Class 10-12 specific
- Return ONLY the JSON"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3, max_tokens=3000,
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
        print(f"[Planner] Error: {e}")
        return _fallback_plan(weak_topics, student_name)


def _fallback_plan(weak_topics, student_name):
    ncert = {
        "Trigonometry":           ("Chapter 8",  ["Exercise 8.1","Exercise 8.2"]),
        "Inverse Trigonometry":   ("Chapter 2",  ["Exercise 2.1","Exercise 2.2"]),
        "Polynomials":            ("Chapter 2",  ["Exercise 2.1","Exercise 2.2"]),
        "Linear Equations":       ("Chapter 3",  ["Exercise 3.1","Exercise 3.2"]),
        "Statistics":             ("Chapter 14", ["Exercise 14.1","Exercise 14.2"]),
        "Probability":            ("Chapter 15", ["Exercise 15.1"]),
        "Circles":                ("Chapter 10", ["Exercise 10.1","Exercise 10.2"]),
        "Coordinate Geometry":    ("Chapter 7",  ["Exercise 7.1","Exercise 7.2"]),
        "Arithmetic Progressions":("Chapter 5",  ["Exercise 5.1","Exercise 5.2"]),
        "Mensuration":            ("Chapter 13", ["Exercise 13.1","Exercise 13.2"]),
        "Differentiation":        ("Chapter 5",  ["Exercise 5.1","Exercise 5.2"]),
        "Integration":            ("Chapter 7",  ["Exercise 7.1","Exercise 7.2"]),
        "Matrices":               ("Chapter 3",  ["Exercise 3.1","Exercise 3.2"]),
        "Vectors":                ("Chapter 10", ["Exercise 10.1","Exercise 10.2"]),
        "Sets":                   ("Chapter 1",  ["Exercise 1.1","Exercise 1.2"]),
        "Functions":              ("Chapter 2",  ["Exercise 2.1","Exercise 2.2"]),
    }
    plan, pqs, resources = [], [], []
    for i, t in enumerate(weak_topics[:4]):
        topic = t["topic"]
        ch, exs = ncert.get(topic, ("Relevant Chapter", ["Exercise 1"]))
        plan.append({"day": i+1, "focus_topic": topic, "duration_minutes": 45,
                     "tasks": [f"Read NCERT {ch} examples", f"Solve {exs[0]}", "Write key formulas"],
                     "goal": f"Understand and fix gaps in {topic}"})
        resources.append({"topic": topic, "ncert_chapter": f"{ch} - {topic}",
                          "exercises": exs, "tip": "Focus on NCERT examples before exercises"})
        pqs.append({"id": i+1, "question": f"Practice question on {topic} from NCERT {ch}",
                    "topic": topic, "difficulty": "Medium",
                    "hint": f"Review {topic} formulas first",
                    "answer": f"Refer to NCERT {ch}",
                    "explanation": f"See NCERT {ch} examples for step-by-step solution"})
    return {"study_plan": plan, "practice_questions": pqs, "resources": resources,
            "motivational_note": f"You've got this, {student_name}! Daily practice is the key."}