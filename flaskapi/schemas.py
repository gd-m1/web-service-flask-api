import re
from marshmallow import Schema, fields, validates, ValidationError


class UserSchema(Schema):
    ROLES = ('author', 'editor')
    STATES = ('active', 'inactive', 'deleted')

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True)
    role = fields.Str(required=True)
    state = fields.Str(required=True)

    @validates('email')
    def validate_email(self, email):
        email_regex = re.compile(r'([a-zA-Z0-9._]+@+[a-zA-Z0-9]+(\.[a-zA-Z]{2,4}))')
        mo = email_regex.search(email)
        if not mo:
            raise ValidationError("Email is not valid! Try another one.")

    @validates('role')
    def validate_role(self, role):
        if role not in self.ROLES:
            raise ValidationError("Role is incorrect! Use one of: 'author', 'editor'")

    @validates('state')
    def validate_state(self, state):
        if state not in self.STATES:
            raise ValidationError("State is incorrect! Use one of: 'active', 'inactive', 'deleted'")


class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    author = fields.Int(required=True)


# Parameters validation
class ArgsSchema(Schema):
    ORDER_BY = ('name', 'last_name', 'email')

    offset = fields.Int()
    limit = fields.Int()
    order_by = fields.Str()
    id = fields.Int()
    email = fields.Str()
    name_substr = fields.Str()
    author = fields.Int()

    @validates('order_by')
    def validate_order(self, order_by):
        if order_by not in self.ORDER_BY:
            raise ValidationError("order_by is incorrect! Use one of: name, last_name, email")
