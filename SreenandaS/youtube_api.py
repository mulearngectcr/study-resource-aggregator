import requests

YOUTUBE_API_KEY = "your_youtube_api_key"


def get_videos(topic):
    url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?part=snippet"
        f"&q={topic}"
        f"&maxResults=5"
        f"&type=video"
        f"&key={YOUTUBE_API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    videos = []

    for item in data.get("items", []):
        videos.append(
            {
                "title": item["snippet"]["title"],
                "channel": item["snippet"]["channelTitle"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            }
        )

    return videos