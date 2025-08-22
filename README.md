Spidy – Your Web-Weaving Portfolio Assistant 🕷️

Hi there! Welcome to Spidy, a friendly AI assistant that knows all about my portfolio and is ready to answer your questions about my projects, experiences, skills, and more. Think of Spidy as a little spider that helps connect the web of my work! 🕸️

Features

Ask about my projects, work experience, skills, education, or hobbies.
Answers are generated using Google Gemini AI for natural, conversational responses.
Lightweight Flask server with a React frontend for smooth interaction.
CORS-ready so you can easily integrate it into a local or remote frontend.

Project Structure
Spidy/
├─ data/
│  ├─ education_data.py
│  ├─ experiences_data.py
│  ├─ hobbies_data.py
│  ├─ projects_data.py
│  └─ skills_data.py
├─ Spidy.py        # Flask backend server
├─ requirements.txt
└─ README.md

Notes

The AI model used is Gemini-2.5-Flash via Google Generative AI.
Currently, the server is synchronous, so responses may take a few seconds.
For development, all origins are allowed via CORS. For production, restrict origins as needed.