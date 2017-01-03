from flask import render_template
from app import app, db, models

@app.route('/')
@app.route('/index')
def index():
    # obtain today's words
    # words = models.Words.query.all()
    words = db.session.query(models.Words, db.func.count(models.Words.id).label("total")).group_by(models.Words.word).order_by("total DESC")
    return render_template('index.html', words=words)