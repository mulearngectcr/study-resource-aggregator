import requests


def get_books(topic):
    """
    Fetch books related to a topic from Open Library API
    """

    url = f"https://openlibrary.org/search.json?q={topic}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        books = []

        for book in data.get("docs", [])[:5]:
            books.append({
                "title": book.get("title", "Unknown Title"),
                "author": (
                    book.get("author_name", ["Unknown Author"])[0]
                    if book.get("author_name")
                    else "Unknown Author"
                ),
                "link": f"https://openlibrary.org{book.get('key', '')}"
            })

        return books

    except requests.exceptions.RequestException as e:
        print(f"Error fetching books: {e}")
        return []


# Test the file directly
if __name__ == "__main__":
    topic = input("Enter topic: ")

    books = get_books(topic)

    print("\nBooks Found:\n")

    for i, book in enumerate(books, start=1):
        print(f"{i}. {book['title']}")
        print(f"   Author: {book['author']}")
        print(f"   Link: {book['link']}")
        print()