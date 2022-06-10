from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.arista.avd.plugins.plugin_utils.schema.errors import AristaAvdError
from ansible_collections.arista.avd.plugins.plugin_utils.schema.avdschema import AvdSchema

try:
    from deepmerge import always_merger
except ImportError as imp_exc:
    DEEPMERGE_IMPORT_ERROR = imp_exc
else:
    DEEPMERGE_IMPORT_ERROR = None


class AvdToStudioSchemaConverter:
    def __init__(self, avdschema: AvdSchema):
        if DEEPMERGE_IMPORT_ERROR:
            raise AristaAvdError('Python library "deepmerge" must be installed to use this plugin') from DEEPMERGE_IMPORT_ERROR

        self._avdschema = avdschema
        self.converters = {
            # "case_sensitive": studioschemaconverters.case_sensitive,
            "default": self.default,
            "description": self.description,
            "display_name": self.display_name,
            "format": self.format,
            "items": self.items,
            "keys": self.keys,
            "max": self.max,
            "max_length": self.max_length,
            "min": self.min,
            "min_length": self.min_length,
            "pattern": self.pattern,
            "primary_key": self.primary_key,
            "required": self.required,
            "type": self.convert_type,
            "valid_values": self.valid_values,
        }

    def convert_schema(self, avd_schema_path: str = None, studio_input_id: str = "root"):
        if avd_schema_path:
            subschema = avd_schema_path.split(".")
            var_name = avd_schema_path.split(".")[-1]
        else:
            subschema = []
            var_name = None
        schema = self._avdschema.subschema(subschema)
        return self._convert(input=schema, id=studio_input_id, var_name=var_name)

    def _convert(self, input: dict, id: str, var_name: str = ""):
        output = {id: {"name": var_name, "id": id, "label": var_name}}
        for key, value in input.items():
            if key in self.converters:
                always_merger.merge(output, self.converters[key](value, id, input))
        return output

    def default(self, default, name, input):
        if input['type'] == 'str':
            return {name: {"string_props": {"default_value": str(default)}}}
        if input['type'] == 'int':
            return {name: {"integer_props": {"default_value": int(default)}}}
        if input['type'] == 'bool':
            return {name: {"boolean_props": {"default_value": bool(default)}}}

    def description(self, description, name, input):
        return {name: {"description": ""}}

    def display_name(self, display_name, name, input):
        return {name: {"label": display_name}}

    def format(self, format, name, input):
        format_converters = {
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

    def required(self, required, name, input):
        return {name: {"required": required}}

    def items(self, items, name, input):
        if DEEPMERGE_IMPORT_ERROR:
            return

        item_name = f"{name}-item"
        output = {name: {"collection_props": {"base_field_id": item_name}}}
        always_merger.merge(output, self._convert(items, item_name, item_name))
        return output

    def keys(self, keys, name, input):
        if DEEPMERGE_IMPORT_ERROR:
            return

        members = []
        output = {}
        for key, value in keys.items():
            if value.get('studios_options', {}).get('exclude', False) is True:
                continue
            member_name = f"{name}-{key}"
            members.append(member_name)
            always_merger.merge(output, self._convert(value, member_name, key))
        always_merger.merge(output, {name: {"group_props": {"members": {"values": members}}}})
        return output

    def max(self, max, name, input):
        return {name: {"integer_props": {"range": f"{input.get('min','min')}..{max}"}}}

    def max_length(self, max_length, name, input):
        return {name: {"string_props": {"length": f"{input.get('min_length','min')}..{max_length}"}}}

    def min(self, min, name, input):
        return {name: {"integer_props": {"range": f"{min}..{input.get('max','max')}"}}}

    def min_length(self, min_length, name, input):
        return {name: {"string_props": {"length": f"{min_length}..{input.get('max_length','max')}"}}}

    def pattern(self, pattern, name, input):
        return {name: {"string_props": {"pattern": pattern}}}

    def primary_key(self, primary_key, name, input):
        return {name: {"collection_props": {"key": primary_key}}}

    def convert_type(self, type, name, input):
        type_converters = {
            "str": "INPUT_FIELD_TYPE_STRING",
            "int": "INPUT_FIELD_TYPE_INTEGER",
            "bool": "INPUT_FIELD_TYPE_BOOLEAN",
            "dict": "INPUT_FIELD_TYPE_GROUP",
            "list": "INPUT_FIELD_TYPE_COLLECTION",
        }
        type_properties = {
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

    def valid_values(self, valid_values, name, input):
        if input['type'] == 'int':
            return {name: {"integer_props": {"static_options": {"values": valid_values}}}}
        if input['type'] == 'str':
            return {name: {"string_props": {"static_options": {"values": valid_values}}}}
