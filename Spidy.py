import os
from flask import Flask, request, jsonify
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

from data.education_data import education as education_data
from data.experiences_data import experiences as experiences_data
from data.hobbies_data import hobbies as hobbies_data
from data.projects_data import projects as projects_data
from data.skills_data import skills as skills_data

app = Flask(__name__)
CORS(app)
genai.api_key = os.getenv("GEMINI_API_KEY")
data = experiences_data

def flatten_doc(doc):
    parts = [
        doc["title"],
        doc["subtitle"],
        doc["description"],
        doc["context"],
        " ".join(doc["skills"]),
        " ".join(doc["technologies"]),
        doc["details"]["problem"],
        doc["details"]["solution"],
        doc["details"]["results"],
        doc["details"]["impact"],
        " ".join(doc["details"]["challenges"]),
        " ".join(doc["details"]["lessons_learned"]),
        " ".join(doc["details"]["components"])
    ]
    return " ".join(parts)

def retrieve_docs(user_question, top_n=3):
    flattened_docs = [flatten_doc(doc) for doc in data]
    def score_doc(doc):
        return sum(word.lower() in doc.lower() for word in user_question.split())
    scored_docs = [(doc, score_doc(doc)) for doc in flattened_docs]
    scored_docs.sort(key=lambda x: x[1], reverse=True)
    top_docs = [doc for doc, score in scored_docs if score > 0][:top_n]

    return top_docs or ["I can tell you about my projects, experience, and skills."]

def generate_answer(user_question):
    context_docs = " ".join(retrieve_docs(user_question))
    prompt = f"Answer the user question based on the portfolio content: {context_docs}\n\nQuestion: {user_question}\nAnswer:"
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"

@app.route('/spidy', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '')
    answer = generate_answer(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)