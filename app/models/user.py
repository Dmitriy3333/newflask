from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), default='user')
    name = db.Column(db.String(255))
    login = db.Column(db.String(40))
    password = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)
