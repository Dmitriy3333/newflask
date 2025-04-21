from extensions import db

class SanatoriumPhoto(db.Model):
    __tablename__ = 'sanatorium_photos'

    id = db.Column(db.Integer, primary_key=True)

    sanatorium_id = db.Column(db.Integer, db.ForeignKey('sanatoriums.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)

    sanatorium = db.relationship('Sanatorium', backref='photos')