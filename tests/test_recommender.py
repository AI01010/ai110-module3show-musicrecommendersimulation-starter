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


# ── custom weights (score_song w_* params) ────────────────────────────────────

def test_custom_genre_weight_lower_reduces_score():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song  = make_song_dict(genre="pop", mood="happy", energy=0.8)
    default_score, _ = score_song(prefs, song)
    low_genre_score, _ = score_song(prefs, song, w_genre=0.10)
    assert default_score > low_genre_score


def test_custom_energy_weight_higher_increases_energy_contribution():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    close = make_song_dict(genre="pop", mood="happy", energy=0.81)
    far   = make_song_dict(genre="pop", mood="happy", energy=0.40)
    close_default, _ = score_song(prefs, close)
    close_boosted, _ = score_song(prefs, close, w_energy=0.40)
    far_default,   _ = score_song(prefs, far)
    far_boosted,   _ = score_song(prefs, far,   w_energy=0.40)
    # gap between close and far should be larger when energy weight is higher
    assert (close_boosted - far_boosted) > (close_default - far_default)


def test_weight_shift_changes_ranking():
    prefs = {"genre": "hip-hop", "mood": "sad", "energy": 0.90}
    sad_low  = make_song_dict(genre="hip-hop", mood="sad",    energy=0.45)  # mood match, wrong energy
    high_eng = make_song_dict(genre="hip-hop", mood="intense",energy=0.90)  # no mood match, right energy
    # default weights: sad_low wins (genre+mood beat energy gap)
    s1, _ = score_song(prefs, sad_low)
    s2, _ = score_song(prefs, high_eng)
    assert s1 > s2
    # shifted weights: energy matters more, high_eng should close the gap
    s1_shift, _ = score_song(prefs, sad_low,  w_genre=0.20, w_energy=0.40)
    s2_shift, _ = score_song(prefs, high_eng, w_genre=0.20, w_energy=0.40)
    # gap between the two songs should be smaller when energy weight is higher
    assert (s1 - s2) > (s1_shift - s2_shift)


def test_zero_genre_weight_no_genre_bonus():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song  = make_song_dict(genre="pop", mood="happy", energy=0.8)
    score, reasons = score_song(prefs, song, w_genre=0.0)
    assert "genre match" not in reasons or "+0.0" in reasons


def test_custom_artist_weight():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "artist": "Neon Echo"}
    song  = make_song_dict(genre="pop", mood="happy", energy=0.8, artist="Neon Echo")
    score_default, _ = score_song(prefs, song)
    score_boosted, _ = score_song(prefs, song, w_artist=0.20)
    assert score_boosted > score_default


# ── edge case / adversarial profile tests ────────────────────────────────────

def test_missing_genre_key_does_not_crash():
    prefs = {"mood": "happy", "energy": 0.8}   # no "genre" key
    song  = make_song_dict(genre="pop", mood="happy", energy=0.8)
    score, reasons = score_song(prefs, song)
    assert isinstance(score, float)
    assert "genre match" not in reasons


def test_missing_mood_key_does_not_crash():
    prefs = {"genre": "pop", "energy": 0.8}    # no "mood" key
    song  = make_song_dict(genre="pop", mood="happy", energy=0.8)
    score, reasons = score_song(prefs, song)
    assert isinstance(score, float)
    assert "mood match" not in reasons


def test_genre_not_in_catalog_falls_back_to_mood():
    prefs = {"genre": "bossa nova", "mood": "relaxed", "energy": 0.55}
    song  = make_song_dict(genre="jazz", mood="relaxed", energy=0.55)
    score, reasons = score_song(prefs, song)
    assert "mood match" in reasons
    assert "genre match" not in reasons


def test_mood_not_in_catalog_falls_back_to_genre():
    prefs = {"genre": "pop", "mood": "bittersweet", "energy": 0.70}
    song  = make_song_dict(genre="pop", mood="happy", energy=0.70)
    score, reasons = score_song(prefs, song)
    assert "genre match" in reasons
    assert "mood match" not in reasons


def test_total_mismatch_score_is_energy_only():
    prefs = {"genre": "bossa nova", "mood": "bittersweet", "energy": 0.50}
    song  = make_song_dict(genre="pop", mood="happy", energy=0.50)
    score, reasons = score_song(prefs, song)
    # only energy + jitter — max ~0.25
    assert score < 0.30
    assert "genre match" not in reasons
    assert "mood match" not in reasons


