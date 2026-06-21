import requests
import streamlit as st

# =============================
# CONFIG
# =============================
API_BASE = "https://movie-rec-466x.onrender.com"   # change to http://127.0.0.1:8000 for local dev
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================
# GLOBAL CSS — dark cinema theme
# =============================
st.markdown(
    """
<style>
/* ---- Root / body ---- */
html, body, [data-testid="stApp"] {
    background-color: #0d0d0f;
    color: #e8e8e8;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background: #111217 !important;
    border-right: 1px solid #1e1f26;
}
[data-testid="stSidebar"] * { color: #c9ccd6 !important; }
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #f0c040 !important; letter-spacing: 0.04em; }

/* ---- Block container ---- */
.block-container {
    padding: 1.4rem 2rem 3rem 2rem !important;
    max-width: 1440px !important;
}

/* ---- App header ---- */
.app-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 0.2rem;
}
.app-header h1 {
    font-size: 2rem;
    font-weight: 800;
    color: #f0c040;
    letter-spacing: -0.02em;
    margin: 0;
}
.app-tagline {
    color: #6b7280;
    font-size: 0.9rem;
    margin-bottom: 1.2rem;
}

/* ---- Section labels ---- */
.section-label {
    font-size: 1.05rem;
    font-weight: 700;
    color: #f0c040;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ---- Movie card container ---- */
.movie-card {
    background: #17181f;
    border: 1px solid #1e2030;
    border-radius: 14px;
    overflow: hidden;
    transition: transform 0.18s ease, box-shadow 0.18s ease;
    cursor: pointer;
    height: 100%;
}
.movie-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(240,192,64,0.12);
    border-color: #f0c040;
}
.movie-card img { width: 100%; display: block; }
.movie-card-body { padding: 8px 10px 10px; }
.movie-card-title {
    font-size: 0.82rem;
    font-weight: 600;
    color: #e2e2e2;
    line-height: 1.2;
    height: 2.1rem;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}
.movie-card-meta {
    font-size: 0.73rem;
    color: #6b7280;
    margin-top: 4px;
}

/* ---- Details hero ---- */
.details-hero {
    background: linear-gradient(135deg, #141520 0%, #1a1b2e 100%);
    border: 1px solid #1e2030;
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 1.6rem;
}
.details-title {
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.2;
    margin-bottom: 0.5rem;
}
.genre-pill {
    display: inline-block;
    background: rgba(240,192,64,0.12);
    color: #f0c040;
    border: 1px solid rgba(240,192,64,0.35);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 3px 4px 3px 0;
    letter-spacing: 0.03em;
}
.overview-text {
    color: #b0b3be;
    font-size: 0.94rem;
    line-height: 1.7;
    margin-top: 12px;
}
.score-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(240,192,64,0.15);
    border: 1px solid rgba(240,192,64,0.4);
    border-radius: 8px;
    padding: 4px 12px;
    font-size: 0.88rem;
    font-weight: 700;
    color: #f0c040;
    margin-right: 10px;
}

/* ---- Divider ---- */
.gold-divider {
    border: none;
    border-top: 1px solid #1e2030;
    margin: 1.4rem 0;
}

/* ---- Buttons ---- */
.stButton > button {
    background: #f0c040 !important;
    color: #0d0d0f !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
    padding: 6px 14px !important;
    width: 100% !important;
    transition: opacity 0.15s !important;
}
.stButton > button:hover {
    opacity: 0.85 !important;
    color: #0d0d0f !important;
}
.stButton > button:active { opacity: 0.7 !important; }

/* ---- Back button override ---- */
.back-btn .stButton > button {
    background: #1e2030 !important;
    color: #c9ccd6 !important;
    border: 1px solid #2e3045 !important;
    width: auto !important;
}

/* ---- Inputs ---- */
[data-testid="stTextInput"] input {
    background: #17181f !important;
    border: 1px solid #2e3045 !important;
    border-radius: 10px !important;
    color: #e8e8e8 !important;
    font-size: 0.98rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #f0c040 !important;
    box-shadow: 0 0 0 2px rgba(240,192,64,0.15) !important;
}

/* ---- Selectbox ---- */
[data-testid="stSelectbox"] > div > div {
    background: #17181f !important;
    border: 1px solid #2e3045 !important;
    border-radius: 10px !important;
    color: #e8e8e8 !important;
}

/* ---- Divider ---- */
hr { border-color: #1e2030 !important; }

/* ---- Info / Warning ---- */
.stAlert { border-radius: 10px !important; }

/* ---- No poster placeholder ---- */
.no-poster {
    aspect-ratio: 2/3;
    background: #1a1b2a;
    border: 1px dashed #2e3045;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #3e4055;
    font-size: 2.5rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# =============================
# STATE + ROUTING
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except Exception:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=60)
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    keyword_l = keyword.strip().lower()
    raw_items = []

    if isinstance(data, dict) and "results" in data:
        for m in data.get("results") or []:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", ""),
                    "vote_average": m.get("vote_average"),
                }
            )
    elif isinstance(data, list):
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": m.get("poster_url"),
                    "release_date": m.get("release_date", ""),
                    "vote_average": m.get("vote_average"),
                }
            )

    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items

    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = final_list[:limit]
    return suggestions, cards


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                    "vote_average": tmdb.get("vote_average"),
                    "release_date": tmdb.get("release_date"),
                }
            )
    return cards


# =============================
# POSTER GRID
# =============================
def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies found for this section.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols, gap="small")
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")
            rating = m.get("vote_average")
            year = (m.get("release_date") or "")[:4]

            with colset[c]:
                if poster:
                    st.image(poster, use_container_width=True)
                else:
                    st.markdown(
                        "<div class='no-poster'>🎬</div>", unsafe_allow_html=True
                    )

                meta_parts = []
                if year:
                    meta_parts.append(year)
                if rating:
                    meta_parts.append(f"⭐ {rating:.1f}")

                st.markdown(
                    f"<div class='movie-card-title'>{title}</div>"
                    f"<div class='movie-card-meta'>{' · '.join(meta_parts)}</div>",
                    unsafe_allow_html=True,
                )

                if tmdb_id:
                    btn_key = f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"
                    if st.button("Open", key=btn_key):
                        goto_details(tmdb_id)


# =============================
# SIDEBAR
# =============================
with st.sidebar:
    st.markdown("## 🎬 CineMatch")
    st.markdown("---")

    if st.button("🏠  Home"):
        goto_home()

    st.markdown("### Browse")
    home_category = st.selectbox(
        "Category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
        format_func=lambda x: {
            "trending": "🔥 Trending",
            "popular": "🌟 Popular",
            "top_rated": "🏆 Top Rated",
            "now_playing": "🎭 Now Playing",
            "upcoming": "📅 Upcoming",
        }.get(x, x),
    )

    st.markdown("### Display")
    grid_cols = st.slider("Columns", 3, 8, 6)

    st.markdown("---")
    st.markdown(
        "<div style='color:#3e4055; font-size:0.75rem;'>Powered by TMDB + TF-IDF</div>",
        unsafe_allow_html=True,
    )


# =============================
# APP HEADER
# =============================
st.markdown(
    """
<div class='app-header'>
    <h1>🎬 CineMatch</h1>
</div>
<div class='app-tagline'>Discover movies you'll love — search, explore, and get personalised recommendations.</div>
""",
    unsafe_allow_html=True,
)

st.markdown("<hr class='gold-divider'>", unsafe_allow_html=True)


# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":

    typed = st.text_input(
        "",
        placeholder="🔍  Search: avenger, batman, interstellar...",
        label_visibility="collapsed",
    )

    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters.")
        else:
            with st.spinner("Searching..."):
                data, err = api_get_json(
                    "/tmdb/search", params={"query": typed.strip()}
                )

            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(
                    data, typed.strip(), limit=24
                )

                if suggestions:
                    labels = ["— Select a movie —"] + [s[0] for s in suggestions]
                    selected = st.selectbox("Suggestions", labels, index=0)
                    if selected != "— Select a movie —":
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions found — try a different keyword.")

                st.markdown("<hr class='gold-divider'>", unsafe_allow_html=True)
                st.markdown(
                    f"<div class='section-label'>🔎 Results for \"{typed.strip()}\"</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")

        st.stop()

    # --- HOME FEED ---
    category_labels = {
        "trending": "🔥 Trending Today",
        "popular": "🌟 Popular Movies",
        "top_rated": "🏆 Top Rated",
        "now_playing": "🎭 Now Playing",
        "upcoming": "📅 Coming Soon",
    }
    st.markdown(
        f"<div class='section-label'>{category_labels.get(home_category, home_category)}</div>",
        unsafe_allow_html=True,
    )

    with st.spinner("Loading movies..."):
        home_cards, err = api_get_json(
            "/home", params={"category": home_category, "limit": 24}
        )

    if err or not home_cards:
        st.error(f"Could not load feed: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")


# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":

    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    # Back button
    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("← Back"):
            goto_home()

    # Fetch details
    with st.spinner("Loading movie details..."):
        data, err = api_get_json(f"/movie/id/{tmdb_id}")

    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    # ---- Hero section ----
    poster_col, info_col = st.columns([1, 2.6], gap="large")

    with poster_col:
        if data.get("poster_url"):
            st.image(data["poster_url"], use_container_width=True)
        else:
            st.markdown(
                "<div class='no-poster' style='height:420px;'>🎬</div>",
                unsafe_allow_html=True,
            )

    with info_col:
        st.markdown(
            f"<div class='details-title'>{data.get('title', 'Unknown Title')}</div>",
            unsafe_allow_html=True,
        )

        # Metadata row
        release = data.get("release_date") or "—"
        year = release[:4] if release != "—" else "—"
        st.markdown(
            f"<span class='score-badge'>📅 {year}</span>",
            unsafe_allow_html=True,
        )

        # Genre pills
        genres = data.get("genres", []) or []
        if genres:
            pills_html = "".join(
                [f"<span class='genre-pill'>{g['name']}</span>" for g in genres]
            )
            st.markdown(
                f"<div style='margin: 10px 0 4px;'>{pills_html}</div>",
                unsafe_allow_html=True,
            )

        st.markdown("<hr class='gold-divider'>", unsafe_allow_html=True)

        overview = data.get("overview") or "No overview available for this movie."
        st.markdown(
            f"<div class='overview-text'>{overview}</div>", unsafe_allow_html=True
        )

    # Backdrop
    if data.get("backdrop_url"):
        st.markdown("<hr class='gold-divider'>", unsafe_allow_html=True)
        st.image(data["backdrop_url"], use_container_width=True)

    # ---- Recommendations ----
    st.markdown("<hr class='gold-divider'>", unsafe_allow_html=True)

    title = (data.get("title") or "").strip()
    if title:
        with st.spinner("Finding recommendations..."):
            bundle, err2 = api_get_json(
                "/movie/search",
                params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
            )

        if not err2 and bundle:
            # TF-IDF section
            tfidf_cards = to_cards_from_tfidf_items(
                bundle.get("tfidf_recommendations")
            )
            if tfidf_cards:
                st.markdown(
                    "<div class='section-label'>🤖 Similar Movies (AI Picks)</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(tfidf_cards, cols=grid_cols, key_prefix="details_tfidf")
                st.markdown("<hr class='gold-divider'>", unsafe_allow_html=True)

            # Genre section
            genre_cards = bundle.get("genre_recommendations", [])
            if genre_cards:
                first_genre = genres[0]["name"] if genres else "Genre"
                st.markdown(
                    f"<div class='section-label'>🎭 More {first_genre} Movies</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(genre_cards, cols=grid_cols, key_prefix="details_genre")

        else:
            st.markdown(
                "<div class='section-label'>🎭 You Might Also Like</div>",
                unsafe_allow_html=True,
            )
            with st.spinner("Loading genre recommendations..."):
                genre_only, err3 = api_get_json(
                    "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
                )
            if not err3 and genre_only:
                poster_grid(
                    genre_only, cols=grid_cols, key_prefix="details_genre_fallback"
                )
            else:
                st.warning("No recommendations available right now.")
    else:
        st.warning("No title available to compute recommendations.")