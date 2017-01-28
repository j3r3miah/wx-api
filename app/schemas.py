from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    created_at = fields.DateTime()
