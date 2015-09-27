from app import db
from datetime import datetime

class gs_repositoryAccessed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(64), index=True, unique=True)
    acessDate = db.Column(db.DateTime)


    #def __repr__(self):
    #    return '<User %r>' % (self.nickname)