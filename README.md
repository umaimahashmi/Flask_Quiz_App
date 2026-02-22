# QuizApp

A lightweight Flask application that presents a timed multiple-choice question (MCQ) quiz.

## Features

- 200 MCQs covering Biology, Chemistry, Physics, English, and Logical Reasoning
- 10-minute countdown timer with automatic submission on timeout
- Progress bar showing how many questions have been answered
- Skip questions and return later
- Results page with per-subject breakdown and answer key
- Bootstrap-based responsive UI with clean, professional styling
- Configurable behaviour via environment variables (shuffle questions, secret key)

## Configuration

Environment variables (you may create a `.env` file or copy `.env.example`):

- `FLASK_SECRET_KEY` – secret used to sign sessions (recommended in production)
- `SHUFFLE_QUESTIONS` – set to `1` / `true` to randomise question order each run
- `FLASK_APP` – name of the application script (usually `app.py`)
- `FLASK_ENV` – `development` or `production` environment
