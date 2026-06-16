import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

# --- UI LAYOUT ---
st.title("Settings")
st.write("Manage your FIOS configuration.")

st.divider()

st.subheader("API Keys")
st.info("In a future version, you will be able to manage your API keys here.")

# Example of how API keys could be managed
# finnhub_key = st.text_input("Finnhub API Key", type="password", value=st.secrets.get("FINNHUB_API_KEY", ""))
# fmp_key = st.text_input("FMP API Key", type="password", value=st.secrets.get("FMP_API_KEY", ""))
# openai_key = st.text_input("OpenAI API Key", type="password", value=st.secrets.get("OPENAI_API_KEY", ""))

st.divider()

st.subheader("Data Management")
st.warning("Clearing the cache will permanently delete all stored data and require a full refresh.")
if st.button("Clear Data Cache"):
    st.success("Cache cleared (simulation). In a real app, this would trigger a data deletion process.")