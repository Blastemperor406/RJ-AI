# scoring.py
from datetime import datetime

# Define song mood impact scores, ranging from -1 (Very Sad) to 1 (Very Happy)
song_moods = {
    "Very Happy": 1.0,
    "Happy": 0.5,
    "Neutral": 0.0,
    "Sad": -0.5,
    "Very Sad": -1.0
}

def calculate_mood_score(cur_mood, song_mood):
    """
    Calculate mood score based on the closeness of cur_mood to the song's intended mood.

    Parameters:
    - cur_mood (float): The user's current mood, ranging from -1 (Very Sad) to 1 (Very Happy).
    - song_mood (str): The mood tag for the song, as per song_moods dictionary.

    Returns:
    - float: A score indicating how well the song's mood matches the user's mood.
    """
    if song_mood in song_moods:
        # Calculate mood match score based on the distance between user mood and song mood
        mood_diff = abs(cur_mood - song_moods[song_mood])
        mood_score = max(0, 5 - (mood_diff * 5))  # Scale difference into a score out of 5
        return mood_score
    return 0  # Default score if song mood is not recognized


# weather_scores = {
#     "Warm and Sunny song": {"Warm and Sunny": 5, "Rainy and Overcast": -2, "Cold and Windy": -2, "Any weather": 3, "No specific suitability": 0},
#     "Rainy and Overcast song": {"Warm and Sunny": -2, "Rainy and Overcast": 5, "Cold and Windy": 3, "Any weather": 3, "No specific suitability": 0},
#     "Cold and Windy song": {"Warm and Sunny": -2, "Rainy and Overcast": 3, "Cold and Windy": 5, "Any weather": 3, "No specific suitability": 0},
#     "Any weather": {"Warm and Sunny": 3, "Rainy and Overcast": 3, "Cold and Windy": 3, "Any weather": 5, "No specific suitability": 0},
#     "No specific suitability": {"Warm and Sunny": 0, "Rainy and Overcast": 0, "Cold and Windy": 0, "Any weather": 0, "No specific suitability": 0}
# }

def calculate_weather_score(weather_suitability, temperature, precipitation, cloud_cover):
    """
    Calculate weather-based score for a song based on the current weather conditions.
    
    Parameters:
    - weather_suitability (str): Weather suitability of the song.
    - temperature (float): Current temperature in Celsius.
    - precipitation (float): Current precipitation in mm.
    - cloud_cover (float): Current cloud cover as a fraction (0 to 1).
    
    Returns:
    - int: Score based on the match of song's weather suitability and current weather.
    """
    score = 0
    # cloud_percentage = cloud_cover * 100  # Convert fraction to percentage for easier comparison

    if weather_suitability == "Warm and Sunny song":
        if temperature > 20 and precipitation < 1 and cloud_cover < 30:
            score += 5
        elif temperature > 15 and cloud_cover < 50:
            score += 3

    elif weather_suitability == "Rainy and Overcast song":
        if 10 <= temperature <= 20 and precipitation > 2 and cloud_cover > 60:
            score += 5
        elif precipitation > 1 and cloud_cover > 50:
            score += 3

    elif weather_suitability == "Cold and Windy song":
        if temperature < 10 and cloud_cover > 50:
            score += 5
        elif temperature < 15:
            score += 3

    elif weather_suitability == "Any weather":
        score += 3  # This song is suitable for any weather

    elif weather_suitability == "No specific suitability":
        score += 1  # Minimal impact from weather conditions

    return score


# def calculate_mood_score(cur_mood, row):
#     """Calculate score based on the current mood and row's mood."""
#     if cur_mood in mood_scores:
#         return mood_scores[cur_mood].get(row['Mood'], 0)  # Default score is 0 if Mood not found
#     return 0  # Default score if current mood is not recognized

# def calculate_weather_score(cur_weather, row):
#     """Calculate score based on the current weather and row's weather suitability."""
#     if row['Weather Suitability'] in weather_scores:
#         return weather_scores[row['Weather Suitability']].get(cur_weather, 0)  # Default score is 0 if Weather not found
#     return 0

def assign_score(row, cur_mood, temp, prec, cloud):
    """Assign a score to the song based on mood,weather and time."""
    score = 0
    score += calculate_mood_score(cur_mood, row['Mood'])
    # score +=calculate_weather_score(cur_weather,row)
    score += calculate_weather_score(row['Weather Suitability'], temp, prec, cloud)


    current_hour = datetime.now().hour

    # Score based on time of day
    if 0 <= current_hour < 4 and row['Time'] == "late night song":
        score += 5
    elif 4 <= current_hour < 8 and row['Time'] == "morning song":
        score += 5
    elif 8 <= current_hour < 12 and row['Time'] == "afternoon song":
        score += 5
    elif 12 <= current_hour < 16 and row['Time'] == "evening song":
        score += 2  # Less suitable for evening songs
    elif 16 <= current_hour < 20 and row['Time'] == "evening song":
        score += 5
    elif 20 <= current_hour < 24 and row['Time'] == "late night song":
        score += 5

    return score