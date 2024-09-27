from datetime import datetime

# Define Ragas with their corresponding time
ragas = {
    "Raga Yaman": "Evening",
    "Raga Bhimpalasi": "Afternoon",
    "Raga Desh": "Night",
    "Raga Todi": "Morning",
    "Raga Bageshree": "Night",
}

# Get current time of the day
def get_time_of_day():
    now = datetime.now()
    current_hour = now.hour

    if 5 <= current_hour < 12:
        return "Morning"
    elif 12 <= current_hour < 17:
        return "Afternoon"
    elif 17 <= current_hour < 21:
        return "Evening"
    else:
        return "Night"

# Recommend a raga based on time
def recommend_raga():
    time_of_day = get_time_of_day()
    recommended_ragas = [raga for raga, time in ragas.items() if time == time_of_day]
    
    if recommended_ragas:
        return f"Recommended Raga for {time_of_day}: {', '.join(recommended_ragas)}"
    else:
        return "No raga available for this time."

# Main execution
if __name__ == "__main__":
    print(recommend_raga())
