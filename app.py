from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Replace with your actual YouTube API key
YOUTUBE_API_KEY = 'AIzaSyC_hnbpQleyqWxzTFPGwhJAHYdcLSHv_88'

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/chatbot')
def chatbot():
    return render_template("chatbot.html")

@app.route('/strength')
def strength():
    return render_template("strength.html")

@app.route('/hypertrophy')
def hypertrophy():
    return render_template("hypertrophy.html")

@app.route('/fat')
def fat():
    return render_template("fat.html")

@app.route('/submit_details', methods=['POST'])
def submit_details():
    user_details = request.json
    # Store user details in session or database if needed
    # For simplicity, we will just return the details
    return jsonify(user_details)

@app.route('/get_workout_plan', methods=['POST'])
def get_workout_plan():
    data = request.json
    user_query = data['query']
    user_details = data['details']

    # Here you would typically call your LLM to get a workout plan based on user_query and user_details
   # workout_plan = f"Workout plan for {user_details['goal']} based on your details."

    # Use the YouTube API to fetch workout videos related to the workout plan
    youtube_search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q={"strength training"} workout&key={YOUTUBE_API_KEY}"
    response = requests.get(youtube_search_url)
    videos = response.json().get('items', [])

    video_links = []
    for video in videos:
        video_title = video['snippet']['title']
        video_id = video['id'].get('videoId')
        video_description = video['snippet']['description']
        video_thumbnail = video['snippet']['thumbnails']['medium']['url']  # Use medium thumbnail

        if video_id:
            video_links.append(f"""
                <div>
                    <h3>{video_title}</h3>
                    <p>{video_description}</p>
                    <img src="{video_thumbnail}" alt="{video_title}" style="width: 320px; height: 180px;">
                    <a href='https://www.youtube.com/watch?v={video_id}' target='_blank'>Watch Video</a>
                </div>
                <hr>
            """)

    return jsonify({
        'workoutPlan': "<br>" + "<br>".join(video_links)
    })

if __name__ == "__main__":
    app.run(debug=True)

# Ensure to replace 'YOUR_YOUTUBE_API_KEY' with your actual YouTube API key.
# This code will now collect user details, process queries, and fetch workout plans with YouTube video links.