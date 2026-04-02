"""
Command line runner for the Music Recommender Simulation.
Run with: python -m src.main
"""

from src.recommender import load_songs, recommend_songs


PROFILES = {
    "Happy Pop Fan":    {"genre": "pop",      "mood": "happy",      "energy": 0.82},
    "Chill Lofi Study": {"genre": "lofi",     "mood": "chill",      "energy": 0.38},
    "High Energy Rock": {"genre": "rock",     "mood": "intense",    "energy": 0.92},
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


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, prefs in PROFILES.items():
        recs = recommend_songs(prefs, songs, k=5)
        print_recommendations(name, recs)


if __name__ == "__main__":
    main()
