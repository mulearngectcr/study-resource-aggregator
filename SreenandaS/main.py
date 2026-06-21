import json
import os

from youtube_api import get_videos
from books_api import get_books
from roadmap_generator import generate_roadmap
from cache import load_cache, save_cache


HISTORY_FILE = "history.json"


def save_history(topic, days):

    history = []

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            history = json.load(file)

    history.append(
        {
            "topic": topic,
            "days": days
        }
    )

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


def view_history():

    if not os.path.exists(HISTORY_FILE):
        print("No history found.")
        return

    with open(HISTORY_FILE, "r") as file:
        history = json.load(file)

    for item in history:
        print(
            f"Topic: {item['topic']} | Days: {item['days']}"
        )


while True:

    print("\n===== STUDY RESOURCE AGGREGATOR =====")
    print("1. Generate Roadmap")
    print("2. View History")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":

        topic = input("Enter topic: ")

        days = int(
            input("Enter number of days: ")
        )

        cache = load_cache()

        if topic.lower() in cache:

            print("\nUsing cached resources...")

            videos = cache[topic.lower()]["videos"]
            books = cache[topic.lower()]["books"]

        else:

            videos = get_videos(topic)
            books = get_books(topic)

            cache[topic.lower()] = {
                "videos": videos,
                "books": books
            }

            save_cache(cache)

        roadmap = generate_roadmap(
            topic,
            days,
            videos,
            books
        )

        print("\n")
        print(roadmap)

        with open(
            "roadmap.txt",
            "w",
            encoding="utf-8"
        ) as file:
            file.write(roadmap)

        save_history(topic, days)

        print("\nRoadmap saved to roadmap.txt")

    elif choice == "2":
        view_history()

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")