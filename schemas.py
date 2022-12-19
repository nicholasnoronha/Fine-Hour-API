from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()
    password = fields.String(required=True, load_only=True)
    email = fields.String(required=True)
    valor_hora = fields.Float()