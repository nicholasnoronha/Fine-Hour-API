from db import db

class BlocklistModel(db.Model):
    __tablename__ = "blocklist"

    id = db.Column(db.Integer, primary_key=True)
    token_jti = db.Column(db.String(256), nullable=False)