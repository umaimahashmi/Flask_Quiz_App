# QuizApp

A lightweight Flask application that presents a timed multiple-choice question (MCQ) quiz.

## 🚀 Features

- 200 MCQs covering Biology, Chemistry, Physics, English, and Logical Reasoning
- 10-minute countdown timer with automatic submission on timeout
- Progress bar showing how many questions have been answered
- Skip questions and return later
- Results page with per-subject breakdown and answer key
- Bootstrap-based responsive UI with clean, professional styling
- Configurable behaviour via environment variables (shuffle questions, secret key)

## 🛠️ Installation

1. Clone the repository
   ```bash
   git clone https://github.com/umaimahashmi/QuizApp.git
   cd QuizApp
   ```
2. (Optional) create a virtual environment
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate  # macOS/Linux
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app
   ```bash
   flask run
   ```
   or
   ```bash
   python app.py
   ```

The application will be available at http://127.0.0.1:5000

## ⚙️ Configuration

Environment variables (you may create a `.env` file or copy `.env.example`):

- `FLASK_SECRET_KEY` – secret used to sign sessions (recommended in production)
- `SHUFFLE_QUESTIONS` – set to `1` / `true` to randomise question order each run
- `FLASK_APP` – name of the application script (usually `app.py`)
- `FLASK_ENV` – `development` or `production` environment

## 🧩 Customisation

- Add or modify questions in `mcqs.csv`. You can optionally include a `Subject` column to assign a subject explicitly.
- Styling can be adjusted via `static/css/style.css`.
- Templates live in `templates/` and can be extended or replaced.

## 📁 Project Structure

```
QuizApp/
├── app.py
├── mcqs.csv
├── requirements.txt
├── static/
│   └── css/style.css
└── templates/
    ├── base.html
    ├── index.html
    ├── mcq.html
    └── results.html