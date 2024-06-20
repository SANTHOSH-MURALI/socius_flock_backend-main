from marshmallow import Schema, fields


class Login(Schema):
  email = fields.Email()
  password = fields.String(required=True)