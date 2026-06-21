# Learning Roadmap Generator

A Python console app that builds a personalised day-wise study plan for any topic using YouTube videos, Open Library books, and the Groq LLM.

## Implementation

The user inputs the desired topic and number of days. The Youtube data v3 API and Open Library search to fetch relevant videos and books. The aggregated resources are then forwarded to an LLM (llama-3.3-70b-versatile) run on Groq, which generates a structured roadmap.

## Example output

```
--- 7-Day Roadmap: React ---

Day 1 – Introduction
  - What to study: What is React and why use it?
  - Watch: "React in 100 Seconds" – https://youtube.com/...
  - Read: "Learning React" by Alex Banks – https://openlibrary.org/...

Day 2 – Core Concepts
  ...
```
