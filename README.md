# Sahasya: Mental Health Support Platform

**Sahasya** is a web-based platform that offers mental health support through a compassionate chatbot, personalized depression analysis for students and working professionals, and a responsive user interface. The project is built using Flask, machine learning models, and integrates the OpenRouter API for chatbot responses.

---

## 🚀 Features

- 🔐 **User Registration & Login** – Secure, session-based authentication.
- 💬 **Chatbot** – Empathetic, supportive conversation using OpenRouter API.
- 📊 **Depression Analysis** – Separate quizzes and ML models for students and professionals.
- 🧑‍💻 **Personalized Dashboard** – Displays user profile and quiz results.
- 📱 **Responsive Design** – Optimized for both desktop and mobile.

---

## 🛠️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/sahasya.git
cd sahasya
```

### 2. Install Dependencies

Ensure you have Python 3.9+ and pip installed.

```bash
pip install -r requirements.txt
```

### 3. Prepare the Environment

Create a `.env` file in the project root with the following content:

```
OPENROUTER_API_KEY=your_openrouter_api_key_here
FLASK_SECRET=your_flask_secret_key_here
```

- Get your OpenRouter API key from [OpenRouter](https://openrouter.ai/)
- Use a strong, random string for `FLASK_SECRET`.

### 4. Add Machine Learning Models

Place your trained model files in the `models/` directory:

- `models/Sahasya_model_2_SVM.pkl` (for students)
- `models/Sahasya_model_1_Decision.pkl` (for working professionals)

---

## 🧪 Running the App Locally

```bash
python app.py
```

The app will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🚀 Deployment (Render)

1. **Push your code to GitHub.**
2. **Create a new Web Service on [Render](https://render.com/):**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
3. **Add Environment Variables in Render Dashboard:**
   - `OPENROUTER_API_KEY`
   - `FLASK_SECRET`
4. **Ensure `requirements.txt` includes `gunicorn`.**

---

## 📁 Project Structure

```
sahasya/
│
├── app.py
├── requirements.txt
├── .env
├── models/
│   ├── Sahasya_model_2_SVM.pkl
│   └── Sahasya_model_1_Decision.pkl
├── templates/
│   ├── login_page.html
│   ├── register.html
│   ├── homepage.html
│   ├── index.html
│   ├── frontpage.html
│   ├── quiz_intro.html
│   ├── category.html
│   ├── s_analysis.html
│   ├── wp_analysis.html
│   ├── result.html
│   └── workingresult.html
└── static/
    ├── css/
    ├── js/
    └── images/
```

---

## 📌 API & Model Notes

- **Chatbot:** Uses OpenRouter API (`openai/gpt-3.5-turbo` by default).
- **ML Models:** Trained using scikit-learn 1.5.2; ensure compatibility.

---

## 🧩 Troubleshooting

- **Chatbot not responding?**
  - Check `.env` values and ensure API key is active.
  - Check Render logs for runtime errors.
- **Login/Registration issues?**
  - Make sure session cookies are enabled in your browser.
- **Model errors?**
  - Verify the correct scikit-learn version and model file paths.

---

#### 🚀 Website live at https://sahasya-mental-health-assistant-rzdr.onrender.com

## 📜 License

This project is for educational purposes. If you wish to use or modify it, please credit the original authors.

