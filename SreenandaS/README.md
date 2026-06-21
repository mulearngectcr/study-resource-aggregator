Study Resource Aggregator + AI Roadmap Generator
Overview
A Python console app that fetches learning resources (books + videos), aggregates them, and generates a day-wise study roadmap using an LLM.
Features
- Search any topic
- Fetch books from Open Library API
- Fetch YouTube resources (optional)
- Generate AI-based roadmap (OpenRouter)
- Cache results
- Save search history
Tech Stack
Python, Requests, Open Library API, OpenRouter API, JSON
Setup
pip install -r requirements.txt
Run project:
python main.py
 API Keys
- OpenRouter API: https://openrouter.ai/keys  
(Add your key in `roadmap_generator.py`)
Project Files
- main.py
- books_api.py
- roadmap_generator.py
- cache.py
Output
Generates a structured day-wise learning roadmap for any topic.
