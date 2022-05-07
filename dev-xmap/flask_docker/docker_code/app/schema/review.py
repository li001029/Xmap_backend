
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

review_schema = {
    "type":"object",
    "properties":{
        "rating":{
            "type":"integer",
        },
        "activity_date":{
            "type":"string",
            "format":"date"
        },
        "comment":{
            "type":"string"
        },
        "park_id":{
            "type":"integer"
        },
        "tags":{
            "type":"array"
        },
        "activity_type":{
            "type":"string"
        }
        
    },
    "required":["activity_date","rating","park_id"],
    "additionalProperties": False
}

def validate_review(data):
    try:
        validate(data, review_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