def test_artist_superfan_score_can_exceed_one():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.82, "artist": "Neon Echo"}
    song  = make_song_dict(genre="pop", mood="happy", energy=0.82, artist="Neon Echo")
    score, _ = score_song(prefs, song)
    # genre(0.40) + mood(0.30) + energy(0.20) + artist(0.10) + jitter > 1.0
    assert score > 1.0


def test_floor_energy_does_not_crash():
    prefs = {"genre": "ambient", "mood": "melancholic", "energy": 0.0}
    song  = make_song_dict(genre="ambient", mood="melancholic", energy=0.01)
    score, _ = score_song(prefs, song)
    assert score >= 0.0


def test_ceiling_energy_does_not_crash():
    prefs = {"genre": "metal", "mood": "aggressive", "energy": 1.0}
    song  = make_song_dict(genre="metal", mood="aggressive", energy=0.98)
    score, _ = score_song(prefs, song)
    assert score > 0.0


# ── recommend_songs edge cases ────────────────────────────────────────────────

def test_recommend_songs_k_larger_than_catalog():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    songs = [make_song_dict() for _ in range(3)]
    results = recommend_songs(prefs, songs, k=10)
    assert len(results) == 3   # can't return more than catalog size


def test_recommend_songs_reasons_always_contain_energy():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    songs = [make_song_dict(genre="classical", mood="sad", energy=0.3)]
    _, _, reasons = recommend_songs(prefs, songs, k=1)[0]
    assert "energy" in reasons


def test_recommend_songs_top_result_has_highest_score():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    songs = [
        make_song_dict(genre="pop",       mood="happy", energy=0.8),
        make_song_dict(genre="classical", mood="sad",   energy=0.2),
    ]
    results = recommend_songs(prefs, songs, k=2)
    assert results[0][1] >= results[1][1]


def test_recommend_songs_single_song_catalog():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    songs = [make_song_dict()]
    results = recommend_songs(prefs, songs, k=1)
    assert len(results) == 1
    assert results[0][0]["genre"] == "pop"


# ── Recommender class edge cases ──────────────────────────────────────────────

def test_recommender_k_larger_than_songs():
    user = UserProfile(favorite_genre="pop", favorite_mood="happy",
                       target_energy=0.8, likes_acoustic=False)
    rec  = make_small_recommender()   # 2 songs
    results = rec.recommend(user, k=99)
    assert len(results) == 2


def test_recommender_no_acoustic_bonus_when_false():
    user_no  = UserProfile(favorite_genre="lofi", favorite_mood="chill",
                           target_energy=0.4, likes_acoustic=False)
    user_yes = UserProfile(favorite_genre="lofi", favorite_mood="chill",
                           target_energy=0.4, likes_acoustic=True)
    from src.recommender import _score_song_oop
    rec  = make_small_recommender()
    lofi = rec.songs[1]   # acousticness=0.9
    score_no,  _ = _score_song_oop(user_no,  lofi)
    score_yes, _ = _score_song_oop(user_yes, lofi)
    assert score_yes > score_no


def test_explain_recommendation_no_match_returns_fallback():
    user = UserProfile(favorite_genre="bossa nova", favorite_mood="bittersweet",
                       target_energy=0.5, likes_acoustic=False)
    rec  = make_small_recommender()
    explanation = rec.explain_recommendation(user, rec.songs[0])
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


# ── load_songs data integrity ─────────────────────────────────────────────────

def test_load_songs_first_song_is_sunrise_city():
    songs = load_songs("data/songs.csv")
    assert songs[0]["title"] == "Sunrise City"
    assert songs[0]["artist"] == "Neon Echo"
    assert songs[0]["genre"] == "pop"


def test_load_songs_last_song_id_is_100():
    songs = load_songs("data/songs.csv")
    assert songs[-1]["id"] == 100


def test_load_songs_energy_values_in_range():
    songs = load_songs("data/songs.csv")
    for s in songs:
        assert 0.0 <= s["energy"] <= 1.0, f"energy out of range for song {s['id']}"


def test_load_songs_all_required_keys_present():
    required = {"id", "title", "artist", "genre", "mood",
                "energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    songs = load_songs("data/songs.csv")
    for s in songs:
        assert required.issubset(s.keys()), f"missing keys in song {s['id']}"
