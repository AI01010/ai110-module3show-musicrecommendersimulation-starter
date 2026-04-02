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

- How many songs are in the catalog  10
- What genres or moods are represented genre: pop, rock, hip-hop, jazz, classical. moods: happy, sad, energetic, calm. energy: low, medium, high. artists: 10 different artists with varying popularity and styles. 
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  idk? 

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

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

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
