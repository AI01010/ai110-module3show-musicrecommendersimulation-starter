# Profile Comparison Reflections

## Happy Pop Fan vs Chill Lofi Study
Both got a clear #1 with a genre and mood double match scoring around 0.92-0.93.
The difference was spots 2-5. Pop fan got a mix of pop songs with different moods. Lofi fan got all lofi songs because the catalog has enough variety there.
Both basically showed the filter bubble in action. Once you match the genre, you stay in that genre for the whole list. It never crosses over even if a song from a different genre would match the mood just as well.

## Happy Pop Fan vs High Energy Rock
Similar score shape at #1 (around 0.92), but rock's #2-5 were closer together in score because rock songs in the catalog have pretty similar energy levels.
Pop's #2-5 spread out more because pop songs have a wider energy range. So if a genre has songs clustered around similar features, the top 5 ends up feeling more repetitive.

## Chill Lofi Study vs Classical Background
Both are low-energy profiles (lofi target=0.38, classical target=0.20) but they felt completely different in output.
Lofi gave back study-vibe tracks. Classical gave back slow, acoustic pieces.
The interesting part was that classical's #2 and #3 were within 0.002 of each other in score. Three classical songs had almost identical energy near 0.20, so the only thing separating them was random jitter. When songs are too similar, the ranking is basically random.

## Sad High Energy vs Hip-Hop Confident
Most informative pair. Confident got exactly what I expected: high-energy confident hip-hop in the top 2.
Sad High Energy got a low-energy sad song at #1 (score 0.82). The mood match (0.30) just dominated. The energy gap was 0.45 points but only translated to about 0.09 in score difference, not enough to beat the mood bonus.
So genre and mood together are almost a guaranteed win, and energy ends up as more of a tiebreaker. That's a problem when the energy target is supposed to be the whole point for that user.

## Acoustic Soul Night vs Genre Wildcard
Both are niche genre profiles but they behaved differently.
Soul had 3 songs so the top 3 were all soul. Then #4-5 fell to r&b and jazz based on mood match. Genre Wildcard (jazz-fusion) had only 1 song. #1 scored 0.91, then #2 dropped to 0.49. That's a massive score cliff. The system is entirely dependent on catalog size per genre. One song in a genre and it's basically useless after that first recommendation.

## Metal Head vs High Energy Rock
These look similar on paper: both high energy with aggressive or intense moods. But they produced completely different lists.
Metal stayed strictly in metal. Rock stayed strictly in rock. No overlap at all, even though a rock/aggressive song would logically appeal to a metal fan. The system has zero cross-genre awareness. The genre key has to match exactly or the song won't surface.

## EDM Rave vs Synthwave Night Drive
Both electronic profiles but they split cleanly. EDM got high-BPM euphoric tracks in the 0.92-0.97 energy range. Synthwave got lower-energy moody tracks in the 0.70-0.85 range.
The score gap between #1 and #2 was smaller for EDM (0.94 vs 0.91) because two euphoric EDM songs qualified about equally. Synthwave had only one moody synthwave song so #1 was clearly ahead. More songs with the same mood means tighter competition at the top.

## Genre Not In Catalog vs Total Mismatch
Genre not in catalog still got usable recs around 0.50 because mood matching kept it afloat.
Total mismatch got around 0.24, which is basically just ranking by energy proximity. Comparing the two makes it clear that mood match is what saves a bad genre request. Without it, the system just ranks by energy, which doesn't really mean anything on its own.

## Floor Energy vs Ceiling Energy
Both worked fine with no crashes, but there's an interesting asymmetry.
Floor (0.01) songs in the catalog had energy values between 0.18-0.32, so the energy penalty was still 0.14-0.16.
Ceiling (0.99) songs had values of 0.94-0.98, so the penalty was only 0.01-0.06.
High-energy users get slightly better energy scores than low-energy users just because the catalog skews toward higher-energy songs overall. It's a subtle data bias built into the catalog itself.

## Artist Superfan vs Happy Pop Fan
Same genre, mood, and energy but the superfan adds the artist bonus for Neon Echo.
The result was predictable. Sunrise City scored 1.045 instead of around 0.92, putting it past 1.0. Everything else in the top 5 was identical.
The artist bonus works as intended, but it exposed that the scoring has no cap. In a real system you would want to normalize scores to stay between 0 and 1 so they are easier to compare and explain.
