import django
from django.core.validators import BaseValidator
from django.core.exceptions import ValidationError

import jsonschema
import jsonschema.exceptions

class JSONSchemaValidator(BaseValidator):
    def compare(self, input_value, schema):
        # print(schema)
        try:
            jsonschema.validate(input_value, schema)
        except jsonschema.exceptions.ValidationError:
            raise ValidationError('%(value)s failed JSON schema check', params={'value':input_value})
        

