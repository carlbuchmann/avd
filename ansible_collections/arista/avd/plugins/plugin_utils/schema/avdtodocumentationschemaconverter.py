from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.arista.avd.plugins.plugin_utils.schema.errors import AristaAvdError
from ansible_collections.arista.avd.plugins.plugin_utils.schema.avdschema import AvdSchema
import yaml

class AvdToDocumentationSchemaConverter:
    '''
    The documentation schema is a flatter representation of the AVD schema
    more suited for creating tables in markdown documentation

    Example:
    foo:
      description: "foo is an example of a schema key"
      table:
        - variable: "foo"
          type: "List, Items: Dictionary"
          description: "Display name of foo - main key will not append description here"
        - variable: "  - bar"
          type: "String"
          required: "Yes, Unique"
          description: "Display name of foo.bar\nDescription of foo.bar"
      yaml:
        - 'foo:'
        - '  - bar: "<str>"'
    '''

    def __init__(self, avdschema: AvdSchema):
        self._avdschema = avdschema

    def convert_schema(self):
        schema = self._avdschema.subschema([])
        output = {}

        for key in schema.get('keys', []):
            output[key] = {
                "description": schema['keys'][key].get('description'),
                "table": self.build_table_row(var_name=key, schema=schema['keys'][key], indentation=""),
            }

        return output

    def build_table_row(self, var_name: str, schema: dict, indentation: str, parent_schema: dict = None, first_list_item_key: bool = False):
        output = []
        # row = {
        #     "variable": f"{indentation}{var_name}",
        #     "type": self.type(schema),
        #     "required": self.required(schema),
        #     "default": self.default(schema),
        #     "restrictions": self.restrictions(schema),
        #     "description": self.description(schema, indentation)
        # }
        if first_list_item_key:
            row_indentation = f"{indentation[:-2]}-{indentation[-1]}"
        else:
            row_indentation = indentation

        row = {}
        row["variable"] = f"{row_indentation}{var_name}"
        row["type"] = self.type(schema)
        required = self.required(schema, var_name, parent_schema)
        if required is not None:
            row["required"] = required

        default = self.default(schema)
        if default is not None:
            row["default"] = default

        restrictions = self.restrictions(schema)
        if restrictions is not None:
            row["restrictions"] = restrictions

        description = self.description(schema, indentation)
        if description is not None:
            row["description"] = description

        output.append(row)

        if schema.get('keys'):
            output.extend(self.keys(schema, indentation))
        elif schema.get('items'):
            output.extend(self.items(schema, indentation))

        return output

    def type(self, schema: dict):
        type_converters = {
            "str": "String",
            "int": "Integer",
            "bool": "Boolean",
            "dict": "Dictionary",
            "list": "List",
        }
        schema_type = schema.get('type', 'unknown')
        output = type_converters.get(schema_type, "Any")

        if schema_type == "list":
            schema_items_type = schema.get('items', {}).get('type', 'unknown')
            items_type = type_converters.get(schema_items_type, "Any")
            output = f"{output}, items: {items_type}"

        return output

    def keys(self, schema: dict, indentation: str):
        output = []
        schema_keys = schema.get('keys', [])
        for key, value in schema_keys.items():
            rows = self.build_table_row(var_name=key, schema=value, indentation=f"{indentation}  ", parent_schema=schema)
            output.extend(rows)
        return output

    def items(self, schema: dict, indentation: str):
        output = []
        items_schema = schema.get('items', {})
        schema_items_type = items_schema.get('type')
        if schema_items_type == "dict":
            schema_keys = items_schema.get('keys', [])
            first = True
            for key, value in schema_keys.items():
                rows = self.build_table_row(var_name=key, schema=value, indentation=f"{indentation}  ", parent_schema=schema, first_list_item_key=first)
                output.extend(rows)
                first = False
        else:
            output = self.build_table_row(var_name=f"<{schema_items_type}>", schema=items_schema, indentation=f"{indentation}  ", parent_schema=schema, first_list_item_key=True)
        return output

    def required(self, schema: dict, var_name: str, parent_schema: dict):
        output = None
        if schema.get('required'):
            output = "Required"
            if parent_schema and parent_schema.get('primary_key') == var_name:
                output = f"{output}, Unique"
        return output

    def default(self, schema: dict):
        return schema.get('default')

    def restrictions(self, schema: dict):
        restrictions = []
        if schema.get('min'):
            restrictions.append(f"Min: {schema['min']}")
        if schema.get('max'):
            restrictions.append(f"Max: {schema['max']}")
        if schema.get('min_length'):
            restrictions.append(f"Min Length: {schema['min_length']}")
        if schema.get('max_length'):
            restrictions.append(f"Max Length: {schema['max_length']}")
        if schema.get('format'):
            restrictions.append(f"Format: {schema['format']}")
        if schema.get('valid_values'):
            restrictions.append("Valid Values:\n")
            for valid_value in schema['valid_values']:
                restrictions.append(f"- {valid_value}")
        if schema.get('pattern'):
            restrictions.append(f"Pattern: {schema['pattern']}")

        if restrictions:
            return "\n".join(restrictions)
        return None

    def description(self, schema: dict, indentation: str):
        descriptions = []
        if schema.get("display_name"):
            descriptions.append(schema["display_name"])
        if schema.get("description") and indentation:
            descriptions.append(schema["description"])

        if descriptions:
            return "\n".join(descriptions)
        return None
