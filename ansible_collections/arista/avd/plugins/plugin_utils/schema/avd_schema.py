from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json
import jsonschema.validators
import jsonschema._validators
import jsonschema._types
import jsonschema
from deepmerge import always_merger


# TODO import this from utils when python pr merges
class AristaAvdError(Exception):
    def __init__(self, message="An Error has occured in an arista.avd plugin"):
        self.message = message
        super().__init__(self.message)


class AvdSchemaError(AristaAvdError):
    pass


class AvdValidationError(AristaAvdError):
    pass


script_dir = os.path.dirname(__file__)
with open(f"{script_dir}/avd_meta_schema.json", "r", encoding="utf-8") as file:
    AVD_META_SCHEMA = json.load(file)


DEFAULT_SCHEMA = {
    "type": "dict",
    "allow_other_keys": True,
}


def _primary_key_validator(validator, primary_key, instance, schema):
    if not validator.is_type(primary_key, "str"):
        return

    if not validator.is_type(instance, "list"):
        return

    if not all(validator.is_type(element, "dict") for element in instance):
        return

    if not all(element.get(primary_key) for element in instance):
        yield jsonschema.ValidationError(f"Primary key '{primary_key}' is not set on all items as required.")

    if len(set([element.get(primary_key) for element in instance])) < len(instance):
        yield jsonschema.ValidationError(f"Value of Primary key '{primary_key}' is not unique as required.")


def _keys_validator(validator, keys, instance, schema):
    '''
    This function validates each key with the relevant subschema
    It also includes various child key validations,
    which can only be implemented with access to the parent "keys" instance.
    - Validate "allow_other_keys" (default is false)
    - Validate "required" under child keys
    '''
    if not validator.is_type(instance, "object"):
        return

    # Validation of "allow_other_keys"
    allow_other_keys = schema.get('allow_other_keys', False)
    if not allow_other_keys:
        # Check what instance only contains the schema keys
        invalid_keys = ','.join([key for key in instance if key not in keys])
        if invalid_keys:
            yield jsonschema.ValidationError(f"Unexpected key(s) '{invalid_keys}' found in dict.")

    # Validation of "required" on child keys
    for key in keys:
        if not keys[key].get('required'):
            continue
        if key not in instance:
            yield jsonschema.ValidationError(f"Required key '{key}' is not set in dict.")

    # Perform regular validation of each child element.
    for property, subschema in keys.items():
        if property in instance:
            yield from validator.descend(
                instance[property],
                subschema,
                path=property,
                schema_path=property,
            )


'''
AvdSchemaValidator is used to validate AVD Data.
It uses a combination of our own validators and builtin jsonschema validators
mapped to our own keywords.
We have extra type checkers not covered by the AVD_META_SCHEMA (array, boolean etc)
since the same TypeChecker is used by the validators themselves.
'''
AvdSchemaValidator = jsonschema.validators.create(
    meta_schema=AVD_META_SCHEMA,
    validators={
        "type": jsonschema._validators.type,
        "max": jsonschema._validators.maximum,
        "min": jsonschema._validators.minimum,
        "valid_values": jsonschema._validators.enum,
        "format": jsonschema._validators.format,
        "max_length": jsonschema._validators.maxLength,
        "min_length": jsonschema._validators.minLength,
        "pattern": jsonschema._validators.pattern,
        "items": jsonschema._validators.items,
        "primary_key": _primary_key_validator,
        "keys": _keys_validator
    },
    type_checker=jsonschema.TypeChecker({
        "any": jsonschema._types.is_any,
        "array": jsonschema._types.is_array,
        "boolean": jsonschema._types.is_bool,
        "integer": jsonschema._types.is_integer,
        "object": jsonschema._types.is_object,
        "null": jsonschema._types.is_null,
        "None": jsonschema._types.is_null,
        "number": jsonschema._types.is_number,
        "string": jsonschema._types.is_string,
        "dict": jsonschema._types.is_object,
        "str": jsonschema._types.is_string,
        "bool": jsonschema._types.is_bool,
        "list": jsonschema._types.is_array,
        "int": jsonschema._types.is_integer,
    })
    # version="0.1",
)


