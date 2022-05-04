from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

user_schema = {
    "type":"object",
    "properties":{
        "first_name":{
            "type":"string",
        },
        "last_name":{
            "type":"string",
        },
        "email":{
            "type":"string",
            "format":"email"
        },
        "password":{
            "type":"string",
            "minLenth":"5"
        }
    },
    "required":["email","password"],
    "additionalProperties": False
}

reset_password_schema ={
    "type":"object",
    "properties":{
        "email":{
            "type":"string",
            "format":"email"
        }
    },
    "required":["email"],
    "additionalProperties": False
}

def validate_user_form(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}

def validate_reset_password_form(data):
    try:
        validate(data, reset_password_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
