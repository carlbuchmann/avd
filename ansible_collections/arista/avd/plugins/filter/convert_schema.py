from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.arista.avd.plugins.plugin_utils.schema.avdschema import AvdSchema
from ansible_collections.arista.avd.plugins.plugin_utils.schema.avdschemaconverter import AvdSchemaConverter
from ansible.utils.display import Display


def convert_schema(schema, type="studios"):
    """
    The `arista.avd.convert_schema` filter will convert AVD Schema to a chosen output format.

    Parameters
    ----------
    schema : dict
        Input AVD Schema
    type : str, optional
        Type of schema to convert to (currently only "studios" is supported)

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
    schemaconverter = AvdSchemaConverter(avdschema)
    output = schemaconverter.to_studios()
    return output


class FilterModule(object):
    def filters(self):
        return {
            'convert_schema': convert_schema,
        }
