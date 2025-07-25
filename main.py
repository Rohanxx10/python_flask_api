from flask import Flask, request, jsonify
import google.generativeai as genai
import json
import os

genai.configure(api_key=os.getenv("AIzaSyAQCcwP7SE_nBmDUt_8d37SZj5mSEAGB5g"))

app = Flask(__name__)

@app.route("/get-scheme-info", methods=["POST"])
def get_government_scheme_info():
    data = request.json
    state = data.get("state")
    language = data.get("language")
    question = data.get("question")

    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

    prompt = f"""
You are an expert in Indian government schemes and official documents (like caste certificates, OBC certificates, income certificates).

Step 1: Check if the question relates to government schemes or official government documents/certificates.
- If NO, respond: "❌ Sorry, I can only help with government welfare schemes or official documents."

Step 2: If YES, respond with info about eligibility, process, documents required, and official website in {language}.
Reply ONLY in JSON with keys:
scheme_name, type, eligibility, documents_required, application_process, official_website

Question:
{question}
"""

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()

        start = response_text.find('{')
        end = response_text.rfind('}')
        if start != -1 and end != -1:
            json_str = response_text[start:end+1]
            return jsonify(json.loads(json_str))
        else:
            return jsonify({"error": "No valid JSON found", "raw_response": response_text})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/", methods=["GET"])
def index():
    return "✅ Govt Scheme Info API is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
