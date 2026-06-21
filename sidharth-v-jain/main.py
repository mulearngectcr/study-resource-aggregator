import os
import sys
import requests

from dotenv import load_dotenv
load_dotenv()

GROQ_MODEL = "llama-3.3-70b-versatile"


def get_user_inputs():
    print("\n----Learning Roadmap Generator----\n")

    topic = input("Topic to learn: ")
    days_str = input("Number of days [7]: ").strip() or "7" # default to 7 days

    youtube_key = os.getenv("YOUTUBE_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")

    max_videos = 10 # Can be changed to input by user; I left it here for now
    max_books  = 10

    return {
        "topic":       topic,
        "days":        int(days_str),
        "youtube_key": youtube_key,
        "groq_key":    groq_key,
        "max_videos":  max_videos,
        "max_books":   max_books,
    }


def fetch_youtube_videos(topic, api_key, max_results):
    if not api_key:
        return []

    print(f"\nFetching YouTube videos for '{topic}'...")

    params = {
        "part": "snippet",
        "q": f"{topic} tutorial",
        "type": "video",
        "maxResults": max_results,
        "relevanceLanguage": "en",
        "key": api_key,
    }

    try:
        resp = requests.get("https://www.googleapis.com/youtube/v3/search", params=params, timeout=15)
        resp.raise_for_status()

        videos = []
        for item in resp.json().get("items", []):
            video = {
                "title":   item["snippet"].get("title", "Untitled"),
                "channel": item["snippet"].get("channelTitle", "Unknown"),
                "url":     f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            }
            videos.append(video)

        print(f"Found {len(videos)} video(s).")
        return videos

    except Exception as e:
        print(f"Warning: Could not fetch YouTube videos: {e}")
        return []


def fetch_open_library_books(topic, max_results):
    print(f"Fetching books for '{topic}' from Open Library...")

    params = {
        "q": topic,
        "fields": "title,author_name,key,first_publish_year",
        "limit": max_results,
    }

    try:
        resp = requests.get("https://openlibrary.org/search.json", params=params, timeout=15)
        resp.raise_for_status()

        books = []
        for doc in resp.json().get("docs", []):
            authors = doc.get("author_name", ["Unknown"])
            book = {
                "title":   doc.get("title", "Untitled"),
                "authors": ", ".join(authors[:3]),
                "year":    doc.get("first_publish_year", "N/A"),
                "url":     f"https://openlibrary.org{doc.get('key', '')}",
            }
            books.append(book)

        print(f"Found {len(books)} book(s).")
        return books

    except Exception as e:
        print(f"Warning: Could not fetch books: {e}")
        return []


def display_resources(videos, books):
    print("\n--- YouTube Videos ---")
    if videos:
        for i, v in enumerate(videos, 1):
            print(f"  {i}. {v['title']} ({v['channel']})")
            print(f"     {v['url']}")
    else:
        print("  (none)")

    print("\n--- Books ---")
    if books:
        for i, b in enumerate(books, 1):
            print(f"  {i}. {b['title']} by {b['authors']} ({b['year']})")
            print(f"     {b['url']}")
    else:
        print("  (none)")


def build_prompt(topic, days, videos, books):
    video_lines = ""
    for v in videos:
        video_lines += f"  - {v['title']} ({v['channel']}): {v['url']}\n"
    if not video_lines:
        video_lines = "  (none)"

    book_lines = ""
    for b in books:
        book_lines += f"  - {b['title']} by {b['authors']} ({b['year']}): {b['url']}\n"
    if not book_lines:
        book_lines = "  (none)"

    prompt = f"""You are a learning assistant.
Create a structured day-wise learning roadmap based on the following data.

Topic: {topic}
Total Days: {days}

YouTube Videos:
{video_lines}
Books:
{book_lines}

Task:
1. Break the topic into a step-by-step learning plan.
2. Distribute learning evenly across the {days} days.
3. Each day should include:
   - What to study
   - Which videos to watch (title + URL)
   - Which book sections to refer (if applicable, title + URL)
4. Keep it beginner-friendly and structured.
5. Output in clean day-wise format.

Return only the roadmap."""

    return prompt


def generate_roadmap(prompt, api_key):
    print(f"\nGenerating roadmap with Groq (llama-3.3-70b-versatile)...")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    body = {
        "model": "llama-3.3-70b-versatile",
        "max_tokens": 4096,
        "temperature": 0.7,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful learning assistant that creates structured, beginner-friendly study roadmaps.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    }

    resp = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=body, timeout=60)

    if not resp.ok:
        print(f"Error: Groq API returned {resp.status_code}: {resp.text}")
        sys.exit(1)

    return resp.json()["choices"][0]["message"]["content"].strip()


def save_roadmap(roadmap, topic, days):
    filename = f"roadmap_{topic.replace(' ', '_')}_{days}days.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Learning Roadmap: {topic} ({days} days)\n")
        f.write("=" * 60 + "\n\n")
        f.write(roadmap + "\n")
    print(f"Roadmap saved to '{filename}'")


def main():
    try:
        cfg = get_user_inputs()

        print("\n----Fetching Resources----")
        videos = fetch_youtube_videos(cfg["topic"], cfg["youtube_key"], cfg["max_videos"])
        books  = fetch_open_library_books(cfg["topic"], cfg["max_books"])

        if not videos and not books:
            print("Error: No resources found. Cannot generate a roadmap.")
            sys.exit(1)

        display_resources(videos, books)

        prompt  = build_prompt(cfg["topic"], cfg["days"], videos, books)
        roadmap = generate_roadmap(prompt, cfg["groq_key"])

        print(f"\n----{cfg['days']}-Day Roadmap: {cfg['topic']}----\n")
        print(roadmap)

        answer = input("\nSave roadmap to a text file? [y/n]: ").strip().lower()
        if answer == "y":
            save_roadmap(roadmap, cfg["topic"], cfg["days"])

        print("\nHappy learning!")

    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(0)


if __name__ == "__main__":
    main()
