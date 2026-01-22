import pickle
import streamlit as st
import requests

# ---------------- CONFIG ----------------
TMDB_API_KEY = "1b178b3e94242bbf2e1a42b1749d1adc"   # 🔴 Replace with your key
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"

st.set_page_config(
    page_title="Movie Recommender",
    layout="wide"
)

# ---------------- API CALL ----------------
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        poster_path = data.get("poster_path")
        if poster_path:
            return POSTER_BASE_URL + poster_path
        else:
            return None

    except requests.exceptions.RequestException as e:
        return None


# ---------------- RECOMMENDER ----------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    movie_names = []
    movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        movie_names.append(movies.iloc[i[0]].title)
        movie_posters.append(fetch_poster(movie_id))

    return movie_names, movie_posters


# ---------------- LOAD DATA ----------------
movies = pickle.load(open("model/movie_list.pkl", "rb"))
similarity = pickle.load(open("model/similarity.pkl", "rb"))

# ---------------- UI ----------------
st.header("🎬 Movie Recommender System")

movie_list = movies["title"].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button("Show Recommendation"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            if recommended_movie_posters[i]:
                st.image(recommended_movie_posters[i])
            else:
                st.write("Poster not available")
