from marshmallow import Schema, fields


class SigUp(Schema):
  name = fields.String(required=True)
  email = fields.Email()
  password = fields.String(required=True)