"""
Command line runner for the Music Recommender Simulation.
Run with: python -m src.main
"""

from src.recommender import load_songs, recommend_songs, score_song


PROFILES = {
    # --- core profiles ---
    "Happy Pop Fan":            {"genre": "pop",        "mood": "happy",      "energy": 0.82},
    "Chill Lofi Study":         {"genre": "lofi",       "mood": "chill",      "energy": 0.38},
    "High Energy Rock":         {"genre": "rock",       "mood": "intense",    "energy": 0.92},

    # --- non-core profiles (diverse normal use cases) ---
    "Late Night R&B":           {"genre": "r&b",        "mood": "romantic",   "energy": 0.60},
    "Metal Head":               {"genre": "metal",      "mood": "aggressive", "energy": 0.97},
    "Sunday Jazz":              {"genre": "jazz",       "mood": "relaxed",    "energy": 0.40},
    "Country Roads":            {"genre": "country",    "mood": "nostalgic",  "energy": 0.50},
    "Folk & Fire":              {"genre": "folk",       "mood": "happy",      "energy": 0.55},
    "EDM Rave":                 {"genre": "edm",        "mood": "euphoric",   "energy": 0.96},
    "Classical Background":     {"genre": "classical",  "mood": "chill",      "energy": 0.20},
    "Indie Dreamer":            {"genre": "indie pop",  "mood": "nostalgic",  "energy": 0.65},
    "Reggae Sunday":            {"genre": "reggae",     "mood": "chill",      "energy": 0.50},
    "Synthwave Night Drive":    {"genre": "synthwave",  "mood": "moody",      "energy": 0.75},
    "Hip-Hop Confident":        {"genre": "hip-hop",    "mood": "confident",  "energy": 0.80},

    # --- existing adversarial profiles ---
    "Sad High Energy":          {"genre": "hip-hop",    "mood": "sad",        "energy": 0.90},  # conflicting: high energy but sad mood
    "Acoustic Soul Night":      {"genre": "soul",       "mood": "romantic",   "energy": 0.52},  # niche genre, low catalog coverage
    "Genre Wildcard":           {"genre": "jazz-fusion","mood": "relaxed",    "energy": 0.58},  # only 1 matching song in catalog

    # --- new edge cases ---
    "Floor Energy":             {"genre": "ambient",    "mood": "melancholic","energy": 0.01},  # near-zero energy — tests energy floor
    "Ceiling Energy":           {"genre": "metal",      "mood": "aggressive", "energy": 0.99},  # max energy — tests energy ceiling
    "Genre Not In Catalog":     {"genre": "bossa nova", "mood": "relaxed",    "energy": 0.55},  # genre that doesn't exist in songs.csv
    "Mood Not In Catalog":      {"genre": "pop",        "mood": "bittersweet","energy": 0.70},  # mood that doesn't exist in songs.csv
    "No Genre At All":          {                       "mood": "happy",      "energy": 0.80},  # missing genre key entirely
    "Artist Superfan":          {"genre": "pop",        "mood": "happy",      "energy": 0.82,   # artist bonus stacks on top of full match
                                 "artist": "Neon Echo"},
    "Total Mismatch":           {"genre": "bossa nova", "mood": "bittersweet","energy": 0.50},  # nothing matches — pure energy scoring only
}


def print_recommendations(profile_name: str, recs: list) -> None:
    print(f"\n{'='*55}")
    print(f"  Profile: {profile_name}")
    print(f"{'='*55}")
    for i, (song, score, reasons) in enumerate(recs, 1):
        print(f"  {i}. {song['title']} — {song['artist']}  [{song['genre']} / {song['mood']}]")
        print(f"     Score : {score:.4f}")
        print(f"     Why   : {reasons}")
        print()


def run_experiment(songs: list) -> None:
    """Weight shift experiment: halve genre (0.40→0.20), double energy (0.20→0.40)."""
    prefs = PROFILES["Sad High Energy"]
    print("\n" + "#" * 55)
    print("  EXPERIMENT: Weight Shift on 'Sad High Energy'")
    print("  Normal   — genre=0.40, energy=0.20")
    print("  Shifted  — genre=0.20, energy=0.40")
    print("#" * 55)

    for label, kwargs in [
        ("Normal weights",  {}),
        ("Shifted weights", {"w_genre": 0.20, "w_energy": 0.40}),
    ]:
        scored = [(s, *score_song(prefs, s, **kwargs)) for s in songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        print(f"\n  [{label}] Top 5:")
        for i, (s, score, _) in enumerate(scored[:5], 1):
            print(f"    {i}. {s['title']} [{s['genre']} / {s['mood']}]  score={score:.4f}")


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, prefs in PROFILES.items():
        recs = recommend_songs(prefs, songs, k=5)
        print_recommendations(name, recs)

    run_experiment(songs)


if __name__ == "__main__":
    main()