class AvdSchema():
    def __init__(self, schema: dict = None):
        if not schema:
            schema = DEFAULT_SCHEMA
        self.load_schema(schema)

    def validate_schema(self, schema: dict, msg: str = None):
        if not msg:
            msg = "An error occured during validation of the schema"
        if not isinstance(schema, dict):
            raise AvdValidationError('The supplied schema is not a dictionary')
        try:
            jsonschema.validate(schema, AVD_META_SCHEMA)
        except Exception as e:
            raise AvdSchemaError(msg) from e

    def load_schema(self, schema: dict):
        self.validate_schema(schema)
        self._schema = schema
        try:
            self._validator = AvdSchemaValidator(schema)
        except Exception as e:
            raise AvdSchemaError('An error occured during creation of the validator') from e

    def extend_schema(self, schema: dict):
        self.validate_schema(schema)
        always_merger.merge(self._schema, schema)
        self.validate_schema(self._schema, msg="An error occured during validation of the new merged schema")

    def validate(self, data, schema: dict = None):
        try:
            if schema:
                self.validate_schema(schema, msg='A Schema error occured during validation of the data')
                yield from self._validator.iter_errors(data, _schema=schema)
            yield from self._validator.iter_errors(data)
        except jsonschema.SchemaError as e:
            raise AvdSchemaError('A Schema error occured during validation of the data') from e
        except AvdSchemaError as e:
            raise AvdSchemaError('A Schema error occured during validation of the data') from e
        except Exception as e:
            raise AvdValidationError('An error occured during validation of the data') from e

    def is_valid(self, data, schema: dict = None):
        try:
            if schema:
                self.validate_schema(schema)
                return self._validator.is_valid(data, _schema=schema)
            return self._validator.is_valid(data)
        except jsonschema.SchemaError as e:
            raise AvdSchemaError('A Schema error occured during validation of the data') from e
        except AvdSchemaError as e:
            raise AvdSchemaError('A Schema error occured during validation of the data') from e
        except Exception as e:
            raise AvdValidationError('An error occured during validation of the data') from e


    def subschema(self, datapath: list, schema=None):
        '''
        Takes datapath elements as a list and returns the subschema for this datapath.
        Optionally the schema can be supplied. This is primarily used for recursive calls.

        Example
        -------
        Data model:
        a:
          b:
            - c: 1
            - c: 2

        Schema:
        a:
          type: dict
          keys:
            b:
              type: list
              primary_key: c
              items:
                type: dict
                keys:
                  c:
                    type: str

        subschema(['a', 'b'])
        >> {"type": "list", "primary_key": "c", "items": {"type": "dict", "keys": {"c": {"type": "str"}}}}

        subschema(['a', 'b', 'c'])
        >> {"type": "str"}

        subschema(['a', 'b', 'c', 'd'])
        >> raises AvdSchemaError

        subschema([])
        >> self._schema (the loaded schema)

        subschema([], <myschema>)
        >> <myschema>

        subschema(None)
        >> raises AvdSchemaError

        subschema(['a'], <invalid_schema>)
        >> raises AvdSchemaError
        '''

        if not isinstance(datapath, list):
            raise AvdSchemaError(f"The datapath argument must be a list. Got {type(datapath)}")

        if not schema:
            schema = self._schema

        self.validate_schema(schema)

        if len(datapath) == 0:
            return schema

        # More items in datapath, so we run recursively with subschema
        key = datapath[0]
        if not isinstance(key, str):
            raise AvdSchemaError(f"All datapath items must be strings. Got {type(key)}")

        if schema['type'] == 'dict' and key in schema.get('keys', []):
            return self.subschema(datapath[1:], schema['keys'][key])

        if schema['type'] == 'list' and key in schema.get('items', {}).get('keys', []):
            return self.subschema(datapath[1:], schema['items']['keys'][key])

        raise AvdSchemaError('The datapath could not be mapped to the schema')
