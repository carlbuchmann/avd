from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.arista.avd.plugins.plugin_utils.schema.errors import AristaAvdError
from ansible_collections.arista.avd.plugins.plugin_utils.schema.avdschema import AvdSchema
from ansible_collections.arista.avd.plugins.plugin_utils.schema.avdtostudioschemaconverter import AvdToStudioSchemaConverter
from ansible_collections.arista.avd.plugins.plugin_utils.schema.avdtodocumentationschemaconverter import AvdToDocumentationSchemaConverter


def convert_schema(schema: dict, type: str):
    """
    The `arista.avd.convert_schema` filter will convert AVD Schema to a chosen output format.

    Parameters
    ----------
    schema : dict
        Input AVD Schema
    type : str, ["studios", "documentation"]
        Type of schema to convert to

    Returns
    -------
    dict
        Schema of the requested type

    Raises
    ------
    AvdSchemaError, AvdValidationError
        If the input schema is not valid, exceptions will be raised accordingly.
    """
    avdschema = AvdSchema(schema)
    if type == "studios":
        schemaconverter = AvdToStudioSchemaConverter(avdschema)
    elif type == "documentation":
        schemaconverter = AvdToDocumentationSchemaConverter(avdschema)
    else:
        raise AristaAvdError(f"Filter arista.avd.convert_schema requires type 'studio' or 'documentation'. Got {type}")

    return schemaconverter.convert_schema()


class FilterModule(object):
    def filters(self):
        return {
            'convert_schema': convert_schema,
        }
