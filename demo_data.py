# demo_data.py
# Pre-built demo result for the hackathon presentation.
# Visit http://localhost:5000/demo → loads this instantly, no API needed.

DEMO_RESULT = {
    "student_name": "Aryan Sharma",
    "subject": "Mathematics — Class 12",

    "scanned": {
        "readable": True,
        "total_questions": 10,
        "attempted": 10,
        "correct": 4,
        "score_percent": 40,
        "notes": "Handwriting is legible. Student attempted all questions.",
        "questions": [
            {
                "number": "Q1", "topic": "Algebra",
                "question_text": "Solve: 2x² - 5x + 3 = 0",
                "student_answer": "x = 1, x = 1.5", "correct_answer": "x = 1, x = 1.5",
                "is_correct": True, "error_type": "correct", "marks": 2
            },
            {
                "number": "Q2", "topic": "Algebra",
                "question_text": "If α, β are roots of x² - 5x + 6 = 0, find α² + β²",
                "student_answer": "25", "correct_answer": "13",
                "is_correct": False, "error_type": "conceptual_gap", "marks": 2
            },
            {
                "number": "Q3", "topic": "Trigonometry",
                "question_text": "Find sin⁻¹(sin(5π/6))",
                "student_answer": "5π/6", "correct_answer": "π/6",
                "is_correct": False, "error_type": "conceptual_gap", "marks": 3
            },
            {
                "number": "Q4", "topic": "Trigonometry",
                "question_text": "If tan θ = 4/3, find sin θ + cos θ",
                "student_answer": "5/7", "correct_answer": "7/5",
                "is_correct": False, "error_type": "calculation_error", "marks": 2
            },
            {
                "number": "Q5", "topic": "Matrices",
                "question_text": "If A = [[1,2],[3,4]], find |A|",
                "student_answer": "-2", "correct_answer": "-2",
                "is_correct": True, "error_type": "correct", "marks": 2
            },
            {
                "number": "Q6", "topic": "Differentiation",
                "question_text": "Differentiate f(x) = sin(x²) w.r.t. x",
                "student_answer": "cos(x²)", "correct_answer": "2x·cos(x²)",
                "is_correct": False, "error_type": "formula_forgotten", "marks": 3
            },
            {
                "number": "Q7", "topic": "Differentiation",
                "question_text": "Find dy/dx if y = x³ - 2x² + 5x",
                "student_answer": "3x² - 4x + 5", "correct_answer": "3x² - 4x + 5",
                "is_correct": True, "error_type": "correct", "marks": 2
            },
            {
                "number": "Q8", "topic": "Integration",
                "question_text": "Evaluate ∫(2x + 3)dx",
                "student_answer": "2x² + 3x + C", "correct_answer": "x² + 3x + C",
                "is_correct": False, "error_type": "calculation_error", "marks": 3
            },
            {
                "number": "Q9", "topic": "3D Geometry",
                "question_text": "If direction cosines are l, m, n then l² + m² + n² = ?",
                "student_answer": "1", "correct_answer": "1",
                "is_correct": True, "error_type": "correct", "marks": 1
            },
            {
                "number": "Q10", "topic": "Probability",
                "question_text": "Two dice thrown. P(sum = 7) = ?",
                "student_answer": "7/36", "correct_answer": "1/6",
                "is_correct": False, "error_type": "conceptual_gap", "marks": 2
            },
        ]
    },

    "analysis": {
        "overall_diagnosis": (
            "Aryan demonstrates solid command of basic differentiation and matrix determinants, "
            "but has critical conceptual gaps in trigonometric inverse functions and integration rules. "
            "The errors in Trigonometry suggest he has not memorised the principal value ranges — "
            "a foundational gap that will affect multiple Class 12 topics. "
            "The integration error reveals confusion between the power rule coefficient."
        ),
        "weak_topics": [
            {
                "topic": "Trigonometry",
                "mastery_percent": 25,
                "error_count": 2,
                "error_types": ["conceptual_gap", "calculation_error"],
                "specific_gaps": [
                    "Doesn't know sin⁻¹(sin x) ≠ x when x is outside [-π/2, π/2]",
                    "Confusing output of trig ratios when applying inverse functions"
                ],
                "priority": "high"
            },
            {
                "topic": "Integration",
                "mastery_percent": 30,
                "error_count": 1,
                "error_types": ["calculation_error"],
                "specific_gaps": [
                    "Forgetting to divide by (n+1) in power rule: ∫x^n dx = x^(n+1)/(n+1) + C",
                    "Wrote 2x² instead of x² for ∫2x dx"
                ],
                "priority": "high"
            },
            {
                "topic": "Differentiation",
                "mastery_percent": 40,
                "error_count": 1,
                "error_types": ["formula_forgotten"],
                "specific_gaps": [
                    "Did not apply chain rule — forgot to multiply by derivative of inner function"
                ],
                "priority": "medium"
            },
            {
                "topic": "Probability",
                "mastery_percent": 50,
                "error_count": 1,
                "error_types": ["conceptual_gap"],
                "specific_gaps": [
                    "Counted 7 favourable outcomes instead of 6 for sum=7 on two dice"
                ],
                "priority": "medium"
            }
        ],
        "strong_topics": [
            {"topic": "Matrices", "mastery_percent": 100, "correct_count": 1},
            {"topic": "Algebra",  "mastery_percent": 80,  "correct_count": 1},
            {"topic": "3D Geometry", "mastery_percent": 100, "correct_count": 1}
        ],
        "error_patterns": [
            {
                "pattern": "Conceptual gap in function inverse rules",
                "frequency": 3,
                "affected_topics": ["Trigonometry", "Integration"]
            }
        ],
        "priority_topic": "Trigonometry",
        "total_errors": 6,
        "error_breakdown": {
            "conceptual_gap": 3,
            "calculation_error": 2,
            "formula_forgotten": 1,
            "incomplete_answer": 0
        }
    },

    "plan": {
        "motivational_note": "You're only 6 corrections away from a great score — let's fix them one by one!",
        "study_plan": [
            {
                "day": 1,
                "focus_topic": "Trigonometry",
                "duration_minutes": 45,
                "tasks": [
                    "Write the principal value ranges for sin⁻¹, cos⁻¹, tan⁻¹ on paper 5 times",
                    "Read NCERT Chapter 2 Examples 1–7 carefully",
                    "Solve Exercise 2.1 Q1–10 without looking at solutions",
                    "Check answers and note which type of problem you still get wrong"
                ],
                "goal": "Never confuse sin⁻¹(sin x) = x range again"
            },
            {
                "day": 2,
                "focus_topic": "Integration",
                "duration_minutes": 45,
                "tasks": [
                    "Write the power rule formula: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C — memorise it",
                    "Solve NCERT Chapter 7 Exercise 7.1 Q1–15",
                    "Focus on problems with 2x, 3x², 5x³ — check you get the coefficient right",
                    "Do 5 definite integral problems from Exercise 7.8"
                ],
                "goal": "Zero calculation errors in basic integration"
            },
            {
                "day": 3,
                "focus_topic": "Differentiation",
                "duration_minutes": 40,
                "tasks": [
                    "Revise chain rule: d/dx[f(g(x))] = f'(g(x)) × g'(x)",
                    "Practice with sin(x²), cos(x³), e^(2x), ln(x²+1)",
                    "Solve NCERT Exercise 5.2 Q1–10",
                    "Create a formula sheet: all differentiation rules on one page"
                ],
                "goal": "Correctly apply chain rule to any composite function"
            },
            {
                "day": 4,
                "focus_topic": "Full Revision",
                "duration_minutes": 60,
                "tasks": [
                    "Re-attempt all 6 wrong questions from today's test — no help",
                    "Time yourself: 5 minutes per question max",
                    "Check answers — target 5/6 correct",
                    "If any still wrong, spend 15 mins on that topic only"
                ],
                "goal": "Score 80%+ on a fresh attempt of this paper"
            }
        ],
        "practice_questions": [
            {
                "id": 1,
                "question": "Find the principal value of sin⁻¹(sin(7π/6))",
                "topic": "Trigonometry",
                "difficulty": "Medium",
                "hint": "7π/6 is in the third quadrant — outside [-π/2, π/2]. Find sin(7π/6) first, then apply sin⁻¹.",
                "answer": "-π/6",
                "explanation": "sin(7π/6) = sin(π + π/6) = -sin(π/6) = -1/2. Now sin⁻¹(-1/2) = -π/6, which is in [-π/2, π/2]. ✓"
            },
            {
                "id": 2,
                "question": "Evaluate: ∫(3x² + 4x + 1) dx",
                "topic": "Integration",
                "difficulty": "Easy",
                "hint": "Apply power rule to each term separately: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C",
                "answer": "x³ + 2x² + x + C",
                "explanation": "∫3x² dx = 3·x³/3 = x³. ∫4x dx = 4·x²/2 = 2x². ∫1 dx = x. Total: x³ + 2x² + x + C ✓"
            },
            {
                "id": 3,
                "question": "Differentiate f(x) = cos(3x²) with respect to x",
                "topic": "Differentiation",
                "difficulty": "Medium",
                "hint": "Chain rule: outer function is cos(u), inner is 3x². Differentiate outer × derivative of inner.",
                "answer": "-6x·sin(3x²)",
                "explanation": "Let u = 3x². d/dx[cos(u)] = -sin(u)·du/dx = -sin(3x²)·6x = -6x·sin(3x²) ✓"
            },
            {
                "id": 4,
                "question": "Two cards are drawn from a deck of 52. What is P(both are aces)?",
                "topic": "Probability",
                "difficulty": "Medium",
                "hint": "There are 4 aces in 52 cards. Use combination: P = C(4,2)/C(52,2)",
                "answer": "1/221",
                "explanation": "C(4,2) = 6 ways to pick 2 aces. C(52,2) = 1326 total ways. P = 6/1326 = 1/221 ✓"
            }
        ],
        "resources": [
            {
                "topic": "Trigonometry",
                "ncert_chapter": "Chapter 2 — Inverse Trigonometric Functions",
                "exercises": ["Exercise 2.1", "Exercise 2.2", "Miscellaneous Exercise"],
                "tip": "Make a table of all 6 inverse trig functions with their domains and ranges — stick it on your wall"
            },
            {
                "topic": "Integration",
                "ncert_chapter": "Chapter 7 — Integrals",
                "exercises": ["Exercise 7.1", "Exercise 7.2", "Exercise 7.8"],
                "tip": "Do Exercise 7.1 completely before moving forward — it covers all basic rules"
            },
            {
                "topic": "Differentiation",
                "ncert_chapter": "Chapter 5 — Continuity and Differentiability",
                "exercises": ["Exercise 5.2", "Exercise 5.4"],
                "tip": "Write chain rule and product rule at top of every practice session as a reminder"
            }
        ]
    }
}


if __name__ == "__main__":
    print(f"Student      : {DEMO_RESULT['student_name']}")
    print(f"Score        : {DEMO_RESULT['scanned']['score_percent']}%")
    print(f"Weak topics  : {[t['topic'] for t in DEMO_RESULT['analysis']['weak_topics']]}")
    print(f"Practice Qs  : {len(DEMO_RESULT['plan']['practice_questions'])}")
    print(f"Study days   : {len(DEMO_RESULT['plan']['study_plan'])}")
    print("\n✅ Demo data ready!")
