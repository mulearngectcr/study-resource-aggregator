from openai import OpenAI

client = OpenAI(
    api_key="your_api_key",
    base_url="https://openrouter.ai/api/v1"
)


def generate_roadmap(topic, days, videos, books):

    video_text = "\n".join(
        [f"- {v['title']} ({v['url']})" for v in videos]
    )

    book_text = "\n".join(
        [f"- {b['title']} by {b['author']}" for b in books]
    )

    prompt = f"""
You are a learning assistant.

Create a structured day-wise learning roadmap.

Topic: {topic}
Total Days: {days}

YouTube Videos:
{video_text}

Books:
{book_text}

Requirements:
1. Break the topic into a step-by-step learning plan.
2. Distribute learning evenly across the days.
3. Include videos and books where relevant.
4. Keep it beginner friendly.
5. Return only the roadmap.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b:free",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content