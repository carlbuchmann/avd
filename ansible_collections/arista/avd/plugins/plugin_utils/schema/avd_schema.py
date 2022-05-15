from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json
import jsonschema.validators
import jsonschema._validators
import jsonschema._types
import jsonschema
from deepmerge import always_merger


# TODO move this to utils when python pr merges
class AristaAvdError(Exception):
    def __init__(self, message="An Error has occured in an arista.avd plugin"):
        self.message = message
        super().__init__(self.message)

    def _json_path_to_jinja(self, json_path):
        path = ""
        for index, elem in enumerate(json_path):
            if isinstance(elem, int):
                path += "[" + str(elem) + "]"
            else:
                if index == 0:
                    path += elem
                    continue
                path += "." + elem
        return path

class AvdSchemaError(AristaAvdError):
    def __init__(self, message = "Schema Error", error: jsonschema.SchemaError = None):
        if isinstance(error, jsonschema.SchemaError):
            self.message = f"'Schema Error: {self._json_path_to_jinja(error.absolute_path)}': {error.message}"
        else:
            self.message = message
        super().__init__(self.message)


class AvdValidationError(AristaAvdError):
    def __init__(self, message: str = "Schema Error", error: jsonschema.ValidationError = None):
        if isinstance(error, (jsonschema.ValidationError)):
            self.message = f"'Validation Error: {self._json_path_to_jinja(error.absolute_path)}': {error.message}"
        else:
            self.message = message
        super().__init__(self.message)


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
        self._schema_validator = jsonschema.Draft7Validator(AVD_META_SCHEMA)
        self.load_schema(schema)

    def validate_schema(self, schema: dict):
        validation_errors = self._schema_validator.iter_errors(schema)
        for validation_error in validation_errors:
            yield self._errror_handler(validation_error)

    def load_schema(self, schema: dict):
        for validation_error in self.validate_schema(schema):
            raise validation_error
        self._schema = schema
        try:
            self._validator = AvdSchemaValidator(schema)
        except Exception as e:
            raise AristaAvdError('An error occured during creation of the validator') from e

    def extend_schema(self, schema: dict):
        for validation_error in self.validate_schema(schema):
            raise validation_error
        always_merger.merge(self._schema, schema)
        for validation_error in self.validate_schema(self._schema):
            raise validation_error

    def validate(self, data, schema: dict = None):
        if schema:
            for schema_validation_error in self.validate_schema(schema):
                yield schema_validation_error
                return

            validation_errors = self._validator.iter_errors(data, _schema=schema)
        else:
            validation_errors = self._validator.iter_errors(data)

        try:
            for validation_error in validation_errors:
                yield self._errror_handler(validation_error)
        except Exception as error:
            yield self._errror_handler(error)

    def _errror_handler(self, error: Exception):
        if isinstance(error, jsonschema.ValidationError):
            return AvdValidationError(error=error)
        if isinstance(error, jsonschema.SchemaError):
            return AvdSchemaError(error=error)
        return AvdSchemaError(str(error))

    def is_valid(self, data, schema: dict = None):
        if schema:
            for schema_validation_error in self.validate_schema(schema):
                raise schema_validation_error
        try:
            if schema:
                return self._validator.is_valid(data, _schema=schema)
            return self._validator.is_valid(data)
        except Exception as error:
            raise self._errror_handler(error) from error

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

        for validation_error in self.validate_schema(schema):
            raise validation_error

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

        # Falling through here in case the schema is not covering the requested datapath
        raise AvdSchemaError('The datapath could not be found in the schema')
