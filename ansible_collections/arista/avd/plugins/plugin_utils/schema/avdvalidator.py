from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json

try:
    import jsonschema.validators
    import jsonschema._validators
    import jsonschema._types
    import jsonschema
except ImportError as imp_exc:
    JSONSCHEMA_IMPORT_ERROR = imp_exc
else:
    JSONSCHEMA_IMPORT_ERROR = None

script_dir = os.path.dirname(__file__)
with open(f"{script_dir}/avd_meta_schema.json", "r", encoding="utf-8") as file:
    AVD_META_SCHEMA = json.load(file)


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
if JSONSCHEMA_IMPORT_ERROR:
    AvdValidator = None
else:
    AvdValidator = jsonschema.validators.create(
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
