from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os
from tqdm import tqdm

from data.experiences_data import experiences as experiences
from data.projects_data import projects as projects 
from data.skills_data import skills as skills
from data.education_data import education as education 
from data.certificates_data import certificates as certificates 
from data.events_data import events as events 
from data.hobbies_data import hobbies as hobbies

docs = []

def flatten_doc_structured(doc):
    doc_type = doc.get("type", "").lower()
    parts = []

    # Common fields
    parts.append(f"ID: {doc.get('id','')}")

    if doc_type in ["experience"]:
        parts.extend([
            f"Title: {doc.get('title','')}",
            f"Role: {doc.get('role','')}",
            f"Organization: {doc.get('organization','')}",
            f"Location: {doc.get('location','')}",
            f"Dates: {doc.get('timeframe','')}",
            f"Description: {doc.get('description','')}",
            f"Technologies: {', '.join(doc.get('technologies',[]))}",
            f"Skills: {', '.join(doc.get('skills',[]))}",
            f"Impact: {doc.get('impact','')}",
            f"URL: {doc.get('url','')}"
        ])
        details = doc.get("details", {})
        parts.extend([
            f"Problem: {details.get('problem','')}",
            f"Solution: {details.get('solution','')}",
            f"Results: {details.get('results','')}",
            f"Challenges: {', '.join(details.get('challenges',[]))}" if 'challenges' in details else "",
            f"Lessons Learned: {', '.join(details.get('lessons_learned',[]))}" if 'lessons_learned' in details else "",
            f"Components: {', '.join(details.get('components',[]))}" if 'components' in details else ""
        ])

    elif doc_type in ["project"]:
        parts.extend([
            f"Title: {doc.get('title','')}",
            f"Description: {doc.get('description','')}",
            f"Problem: {doc.get('problem','')}",
            f"Solution: {doc.get('solution','')}",
            f"Technologies: {', '.join(doc.get('technologies',[]))}",
            f"Type: {doc.get('type','')}",
            f"URL: {doc.get('url','')}"
        ])
        details = doc.get("details", {})
        parts.extend([
            f"Results: {details.get('results','')}",
            f"Challenges: {', '.join(details.get('challenges',[]))}" if 'challenges' in details else "",
            f"Lessons Learned: {', '.join(details.get('lessons_learned',[]))}" if 'lessons_learned' in details else "",
            f"Components: {', '.join(details.get('components',[]))}" if 'components' in details else "",
            f"Impact: {details.get('impact','')}"
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
        parts.extend([
            f"Title: {doc.get('title','')}",
            f"Description: {doc.get('description','')}",
            f"Skills: {', '.join(doc.get('skills',[]))}",
            f"Years Practiced: {doc.get('years_practiced','')}"
        ])
        details = doc.get("details", {})
        parts.extend([
            f"Reason: {details.get('reason','')}",
            f"Benefits: {', '.join(details.get('benefits',[]))}" if 'benefits' in details else "",
            f"Challenges: {', '.join(details.get('challenges',[]))}" if 'challenges' in details else "",
            f"Impact: {details.get('impact','')}"
        ])

    elif doc_type == "skill":
        parts.extend([
            f"Title: {doc.get('title','')}",
            f"Description: {doc.get('description','')}",
            f"Tools: {', '.join(doc.get('tools',[]))}" if 'tools' in doc else "",
            f"Impact: {doc.get('impact','')}"
        ])
        details = doc.get("details", {})
        parts.extend([
            f"Applications: {', '.join(details.get('applications',[]))}" if 'applications' in details else "",
            f"Strengths: {', '.join(details.get('strengths',[]))}" if 'strengths' in details else ""
        ])

    elif doc_type == "certificate":
        parts.extend([
            f"Title: {doc.get('title','')}",
            f"Description: {doc.get('description','')}",
            f"Issuer: {doc.get('issuer','')}",
            f"Date: {doc.get('date','')}",
            f"Source: {doc.get('source','')}",
            f"URL: {doc.get('url','')}"
        ])

    elif doc_type == "event":
        parts.extend([
            f"Title: {doc.get('title','')}",
            f"Description: {doc.get('description','')}",
            f"Date: {doc.get('date','')}",
            f"Location: {doc.get('location','')}",
            f"URL: {doc.get('url','')}"
        ])

    else:
        parts.extend([
            f"Title: {doc.get('title','')}",
            f"Description: {doc.get('description','')}"
        ])

    return "\n".join([p for p in parts if p])

for dataset in [experiences, education, hobbies, projects, skills, certificates, events]:
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
