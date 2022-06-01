from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.arista.avd.plugins.plugin_utils.schema.avdschema import AvdSchema
from ansible_collections.arista.avd.plugins.plugin_utils.studiobuilder.studiobuilder import AvdStudioBuilder
from ansible.utils.display import Display


test_studio_design = {
    "display_name": "my test studio",
    "description": "",
    "inputs": {
        "fabric_name": {},
        "bgp_peer_groups": {},
        "p2p_uplinks_mtu": {},
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
                "mgmt_gateway": {},
            },
            "resolvers": {
                "pod_vars": {
                    "display_name": "POD Settings",
                    "tag_type": "device",
                    "resolver_type": "single",
                    "tag_label": "POD_Name",
                    "prepopulated": True,
                    "layout": "hierarchical",
                    "inputs": {},
                    "resolvers": {
                        "role_vars": {
                            "display_name": "Device Role Settings",
                            "tag_type": "device",
                            "resolver_type": "single",
                            "tag_label": "Role",
                            "prepopulated": True,
                            "layout": "hierarchical",
                            "inputs": {
                                "node_type_key.defaults.loopback_ipv4_pool": {},
                                "node_type_key.defaults.vtep_loopback_ipv4_pool": {},
                                "node_type_key.defaults.bgp_defaults": {},
                                "node_type_key.defaults.uplink_interfaces": {},
                                "node_type_key.defaults.uplink_switches": {},
                                "node_type_key.defaults.uplink_ipv4_pool": {},
                                "node_type_key.defaults.mlag_interfaces": {},
                                "node_type_key.defaults.mlag_peer_ipv4_pool": {},
                                "node_type_key.defaults.mlag_peer_l3_ipv4_pool": {},
                                "node_type_key.defaults.virtual_router_mac_address": {},
                                "node_type_key.defaults.spanning_tree_priority": {},
                                "node_type_key.defaults.spanning_tree_mode": {},
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
                "node_type_key.defaults.id": {
                    "tag_label": "ID",
                    "type": "int",
                },
                "node_type_key.defaults.platform": {
                    "tag_label": "Platform",
                },
                "node_type_key.defaults.mgmt_ip": {
                    "tag_label": "Management_IP",
                },
                "node_type_key.defaults.bgp_as": {
                    "tag_label": "BGP_AS",
                },
                "node_type_key.defaults.uplink_switch_interfaces": {
                    "tag_label": "Uplink_Switch_Interfaces",
                    "type": "list",
                },
                "node_type_key.node_groups": {
                    "tag_label": "Node_Group",
                    "type": "node_group",
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
        studio_design = test_studio_design

    avdschema = AvdSchema(schema)

    builder = AvdStudioBuilder(avdschema)
    output = builder.build(studio_design)
    return output


class FilterModule(object):
    def filters(self):
        return {
            'build_studio': build_studio,
        }
