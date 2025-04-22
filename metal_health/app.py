from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from dotenv import load_dotenv
import os
import requests
import json
import joblib
import pandas as pd

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "default-secret")

# API Keys & Config
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Models
student_model = joblib.load("models/Sahasya_model_2_SVM.pkl")
working_model = joblib.load("models/Sahasya_model_1_Decision.pkl")

PREDICTION_LABELS = {
    1: "No Depression",
    2: "Minimal Depression",
    3: "Moderate Depression",
    4: "Severe Depression"
}

# === Routes ===

@app.route('/')
def login():
    return render_template('login_page.html')

@app.route('/login', methods=['POST'])
def login_submit():
    email = request.form.get('email')
    password = request.form.get('password')
    users = session.get('users', {})
    user = users.get(email)

    if user and user['password'] == password:
        session['user'] = email
        session['name'] = user['name']
        session['age'] = user['age']
        session['gender'] = user['gender']
        return redirect(url_for('about'))

    flash("Login failed: Invalid credentials.", "danger")
    return redirect(url_for('login'))

@app.route('/chat', methods=['POST'])
def chat():
    if 'user' not in session:
        return jsonify({"response": "Unauthorized"}), 401
    
    user_input = request.json.get('message')
    try:
        bot_response = get_chat_response(user_input)
        return jsonify({"response": bot_response})
    except Exception as e:
        print("Chat Error:", e)
        return jsonify({"response": "Sorry, something went wrong."}), 500

@app.route('/home')
def home():
    if 'user' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/about')
def about():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('homepage.html')

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_submit():
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    name = request.form.get('name')
    age = request.form.get('age')
    gender = request.form.get('gender')

    if password != confirm_password:
        flash("Passwords do not match", "error")
        return redirect(url_for('register'))

    users = session.get('users', {})
    if email in users:
        flash("Email already registered", "error")
        return redirect(url_for('register'))

    users[email] = {
        'password': password,
        'name': name,
        'age': age,
        'gender': gender
    }
    session['users'] = users
    flash("Registration successful! Please login.", "success")
    return redirect(url_for('login'))

@app.route('/start')
def start():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('frontpage.html')

@app.route('/quiz_intro')
def quiz_intro():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('quiz_intro.html')

@app.route('/category', methods=['GET', 'POST'])
def category():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        session['category'] = request.form.get('category')
        if session['category'] == 'student':
            return redirect(url_for('s_analysis'))
        return redirect(url_for('wp_analysis'))
    return render_template('category.html')

@app.route('/s_analysis', methods=['GET', 'POST'])
def s_analysis():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        answers = json.loads(request.form.get('answers'))
        prediction = student_model.predict(pd.DataFrame([answers]))[0]
        session['prediction'] = int(prediction)
        return redirect(url_for('result'))
    return render_template('s_analysis.html')

@app.route('/wp_analysis', methods=['GET', 'POST'])
def wp_analysis():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        answers = json.loads(request.form.get('answers'))
        prediction = working_model.predict(pd.DataFrame([answers]))[0]
        session['prediction'] = int(prediction)
        return redirect(url_for('working_result'))
    return render_template('wp_analysis.html')

@app.route('/result')
def result():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    prediction_text = PREDICTION_LABELS.get(session.get('prediction'), "Unknown")
    return render_template('result.html', prediction=prediction_text)

@app.route('/working_result')
def working_result():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    prediction_text = PREDICTION_LABELS.get(session.get('prediction'), "Unknown")
    return render_template('workingresult.html', prediction=prediction_text)

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

def get_chat_response(message):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{
            "role": "system",
            "content": "Your name is Sahasya. You are a compassionate mental health assistant. Provide emotional support and coping strategies."
        }, {
            "role": "user", 
            "content": message
        }]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

if __name__ == '__main__':
    app.run()

