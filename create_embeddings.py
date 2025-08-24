from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os
from tqdm import tqdm

from data.experiences_data import experiences as experiences
from data.education_data import education as education 
from data.hobbies_data import hobbies as hobbies 
from data.projects_data import projects as projects 
from data.skills_data import skills as skills

docs = []

def flatten_doc_structured(doc):
    doc_type = doc.get("type", "").lower()
    parts = []

    if doc_type in ["experience", "project"]:
        details = doc.get("details", {})
        parts.extend([
            f"Title: {doc.get('title','')}",
            f"Role: {doc.get('role','')}" if 'role' in doc else "",
            f"Organization: {doc.get('organization','')}" if 'organization' in doc else "",
            f"Dates: {doc.get('timeframe','')}" if 'timeframe' in doc else "",
            f"Description: {doc.get('description','')}",
            f"Technologies: {', '.join(doc.get('technologies',[]))}",
            f"Skills: {', '.join(doc.get('skills',[]))}",
            f"Problem: {details.get('problem','')}",
            f"Solution: {details.get('solution','')}",
            f"Results: {details.get('results','')}",
            f"Impact: {details.get('impact','')}",
            f"Challenges: {', '.join(details.get('challenges',[]))}",
            f"Lessons Learned: {', '.join(details.get('lessons_learned',[]))}",
            f"Components: {', '.join(details.get('components',[]))}" if 'components' in details else ""
        ])

    elif doc_type == "education":
        parts.extend([
            f"Degree: {doc.get('degree','')}",
            f"Institution: {doc.get('institution','')}",
            f"Location: {doc.get('location','')}",
            f"Dates: {doc.get('timeframe','')}",
            f"Description: {doc.get('description','')}",
            f"Achievements: {', '.join(doc.get('achievements',[]))}",
            f"Tags: {', '.join(doc.get('tags',[]))}"
        ])

    elif doc_type == "hobby":
        details = doc.get("details", {})
        parts.extend([
            f"Title: {doc.get('title','')}",
            f"Description: {doc.get('description','')}",
            f"Context: {doc.get('context','')}",
            f"Skills: {', '.join(doc.get('skills',[]))}",
            f"Reason: {details.get('reason','')}",
            f"Benefits: {', '.join(details.get('benefits',[]))}",
            f"Challenges: {', '.join(details.get('challenges',[]))}",
            f"Impact: {details.get('impact','')}"
        ])

    elif doc_type == "skill":
        details = doc.get("details", {})
        parts.extend([
            f"Title: {doc.get('title','')}",
            f"Description: {doc.get('description','')}",
            f"Context: {doc.get('context','')}",
            f"Tools: {', '.join(details.get('tools',[]))}",
            f"Applications: {', '.join(details.get('applications',[]))}",
            f"Strengths: {', '.join(details.get('strengths',[]))}",
            f"Impact: {details.get('impact','')}",
            f"Tags: {', '.join(doc.get('tags',[]))}"
        ])

    else:
        # fallback for unknown types
        parts.extend([
            f"Title: {doc.get('title','')}",
            f"Description: {doc.get('description','')}",
            f"Context: {doc.get('context','')}"
        ])

    # Remove empty strings and join with a separator
    return "\n".join([p for p in parts if p])

for dataset in [experiences, education, hobbies, projects, skills]:
    for doc in dataset:
        docs.append(flatten_doc_structured(doc))

model = SentenceTransformer('all-MiniLM-L6-v2')
doc_vectors = []
batch_size = 16
for i in tqdm(range(0, len(docs), batch_size), desc="Encoding docs"):
    batch = docs[i:i+batch_size]
    batch_vecs = model.encode(batch, convert_to_numpy=True).astype("float32")
    doc_vectors.append(batch_vecs)

doc_vectors = np.vstack(doc_vectors)

dim = doc_vectors.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(doc_vectors)

faiss.write_index(index, "embeddings/docs_index.idx")
np.save("embeddings/docs.npy", np.array(docs))

print(f"Saved {len(docs)} documents and embeddings")
