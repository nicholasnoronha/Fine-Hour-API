from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    qtd_horas = db.Column(db.Float(2))
    valor_horas = db.Column(db.Float(2))

    tasks = db.relationship("TaskModel", back_populates="user", lazy="dynamic")