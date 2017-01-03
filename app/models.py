from app import db

class Words(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    word = db.Column(db.String)

    def __repr__(self):
        return "<Word {}>".format(self.word)
