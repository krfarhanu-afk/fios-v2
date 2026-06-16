import os
import json
from openai import OpenAI

# --- CONFIGURATION ---
try:
    from streamlit.errors import StreamlitSecretNotFoundError
    import streamlit as st
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except (ImportError, StreamlitSecretNotFoundError):
    import toml
    secrets_path = os.path.join(os.path.dirname(__file__), '..', '.streamlit', 'secrets.toml')
    with open(secrets_path, 'r') as f:
        secrets = toml.load(f)
    OPENAI_API_KEY = secrets.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# --- AI PROMPT TEMPLATE ---
# This is the prompt template we designed in docs/AI_PROMPT.md
PROMPT_TEMPLATE = """
Generate a compressed financial intelligence brief for {ticker}. 

**CONTEXT:**
- Company Profile: {profile}
- Recent News: {news}
- Recent SEC Filings: {filings}

**TASK:**
Analyze the provided context and generate a 2-3 sentence summary covering the most critical insights. Focus on what a busy executive needs to know. Structure the output as a single block of text.
"""

def generate_ai_brief(ticker, profile_data, news_data, filings_data):
    """
    Generates an AI-powered summary for a given ticker using its data.
    """
    if not OPENAI_API_KEY or "YOUR_OPENAI_API_KEY" in OPENAI_API_KEY:
        print("OpenAI API key is not configured. Skipping AI brief generation.")
        return None

    # Format the context data for the prompt
    profile_context = json.dumps(profile_data, indent=2) if profile_data else "Not available."
    news_context = json.dumps(news_data, indent=2) if news_data else "Not available."
    filings_context = json.dumps(filings_data, indent=2) if filings_data else "Not available."

    prompt = PROMPT_TEMPLATE.format(
        ticker=ticker,
        profile=profile_context,
        news=news_context,
        filings=filings_context
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial analyst providing briefs for executives."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating AI brief for {ticker}: {e}")
        return None

if __name__ == "__main__":
    # Example usage for testing
    # This requires cache files to be present.
    CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'cache')
    TICKER = "AAPL"

    def load_test_data(filename):
        filepath = os.path.join(CACHE_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return None
        return None

    print(f"Generating AI brief for {TICKER}...")
    profile = load_test_data(f"{TICKER}_profile.json")
    news = load_test_data(f"{TICKER}_news.json") # This will be None for now
    filings = load_test_data(f"{TICKER}_filings.json")

    brief = generate_ai_brief(TICKER, profile, news, filings)

    if brief:
        print("\n--- GENERATED BRIEF ---")
        print(brief)
        # In a real run, we would save this to data/cache/system_ai_brief.json
    else:
        print("\n--- FAILED TO GENERATE BRIEF ---")