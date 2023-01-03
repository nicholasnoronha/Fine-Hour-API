from marshmallow import Schema, fields

class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()
    password = fields.String(required=True, load_only=True)
    email = fields.String(required=True)
    valor_hora = fields.Float()

class PlainTaskSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    description = fields.String()
    hours_spent = fields.Float()
    created_at = fields.Date(required=True)


class UserSchema(PlainUserSchema):
    tasks = fields.List(fields.Nested(PlainTaskSchema(), dump_only=True))

class TaskSchema(PlainTaskSchema):
    user_id = fields.Int(required=True, load_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)

class JtiSchema(Schema):
    id = fields.Int(dump_only=True)
    token_jti = fields.String()