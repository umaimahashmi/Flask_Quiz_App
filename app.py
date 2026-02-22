import os
import random
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
import csv
import time

app = Flask(__name__, static_folder='static', template_folder='templates')
# use an environment variable for the secret key in a real deployment
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'change-me-to-a-secure-random-value')

# Flask-Session Configuration
app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem-based sessions
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
Session(app)

# Load MCQs from CSV
def load_mcqs(filename):
    """Load questions from a CSV file and return a list of MCQ dictionaries.

    If the CSV contains a "Subject" column it will be used; otherwise the
    subject is determined by position using :func:`identify_subject`.
    The function also supports optional shuffling via the environment
    variable ``SHUFFLE_QUESTIONS``.
    """
    mcqs = []
    path = os.path.join(os.path.dirname(__file__), filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"{filename} not found at {path}")

    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for index, row in enumerate(reader):
            subject = row.get('Subject') or identify_subject(index)
            mcq = {
                'number': index + 1,
                'question': row.get('Questions', '').strip(),
                'options': {
                    'A': row.get('A', '').strip(),
                    'B': row.get('B', '').strip(),
                    'C': row.get('C', '').strip(),
                    'D': row.get('D', '').strip()
                },
                'correct_option': row.get('Correct', '').strip().upper(),
                'subject': subject
            }
            mcqs.append(mcq)

    # shuffle if requested to make each run feel fresh
    if os.environ.get('SHUFFLE_QUESTIONS', 'False').lower() in ('1', 'true', 'yes'):
        random.shuffle(mcqs)
    return mcqs

# Identify subject based on index
def identify_subject(index):
    if index < 68:
        return 'Biology'
    elif index < 122:
        return 'Chemistry'
    elif index < 176:
        return 'Physics'
    elif index < 194:
        return 'English'
    else:
        return 'Logical Reasoning'

# Load MCQs
mcqs = load_mcqs('mcqs.csv')

@app.route('/')
def home():
    """Landing page with instructions and a start button."""
    # supply mcq count to show in instructions
    return render_template('index.html', mcqs=mcqs)


def init_scores():
    """Compute the total number of questions per subject and initialise a score dictionary."""
    totals = {}
    for mcq in mcqs:
        totals[mcq['subject']] = totals.get(mcq['subject'], 0) + 1
    return {sub: {'correct': 0, 'total': totals[sub]} for sub in totals}


@app.route('/begin', methods=['POST'])
def begin():
    """Initialize or reset the quiz state and jump to the first question."""
    session.clear()
    session['start_time'] = time.time()
    session['mcq_index'] = 0
    session['answers'] = []
    session['skipped_mcqs'] = []
    session['scores'] = init_scores()
    return redirect(url_for('show_mcq'))


@app.route('/restart')
def restart():
    """Convenience route to go back to landing page."""
    return redirect(url_for('home'))


@app.route('/mcq')
def show_mcq():
    # ensure quiz was started
    if 'start_time' not in session:
        return redirect(url_for('home'))

    index = session.get('mcq_index', 0)
    skipped_mcqs = session.get('skipped_mcqs', [])
    error = session.pop('error', None)

    elapsed_time = time.time() - session['start_time']
    if elapsed_time > 600:  # ten minutes
        flash('Time is up!', 'warning')
        return redirect(url_for('results'))

    mcq = None
    if index < len(mcqs):
        mcq = mcqs[index]
    elif skipped_mcqs:
        mcq_index = skipped_mcqs.pop(0)
        session['skipped_mcqs'] = skipped_mcqs
        session['mcq_index'] = mcq_index
        mcq = mcqs[mcq_index]
    else:
        return redirect(url_for('results'))

    progress = int((index / len(mcqs)) * 100) if mcqs else 0
    return render_template('mcq.html', mcq=mcq, elapsed_time=elapsed_time, error=error, progress=progress)





@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    answer = request.form.get('answer')
    if not answer:
        flash('Please select an option before proceeding.', 'danger')
        return redirect(url_for('show_mcq'))

    index = session.get('mcq_index', 0)
    if index < len(mcqs):
        mcq = mcqs[index]
        correct_option = mcq['correct_option']
        user_answer = answer.strip().upper()

        if user_answer == correct_option:
            session['scores'][mcq['subject']]['correct'] += 1

        skipped_mcqs = session.get('skipped_mcqs', [])
        if index in skipped_mcqs:
            skipped_mcqs.remove(index)
            session['skipped_mcqs'] = skipped_mcqs

        session['answers'].append((mcq, user_answer))
        session['mcq_index'] += 1

    return redirect(url_for('show_mcq'))


@app.route('/skip_mcq', methods=['POST'])
def skip_mcq():
    index = session.get('mcq_index', 0)
    if index < len(mcqs):
        skipped_mcqs = session.get('skipped_mcqs', [])
        if index not in skipped_mcqs:
            skipped_mcqs.append(index)
            session['skipped_mcqs'] = skipped_mcqs
        session['mcq_index'] += 1
        flash('Question skipped; you can review it later.', 'info')
    return redirect(url_for('show_mcq'))

@app.route('/results')
def results():
    scores = session.get('scores', {})
    total_correct = sum(score['correct'] for score in scores.values())
    total_questions = sum(score['total'] for score in scores.values())
    answers = session.get('answers', [])
    percentages = {sub: (score['correct'] / score['total'] * 100 if score['total'] else 0)
                   for sub, score in scores.items()}
    return render_template('results.html', scores=scores, percentages=percentages,
                           total_correct=total_correct, total_questions=total_questions,
                           answers=answers, mcqs=mcqs)

if __name__ == '__main__':
    app.run(debug=True)
