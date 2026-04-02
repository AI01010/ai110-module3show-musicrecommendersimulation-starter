from src.recommender import Song, UserProfile, Recommender, load_songs, score_song, recommend_songs


# ── helpers ───────────────────────────────────────────────────────────────────

def make_small_recommender() -> Recommender:
    songs = [
        Song(id=1, title="Test Pop Track", artist="Test Artist",
             genre="pop", mood="happy", energy=0.8,
             tempo_bpm=120, valence=0.9, danceability=0.8, acousticness=0.2),
        Song(id=2, title="Chill Lofi Loop", artist="Test Artist",
             genre="lofi", mood="chill", energy=0.4,
             tempo_bpm=80, valence=0.6, danceability=0.5, acousticness=0.9),
    ]
    return Recommender(songs)


def make_song_dict(genre="pop", mood="happy", energy=0.8, artist="Test Artist") -> dict:
    return {"id": 1, "title": "T", "artist": artist,
            "genre": genre, "mood": mood, "energy": energy,
            "tempo_bpm": 120.0, "valence": 0.8, "danceability": 0.8, "acousticness": 0.2}


# ── OOP tests (Recommender class) ─────────────────────────────────────────────

def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(favorite_genre="pop", favorite_mood="happy",
                       target_energy=0.8, likes_acoustic=False)
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(favorite_genre="pop", favorite_mood="happy",
                       target_energy=0.8, likes_acoustic=False)
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_recommend_respects_k():
    user = UserProfile(favorite_genre="pop", favorite_mood="happy",
                       target_energy=0.8, likes_acoustic=False)
    rec = make_small_recommender()
    assert len(rec.recommend(user, k=1)) == 1


def test_genre_mismatch_scores_lower():
    user = UserProfile(favorite_genre="pop", favorite_mood="happy",
                       target_energy=0.8, likes_acoustic=False)
    rec = make_small_recommender()
    pop_song  = rec.songs[0]   # genre=pop
    lofi_song = rec.songs[1]   # genre=lofi

    from src.recommender import _score_song_oop
    pop_score,  _ = _score_song_oop(user, pop_song)
    lofi_score, _ = _score_song_oop(user, lofi_song)
    assert pop_score > lofi_score


def test_acoustic_bonus_applied():
    user = UserProfile(favorite_genre="lofi", favorite_mood="chill",
                       target_energy=0.4, likes_acoustic=True)
    rec = make_small_recommender()
    lofi_song = rec.songs[1]   # acousticness=0.9

    from src.recommender import _score_song_oop
    score_with, _ = _score_song_oop(user, lofi_song)
    # Score should include acoustic bonus (0.10) — total can reach 1.0
    assert score_with >= 0.10


def test_explain_contains_genre_when_matched():
    user = UserProfile(favorite_genre="pop", favorite_mood="happy",
                       target_energy=0.8, likes_acoustic=False)
    rec = make_small_recommender()
    explanation = rec.explain_recommendation(user, rec.songs[0])
    assert "genre" in explanation.lower()


# ── Functional tests (score_song / recommend_songs / load_songs) ──────────────

def test_score_song_genre_and_mood_match():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song  = make_song_dict(genre="pop", mood="happy", energy=0.8)
    score, reasons = score_song(prefs, song)
    # genre(0.40) + mood(0.30) + energy(0.20) + jitter = at least 0.90
    assert score >= 0.90
    assert "genre match" in reasons
    assert "mood match" in reasons


def test_score_song_no_match_is_low():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song  = make_song_dict(genre="classical", mood="sad", energy=0.2)
    score, _ = score_song(prefs, song)
    # only energy contrib + jitter, max ~0.27
    assert score < 0.30


def test_score_song_energy_closer_scores_higher():
    prefs = {"genre": "rock", "mood": "intense", "energy": 0.9}
    close_song = make_song_dict(genre="rock", mood="intense", energy=0.88)
    far_song   = make_song_dict(genre="rock", mood="intense", energy=0.40)
    close_score, _ = score_song(prefs, close_song)
    far_score,   _ = score_song(prefs, far_song)
    assert close_score > far_score


def test_score_song_artist_bonus():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "artist": "Neon Echo"}
    match_song = make_song_dict(genre="pop", mood="happy", energy=0.8, artist="Neon Echo")
    no_match   = make_song_dict(genre="pop", mood="happy", energy=0.8, artist="Other")
    match_score,   _ = score_song(prefs, match_song)
    no_match_score, _ = score_song(prefs, no_match)
    assert match_score > no_match_score


def test_recommend_songs_returns_k_results():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    songs = [make_song_dict() for _ in range(10)]
    results = recommend_songs(prefs, songs, k=3)
    assert len(results) == 3


def test_recommend_songs_sorted_descending():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    songs = [
        make_song_dict(genre="pop",       mood="happy",  energy=0.8),
        make_song_dict(genre="classical", mood="sad",    energy=0.2),
        make_song_dict(genre="rock",      mood="intense",energy=0.9),
    ]
    results = recommend_songs(prefs, songs, k=3)
    scores = [score for _, score, _ in results]
    assert scores == sorted(scores, reverse=True)


def test_recommend_songs_tuple_structure():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    songs = [make_song_dict()]
    results = recommend_songs(prefs, songs, k=1)
    song, score, reasons = results[0]
    assert isinstance(song, dict)
    assert isinstance(score, float)
    assert isinstance(reasons, str)


def test_load_songs_count():
    songs = load_songs("data/songs.csv")
    assert len(songs) == 100


def test_load_songs_numeric_fields():
    songs = load_songs("data/songs.csv")
    first = songs[0]
    assert isinstance(first["energy"],       float)
    assert isinstance(first["tempo_bpm"],    float)
    assert isinstance(first["valence"],      float)
    assert isinstance(first["danceability"], float)
    assert isinstance(first["acousticness"], float)
    assert isinstance(first["id"],           int)
