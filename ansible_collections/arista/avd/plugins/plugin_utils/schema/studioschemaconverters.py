from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from deepmerge import always_merger


def default(avdschemaconverter, default, name, input, converters):
    if input['type'] == 'str':
        return {name: {"string_props": {"default_value": str(default)}}}
    if input['type'] == 'int':
        return {name: {"integer_props": {"default_value": int(default)}}}
    if input['type'] == 'bool':
        return {name: {"boolean_props": {"default_value": bool(default)}}}

def description(avdschemaconverter, description, name, input, converters):
    return {name: {"description": ""}}

def display_name(avdschemaconverter, display_name, name, input, converters):
    return {name: {"label": display_name}}

def format(avdschemaconverter, format, name, input, converters):
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

def required(avdschemaconverter, required, name, input, converters):
    return {name: {"required": required}}

def items(avdschemaconverter, items, name, input, converters):
    item_name = f"{name}-item"
    output = {name: {"collection_props": {"base_field_id": item_name}}}
    always_merger.merge(output, avdschemaconverter.convert(items, converters, item_name, item_name))
    return output

def keys(avdschemaconverter, keys, name, input, converters):
    members = []
    output = {}
    for key, value in keys.items():
        if value.get('studios_options', {}).get('exclude', False) is True:
            continue
        member_name = f"{name}-{key}"
        members.append(member_name)
        always_merger.merge(output, avdschemaconverter.convert(value, converters, member_name, key))
    always_merger.merge(output, {name: {"group_props": {"members": {"values": members}}}})
    return output

def max(avdschemaconverter, max, name, input, converters):
    return {name: {"integer_props": {"range": f"{input.get('min','min')}..{max}"}}}

def max_length(avdschemaconverter, max_length, name, input, converters):
    return {name: {"string_props": {"length": f"{input.get('min_length','min')}..{max_length}"}}}

def min(avdschemaconverter, min, name, input, converters):
    return {name: {"integer_props": {"range": f"{min}..{input.get('max','max')}"}}}

def min_length(avdschemaconverter, min_length, name, input, converters):
    return {name: {"string_props": {"length": f"{min_length}..{input.get('max_length','max')}"}}}

def pattern(avdschemaconverter, pattern, name, input, converters):
    return {name: {"string_props": {"pattern": pattern}}}

def primary_key(avdschemaconverter, primary_key, name, input, converters):
    return {name: {"collection_props": {"key": primary_key}}}

def convert_type(avdschemaconverter, type, name, input, converters):
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

def valid_values(avdschemaconverter, valid_values, name, input, converters):
    if input['type'] == 'int':
        return {name: {"integer_props": {"static_options": {"values": valid_values}}}}
    if input['type'] == 'str':
        return {name: {"string_props": {"static_options": {"values": valid_values}}}}
