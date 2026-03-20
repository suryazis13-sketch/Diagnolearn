"""
test_groq.py - Test if Groq API is working.
Usage: python test_gemini.py
"""
import os, sys
from dotenv import load_dotenv

load_dotenv()

key = os.environ.get("GROQ_API_KEY")
if not key:
    print("[ERROR] GROQ_API_KEY not found in .env")
    print("Get your free key at: https://console.groq.com")
    sys.exit(1)

print("=" * 50)
print("  Groq API Test")
print("=" * 50)

from groq import Groq
client = Groq(api_key=key)

try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":"Say exactly: GROQ IS WORKING"}],
        max_tokens=20
    )
    print(f"\n[OK] {response.choices[0].message.content.strip()}")
    print("\nApp is ready! Run: python app.py")
except Exception as e:
    print(f"\n[ERROR] {e}")

print("=" * 50)