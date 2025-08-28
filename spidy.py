import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

load_dotenv()
print("Loaded key:", os.getenv("GEMINI_API_KEY"))
app = Flask(__name__)
CORS(app)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

index = faiss.read_index("embeddings/docs_index.idx")
docs = np.load("embeddings/docs.npy", allow_pickle=True).tolist()
model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve_docs(user_question, top_n=3, min_score=0.3):
    query_vec = model.encode([user_question], convert_to_numpy=True)
    D, I = index.search(query_vec, k=top_n)
    top_docs = []
    for i, score in zip(I[0], D[0]):
        if score < min_score:
            continue
        top_docs.append(docs[i])
    return top_docs

def generate_answer(user_question):
    context_docs = " ".join(retrieve_docs(user_question))
    print(context_docs)
    prompt = f"""
        You are Spidy, a virtual assistant that answers questions about Yassine's professional portfolio.
        ONLY answer the question using the context below. Do NOT include greetings, small talk, or repetitive intros.
        Use third person (e.g., "Yassine has done..."). Be concise, accurate, and include friendly emojis occasionally when appropriate.
        Context: {context_docs}
        Question: {user_question}
        Answer:
    """
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
    app.run(host="0.0.0.0", port=5000)