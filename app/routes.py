from flask import render_template, redirect, url_for, request, session
from app import app, db
from app.models import User, Quiz, Question
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    quizzes = Quiz.query.filter_by(creator_id=session['user_id']).all()
    return render_template('dashboard.html', quizzes=quizzes)

@app.route('/create_quiz', methods=['GET', 'POST'])
def create_quiz():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        quiz = Quiz(title=title, creator_id=session['user_id'])
        db.session.add(quiz)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('create_quiz.html')

@app.route('/quiz/<int:quiz_id>/add_question', methods=['POST'])
def add_question(quiz_id):
    question = Question(
        question_text=request.form['question_text'],
        option_a=request.form['option_a'],
        option_b=request.form['option_b'],
        option_c=request.form['option_c'],
        option_d=request.form['option_d'],
        correct_answer=request.form['correct_answer'],
        quiz_id=quiz_id
    )
    db.session.add(question)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    if request.method == 'POST':
        score = 0
        for q in questions:
            answer = request.form.get(str(q.id))
            if answer == q.correct_answer:
                score += 1
        return render_template('result.html', score=score, total=len(questions))
    return render_template('take_quiz.html', quiz=quiz, questions=questions)

