from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.arista.avd.plugins.plugin_utils.schema.avdschema import AvdSchema
from deepmerge import always_merger


class AvdSchemaConverter:
    def __init__(self, avdschema: AvdSchema, studio_converter: dict = None):
        self._avdschema = avdschema
        if studio_converter:
            self.studio_converter = studio_converter
        else:
            self.studio_converters = {
                # "case_sensitive": convert_case_sensitive_to_studios,
                "default": convert_default_to_studios,
                "description": convert_description_to_studios,
                "display_name": convert_display_name_to_studios,
                "format": convert_format_to_studios,
                "items": convert_items_to_studios,
                "keys": convert_keys_to_studios,
                "max": convert_max_to_studios,
                "max_length": convert_max_length_to_studios,
                "min": convert_min_to_studios,
                "min_length": convert_min_length_to_studios,
                "pattern": convert_pattern_to_studios,
                "primary_key": convert_primary_key_to_studios,
                "required": convert_required_to_studios,
                "type": convert_type_to_studios,
                "valid_values": convert_valid_values_to_studios,
            }

    def to_studios(self):
        schema = self._avdschema.subschema([])
        return self.convert(schema, self.studio_converters)

    def convert(self, input: dict, converters: dict, name: str = "root", var_name: str = ""):
        output = {name: {"name": var_name, "id": name, "label": var_name}}
        for key, value in input.items():
            if key in converters:
                always_merger.merge(output, converters[key](self, value, name, input, converters))
        return output

def convert_default_to_studios(avdschemaconverter, default, name, input, converters):
    if input['type'] == 'str':
        return {name: {"string_props": {"default_value": str(default)}}}
    if input['type'] == 'int':
        return {name: {"integer_props": {"default_value": int(default)}}}
    if input['type'] == 'bool':
        return {name: {"boolean_props": {"default_value": bool(default)}}}

def convert_description_to_studios(avdschemaconverter, description, name, input, converters):
    return {name: {"description": ""}}

def convert_display_name_to_studios(avdschemaconverter, display_name, name, input, converters):
    return {name: {"label": display_name}}

def convert_format_to_studios(avdschemaconverter, format, name, input, converters):
    format_converters={
        "ipv4": "ip",
        "ipv4_cidr": "cidr",
        "ipv6": "ipv6",
        "ipv6_cidr": "cidr",
        "ip": "ip",
        "cidr": "cidr",
        "mac": "mac"
    }
    # Return the converted format or None
    return {name: {"string_props": {"format": format_converters.get(format, None)}}}

def convert_required_to_studios(avdschemaconverter, required, name, input, converters):
    return {name: {"required": required}}

def convert_items_to_studios(avdschemaconverter, items, name, input, converters):
    item_name = f"{name}-item"
    output = {name: {"collection_props": {"base_field_id": item_name}}}
    always_merger.merge(output, avdschemaconverter.convert(items, converters, item_name, item_name))
    return output

def convert_keys_to_studios(avdschemaconverter, keys, name, input, converters):
    members = []
    output = {}
    for key, value in keys.items():
        member_name = f"{name}-{key}"
        members.append(member_name)
        always_merger.merge(output, avdschemaconverter.convert(value, converters, member_name, key))
    always_merger.merge(output, {name: {"group_props": {"members": {"values": members}}}})
    return output

def convert_max_to_studios(avdschemaconverter, max, name, input, converters):
    return {name: {"integer_props": {"range": f"{input.get('min','min')}..{max}"}}}

def convert_max_length_to_studios(avdschemaconverter, max_length, name, input, converters):
    return {name: {"string_props": {"length": f"{input.get('min_length','min')}..{max_length}"}}}

def convert_min_to_studios(avdschemaconverter, min, name, input, converters):
    return {name: {"integer_props": {"range": f"{min}..{input.get('max','max')}"}}}

def convert_min_length_to_studios(avdschemaconverter, min_length, name, input, converters):
    return {name: {"string_props": {"length": f"{min_length}..{input.get('max_length','max')}"}}}

def convert_pattern_to_studios(avdschemaconverter, pattern, name, input, converters):
    return {name: {"string_props": {"pattern": pattern}}}

def convert_primary_key_to_studios(avdschemaconverter, primary_key, name, input, converters):
    return {name: {"collection_props": {"key": primary_key}}}

def convert_type_to_studios(avdschemaconverter, type, name, input, converters):
    type_converters={
        "str": "INPUT_FIELD_TYPE_STRING",
        "int": "INPUT_FIELD_TYPE_INTEGER",
        "bool": "INPUT_FIELD_TYPE_BOOLEAN",
        "dict": "INPUT_FIELD_TYPE_GROUP",
        "list": "INPUT_FIELD_TYPE_COLLECTION",
    }
    type_properties={
        "str": "string_props",
        "int": "integer_props",
        "bool": "boolean_props",
        "dict": "group_props",
        "list": "collection_props",
    }
    # Return the converted format or String
    return {
        name: {
            "type": type_converters.get(type, "INPUT_FIELD_TYPE_STRING"),
            type_properties.get(type, "string_props"): {}
        }
    }

def convert_valid_values_to_studios(avdschemaconverter, valid_values, name, input, converters):
    if input['type'] == 'int':
        return {name: {"integer_props": {"static_options": {"values": valid_values}}}}
    if input['type'] == 'str':
        return {name: {"string_props": {"static_options": {"values": valid_values}}}}
