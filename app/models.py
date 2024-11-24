from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class APIResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lmk_key = db.Column(db.String(100))
    address1 = db.Column(db.String(255))
    address2 = db.Column(db.String(255))
    address3 = db.Column(db.String(255))
    postcode = db.Column(db.String(20))
    inspection_date = db.Column(db.String(20))
    uprn = db.Column(db.String(100))

class ScraperResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255))
    energy_rating = db.Column(db.String(5))
    valid_until = db.Column(db.String(20))
    expired = db.Column(db.String(10))
