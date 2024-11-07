from data import load_songs_data
from scoring import assign_score
from cooldown import CooldownManager

def recommend_songs(songs_df, cur_mood, temp, prec, cloud, num_recommendations=5):
    """Recommend songs based on current mood and manage cooldown."""
    cooldown_manager = CooldownManager()
    recommendations = []

    # Calculate scores for each song
    songs_df['Score'] = songs_df.apply(lambda row: assign_score(row, cur_mood, temp, prec, cloud), axis=1)

    # Sort songs by score in descending order
    sorted_songs = songs_df.sort_values(by='Score', ascending=False)

    # Recommend songs while respecting cooldown
    for _, row in sorted_songs.iterrows():
        song = row["Title"]
        if cooldown_manager.add_song(song):
            recommendations.append((song+" by " +row["Singer"]))
            if len(recommendations) == num_recommendations:
                break

    return recommendations

if __name__ == "__main__":
    # Load the song data
    songs_df = load_songs_data("music_data.csv")

    # Set current mood
    cur_mood = "Sad"  # Example mood

    # Set current Weather
    # cur_weather = "Rainy and Overcast song"
    temp = 30
    prec = 1
    cloud = 35

