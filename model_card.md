# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  This is a recommendation engine for users to find songs based on their preferences. 
It is intended to store information and improve recommendations over time based on 4 key features: 
genre, mood, energy, and artist. 
This is for a single user so no collaborative filtering or popularity metrics are available. This is for classroom exploration only, not for real users.

- What kind of recommendations does it generate: top 3-10 songs
- What assumptions does it make about the user: they like listing to music and have preferences for genre, mood, energy, and artist if they listen to them a lot 
- Is this for real users or classroom exploration: both   

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  genre is the most important factor, followed by mood, energy, and artist. 
The model calculates a score for each song based on how well it matches the user's preferences.
each feature has a score from 0 to 1, and the final score is a weighted average of these feature scores.
The weights are: genre (0.4), mood (0.3), energy (0.2), artist (0.1).
If a user has a strong preference for a specific genre, mood, artist, or energy level, songs in that category will score higher (higher weight).
add in a random factor to introduce some variability in the recommendations, so the same user might get slightly different suggestions each time they run the recommender. Increase its weight if the user selects a random song instead of a recommended one.

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog: Started with 10, expanded to 100.
- What genres or moods are represented: Genres include pop, rock, hip-hop, jazz, classical, r&b, edm, country, folk, metal, soul, latin, reggae, synthwave, lofi, ambient, indie pop, indie rock, and jazz-fusion. Moods include happy, sad, intense, chill, focused, relaxed, moody, romantic, nostalgic, melancholic, confident, euphoric, and aggressive.
- Did I add or remove data: Added 90 songs. The original 10 were not enough to test anything meaningful across different user types.
- Are there parts of musical taste missing: Quite a bit actually. No lyric themes, no release era, no language tags, no sub-genre detail. Also no popularity score, so a viral hit and an obscure track are treated the same.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

- The genre weight (0.40) is the strongest factor. A user who likes one pop song will keep getting pop recs even when a different genre matches their mood better. Classic filter bubble.
- Conflicting preferences break the scoring. A "sad high energy" user gets a low-energy sad song at #1 because the mood match (0.30) overrides the energy gap. The weights have no way to handle contradictions.
- Niche genres like jazz-fusion only have 1 song in the catalog, so after #1 the system just falls back to mood-matching across completely unrelated genres.
- No artist diversity penalty. If one artist has multiple high-scoring songs they can dominate the entire top 5.
- Energy scoring uses a single target value. Users who like both very high and very low energy music get stuck with mid-energy recs that don't actually fit either preference.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

Tested 6 profiles total: 3 normal (Happy Pop Fan, Chill Lofi Study, High Energy Rock) and 3 adversarial (Sad High Energy, Acoustic Soul Night, Genre Wildcard).

The normal profiles all behaved as expected. A genre and mood double match scored around 0.92 and landed at #1. Spots 2-5 were all same-genre songs scoring around 0.60.
The adversarial profiles showed some real problems. Sad High Energy was the most surprising: a low-energy sad hip-hop song ranked #1 even though the target energy was 0.90. The mood match just overrode the energy gap. Genre Wildcard had a big score cliff: #1 was 0.95, but #2 dropped to 0.51 because there was only one song in that genre.
Also ran a weight shift experiment: halved genre weight (0.40 to 0.20) and doubled energy weight (0.20 to 0.40). The #1 result still didn't change. Weights alone don't seem to fix the filter bubble issue.
Wrote 39 unit tests on score_song, recommend_songs, load_songs, custom weight params, edge cases, and the OOP Recommender class. All passing.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
