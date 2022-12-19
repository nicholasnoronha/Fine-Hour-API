from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    qtd_horas = db.Column(db.Integer)
    valor_horas = db.Column(db.Float(2))