from flask import render_template
from app import app, db, models
import json

@app.route('/')
@app.route('/index')
def index():
    # obtain today's words
    # words = models.Words.query.all()
    # words = list((str(word[0]), word[1]) for word in db.session.query(models.Words, db.func.count(models.Words.id).label("total")).group_by(models.Words.word).order_by("total DESC"))
    data = db.session.query(models.Words, db.func.count(models.Words.id).label("total")).group_by(models.Words.word).order_by("total DESC").all()[:50]
    words = [_[0].word for _ in data]
    count = [_[1] for _ in data]
    return render_template('index.html', words=words, count = count)