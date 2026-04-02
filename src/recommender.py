import csv
import random
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its attributes. Required by tests/test_recommender.py"""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences. Required by tests/test_recommender.py"""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP implementation of the recommendation logic. Required by tests/test_recommender.py"""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score every song against the user profile and return the top k sorted by score."""
        scored = []
        for song in self.songs:
            score, _ = _score_song_oop(user, song)
            scored.append((score, song))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        _, reasons = _score_song_oop(user, song)
        return " | ".join(reasons) if reasons else "no strong match found"


def _score_song_oop(user: UserProfile, song: Song) -> Tuple[float, List[str]]:
    """
    Compute a weighted score for a Song against a UserProfile.
    Weights: genre 0.40, mood 0.30, energy 0.20, acoustic 0.10.
    """
    score = 0.0
    reasons = []

    if song.genre == user.favorite_genre:
        score += 0.40
        reasons.append(f"genre match: {song.genre} (+0.40)")

    if song.mood == user.favorite_mood:
        score += 0.30
        reasons.append(f"mood match: {song.mood} (+0.30)")

    energy_sim = 1.0 - abs(song.energy - user.target_energy)
    energy_contrib = round(energy_sim * 0.20, 4)
    score += energy_contrib
    reasons.append(f"energy {song.energy:.2f} vs target {user.target_energy:.2f} (+{energy_contrib:.2f})")

    if user.likes_acoustic and song.acousticness > 0.6:
        score += 0.10
        reasons.append(f"acoustic match: acousticness={song.acousticness:.2f} (+0.10)")

    return round(score, 4), reasons


# ── Functional interface (used by main.py) ────────────────────────────────────

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with numeric fields cast."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"]           = int(row["id"])
            row["energy"]       = float(row["energy"])
            row["tempo_bpm"]    = float(row["tempo_bpm"])
            row["valence"]      = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """
    Score a single song dict against user_prefs dict.
    user_prefs keys: genre, mood, energy, artist (optional).
    Returns (score, reasons_string).
    Weights: genre 0.40, mood 0.30, energy 0.20, artist 0.10, random jitter up to 0.05.
    """
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        score += 0.40
        reasons.append(f"genre match: {song['genre']} (+0.40)")

    if song["mood"] == user_prefs.get("mood"):
        score += 0.30
        reasons.append(f"mood match: {song['mood']} (+0.30)")

    target_energy = user_prefs.get("energy", 0.5)
    energy_sim = 1.0 - abs(song["energy"] - target_energy)
    energy_contrib = round(energy_sim * 0.20, 4)
    score += energy_contrib
    reasons.append(f"energy {song['energy']:.2f} vs target {target_energy:.2f} (+{energy_contrib:.2f})")

    if user_prefs.get("artist") and song["artist"] == user_prefs["artist"]:
        score += 0.10
        reasons.append(f"favorite artist: {song['artist']} (+0.10)")

    jitter = random.uniform(0, 0.05)
    score = round(score + jitter, 4)

    return score, " | ".join(reasons)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, sort by score descending, and return the top k as (song, score, reasons)."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
