import streamlit as st
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Set your Genius API token here
GENIUS_API_TOKEN = "https://genius.com/developers"

def search_song_on_genius(song_title):
    base_url = "https://api.genius.com"
    headers = {"Authorization": f"Bearer {GENIUS_API_TOKEN}"}
    search_url = f"{base_url}/search"
    params = {"q": f"Taylor Swift {song_title}"}
    
    response = requests.get(search_url, params=params, headers=headers)

    # Debugging help:
    if response.status_code != 200:
        st.error(f"Failed to connect to Genius API: {response.status_code}")
        st.text(response.text)
        return None

    try:
        json_data = response.json()
        hits = json_data["response"]["hits"]
        if hits:
            return hits[0]["result"]["url"]
        return None
    except KeyError:
        st.error("Unexpected response structure from Genius API.")
        st.text(response.text)
        return None

def scrape_lyrics_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    lyrics_divs = soup.find_all("div", class_="Lyrics__Container")
    if not lyrics_divs:
        return "Lyrics not found."

    lyrics = "\n".join(div.get_text(separator="\n") for div in lyrics_divs)
    return lyrics

def generate_wordcloud(lyrics):
    wc = WordCloud(width=800, height=400, background_color='white').generate(lyrics)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

# --- Streamlit App ---
st.set_page_config(page_title="Swiftie Lyrics Explorer 🎤", layout="centered")
st.title("🎶 Swiftie Lyrics Explorer")

song_title = st.text_input("Enter a Taylor Swift song title:")

if song_title:
    with st.spinner("Fetching lyrics..."):
        song_url = search_song_on_genius(song_title)
        if song_url:
            lyrics = scrape_lyrics_from_url(song_url)
            st.subheader("Lyrics")
            st.text_area(" ", lyrics, height=300)

            st.subheader("Word Cloud")
            generate_wordcloud(lyrics)
        else:
            st.error("Song not found on Genius.")
