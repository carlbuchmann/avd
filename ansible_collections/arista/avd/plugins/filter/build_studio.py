from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.arista.avd.plugins.plugin_utils.schema.avdschema import AvdSchema
from ansible_collections.arista.avd.plugins.plugin_utils.studiobuilder.studiobuilder import AvdStudioBuilder
from ansible.utils.display import Display


test_studio_design = {
    "display_name": "my test studio",
    "description": "",
    "inputs": {
        "fabric_name": {}
    },
    "resolvers": {
        "dc_vars": {
            "display_name": "Datacenter Settings",
            "tag_type": "device",
            "resolver_type": "single",
            "tag_label": "DC_Name",
            "prepopulated": True,
            "layout": "hierarchical",
            "inputs": {
                "vtep_vvtep_ip": {}
            },
            "resolvers": {
                "pod_vars": {
                    "display_name": "POD Settings",
                    "tag_type": "device",
                    "resolver_type": "single",
                    "tag_label": "POD_Name",
                    "prepopulated": True,
                    "layout": "hierarchical",
                    "inputs": {
                        "evpn_short_esi_prefix": {}
                    },
                    "resolvers": {
                        "role_vars": {
                            "display_name": "Device Role Settings",
                            "tag_type": "device",
                            "resolver_type": "single",
                            "tag_label": "Role",
                            "prepopulated": True,
                            "layout": "hierarchical",
                            "inputs": {
                                "node_type_key.defaults.loopback_ipv4_pool": {}
                            }
                        }
                    }

                }
            }
        }
    },
    "taggers": {
        "nodes": {
            "type": "device",
            "assignment_type": "single",
            "tags": {
                "type": {
                    "tag_label": "Role",
                    "suggested_values": [
                        "l3leaf",
                        "l2leaf",
                        "spine",
                    ],
                },
                "dc_name": {
                    "tag_label": "DC_Name",
                },
                "pod_name": {
                    "tag_label": "POD_Name",
                },
                "node_type_key.nodes_groups.nodes.id": {
                    "tag_label": "ID",
                },
                "node_bgp_as": {
                    "tag_label": "BGP_AS",
                },
                "short_esi": {
                    "tag_label": "Short_ESI",
                },
                "node_type_key.node_groups.name": {
                    "tag_label": "MLAG_Group",
                },
            }
        }
    }
}


def build_studio(schema, studio_design=None):
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
    if studio_design is None:
        studio_design=test_studio_design

    avdschema = AvdSchema(schema)

    builder = AvdStudioBuilder(avdschema)
    output = builder.build(studio_design)
    return output


class FilterModule(object):
    def filters(self):
        return {
            'build_studio': build_studio,
        }
