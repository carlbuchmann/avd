from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.arista.avd.plugins.plugin_utils.schema.errors import AristaAvdError
from ansible_collections.arista.avd.plugins.plugin_utils.schema.avdschema import AvdSchema
from ansible_collections.arista.avd.plugins.plugin_utils.studiobuilder import studioschemaconverters

try:
    from deepmerge import always_merger
except ImportError as imp_exc:
    DEEPMERGE_IMPORT_ERROR = imp_exc
else:
    DEEPMERGE_IMPORT_ERROR = None


class AvdSchemaConverter:
    def __init__(self, avdschema: AvdSchema, studio_converter: dict = None):
        if DEEPMERGE_IMPORT_ERROR:
            raise AristaAvdError('Python library "deepmerge" must be installed to use this plugin') from DEEPMERGE_IMPORT_ERROR

        self._avdschema = avdschema
        if studio_converter:
            self.studio_converter = studio_converter
        else:
            self.studio_converters = {
                # "case_sensitive": studioschemaconverters.case_sensitive,
                "default": studioschemaconverters.default,
                "description": studioschemaconverters.description,
                "display_name": studioschemaconverters.display_name,
                "format": studioschemaconverters.format,
                "items": studioschemaconverters.items,
                "keys": studioschemaconverters.keys,
                "max": studioschemaconverters.max,
                "max_length": studioschemaconverters.max_length,
                "min": studioschemaconverters.min,
                "min_length": studioschemaconverters.min_length,
                "pattern": studioschemaconverters.pattern,
                "primary_key": studioschemaconverters.primary_key,
                "required": studioschemaconverters.required,
                "type": studioschemaconverters.convert_type,
                "valid_values": studioschemaconverters.valid_values,
            }

    def to_studios(self, avd_schema_path: str = None, studio_input_id: str = "root"):
        if avd_schema_path:
            subschema = avd_schema_path.split(".")
            var_name = avd_schema_path.split(".")[-1]
        else:
            subschema = []
            var_name = None
        schema = self._avdschema.subschema(subschema)
        return self.convert(input=schema, converters=self.studio_converters, id=studio_input_id, var_name=var_name)

    def convert(self, input: dict, converters: dict, id: str = "root", var_name: str = ""):
        output = {id: {"name": var_name, "id": id, "label": var_name}}
        for key, value in input.items():
            if key in converters:
                always_merger.merge(output, converters[key](self, value, id, input, converters))
        return output
