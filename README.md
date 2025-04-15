# Flask Online Quiz App

A simple web application where users can register, log in, create quizzes, take quizzes, and see results.

## How to Run

```bash
git clone https://github.com/Shahriark369/quizapp.git
cd quizapp
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python
>>> from app import db
>>> db.create_all()
>>> exit()
python run.py

---

## 🔹 ৪. `app/__init__.py`

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
db = SQLAlchemy(app)

from app import routes

