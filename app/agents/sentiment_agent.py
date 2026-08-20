from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from app.config import settings
from app.schemas.twitter_schema import TweetSentimentList

SYSTEM_PROMPT = """You are a sentiment classifier for airline-related tweets.

You will be given:
1. A set of sentiment labels. Each has a name, a description, and examples.
2. One or more tweets, each with a tweet_id and text.

Task:
- Assign exactly one sentiment label to each tweet.
- Use ONLY these labels: positive, negative, neutral, mixed. Never invent a label.
- Decide based on the tweet's substantive content. Ignore URLs, @mentions,
  and #hashtags unless they carry meaning.
- Judge fit using each label's description and examples, not just its name.
- A tweet is "neutral" if it only states facts with no emotional or evaluative
  tone, even if the event sounds good or bad.
- Grade only on the language actually present in the text. Do not infer unstated
  feelings from context.
- If a tweet seems to fit more than one label, pick the single best match.

Output:
- Return a JSON object with a single key "tweets", whose value is a list with
  one object per tweet, in the same order given.
- Each object must have exactly two keys: "tweet_id" and "sentiment".
- Copy tweet_id exactly as given.
- "sentiment" must be exactly one of: positive, negative, neutral, mixed.
- Output only the JSON object. No explanation, no extra text, no markdown fences.

Example output:
{"tweets": [{"tweet_id": 1, "sentiment": "negative"}, {"tweet_id": 2, "sentiment": "neutral"}]}
"""


SENTIMENT_DICT = {
    "positive": {
        "description": "The post expresses a user's happiness, satisfaction, good well-being, gratitude, excitement, or pleasantries, or reacts favorably to something good happening to/for the airline (e.g. expansion, new routes, awards, upgrades, strong performance). Must include an emotional or evaluative tone, not just a statement of fact.",
        "examples": [
            "Just landed and my bag was the first one out, love it when that happens!",
            "Huge congrats to the airline on launching their new direct route to Tokyo!",
            "Upgraded to business class for free today, what a great way to fly.",
            "The cabin crew on my flight today were incredibly kind and attentive.",
            "So happy to hear the airline had record profits this quarter!",
        ],
    },
    "negative": {
        "description": "The post expresses a user's frustration, sadness, anger, disappointment, or dissatisfaction, or reacts unfavorably to something that negatively affects the airline or passengers (e.g. delays, cancellations, lost or damaged baggage, poor service, accidents, safety incidents). Must include an emotional or evaluative tone, not just a statement of fact.",
        "examples": [
            "My flight has been delayed 3 times now, I'm going to miss my connection.",
            "They lost my luggage AGAIN. Third time this year with this airline.",
            "Absolutely furious, sat on the tarmac for 4 hours with no explanation.",
            "Terrible news about the emergency landing today, hope everyone is safe.",
            "Frustrated that they're cutting several regional routes I rely on.",
        ],
    },
    "neutral": {
        "description": "The post is a factual or informational statement that does not express feelings, opinions, or evaluative tone, even if it describes an event that could otherwise be seen as good or bad (e.g. a delay, a new route, a policy change). If no emotion is expressed, the post is neutral regardless of subject matter.",
        "examples": [
            "Flight AA1234 departs from Gate 22 at 3:45pm.",
            "The airline is launching a new direct route to Tokyo next month.",
            "Flight 812 was delayed by two hours due to weather.",
            "The airline announced it will cut three regional routes starting in October.",
            "The airline's fleet consists mainly of Boeing 737 and Airbus A320 aircraft.",
            "The idea of picking an Ethiopian for Team Leader at Uganda Airlines gets justification. Let's get the best out of the Ethiopian we have, for the time we have him.",
            "Until it gets to the point of Uganda Airlines",
            "Rwanda air is the same as Uganda Airlines. Uganda and Rwanda is the same..one passport await",
        ],
    },
    "mixed": {
        "description": "The post expresses both positive and negative sentiment toward the airline or a flight experience, such as praising one aspect while criticizing another, or a situation with both a setback and a silver lining. Must include emotional or evaluative tone on both sides, not just factual reporting of contrasting events.",
        "examples": [
            "Flight was delayed 2 hours but the crew handed out free snacks and were super apologetic.",
            "Lost my bag, but customer service resolved it fast and even upgraded my next flight.",
            "Great legroom and entertainment, but the boarding process was total chaos.",
            "Glad they added a new route to my city, but annoyed ticket prices are now way higher.",
            "Turbulence was scary, but the pilot's calm updates made it a lot less stressful.",
        ],
    },
}


model = init_chat_model(
    settings.claude_model,
    api_key=settings.anthropic_api_key,
    timeout=600,
    max_tokens=4000,
    streaming=True,
    output_config={"effort": "low"},
)

sentiment_agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    response_format=TweetSentimentList,
)
