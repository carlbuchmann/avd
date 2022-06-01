from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.arista.avd.plugins.plugin_utils.studiobuilder.avdschemaconverter import AvdSchemaConverter
from ansible_collections.arista.avd.plugins.plugin_utils.schema.avdschema import AvdSchema
import json


class AvdStudioBuilder:
    def __init__(self, avdschema: AvdSchema, ):
        self._converter = AvdSchemaConverter(avdschema)

    def build(self, studio_design: dict):
        self._data_maps = []
        self._input_fields = {}
        self._input_layout = {}
        self._input_fields.update({
            "root": {
                "type": "INPUT_FIELD_TYPE_GROUP",
                "name": "",
                "label": "",
                "id": "root",
                "group_props": {
                    "members": {
                        "values": [],
                    }
                }
            }
        })
        self._add_inputs(studio_design['inputs'], self._input_fields["root"])
        self._add_taggers(studio_design.get('taggers', {}), self._input_fields["root"])
        self._add_resolvers(studio_design.get('resolvers', {}), self._input_fields["root"])
        self._set_template()

        self._studio = {
            "display_name": studio_design["display_name"],
            "description": studio_design["description"],
            "input_schema": {
                "fields": {
                    "values": self._input_fields,
                },
                "layout": {
                    "value": json.dumps(self._input_layout),
                },
            },
            "template": {
                "type": "TEMPLATE_TYPE_MAKO",
                "body": self._template,
            },
        }
        return self._studio

    def _add_inputs(self, inputs, parent):
        for var_path, input_options in inputs.items():
            # With var_path "foo.bar", the variable name should be "<parent-name>-bar"
            var_name = var_path.split('.')[-1]
            studio_input_id = f"{parent['id']}-{var_name}"

            # We could get multiple inputs if the input is a group with nested inputs.
            new_inputs = self._converter.to_studios(avd_schema_path=var_path, studio_input_id=studio_input_id)

            # We can only have one input with a matching name.
            for new_input_id, new_input in new_inputs.items():
                if new_input_id != studio_input_id:
                    continue

                # If var_path is more than just a var, we should add a data mapper to the studio template
                if var_path != var_name:
                    self._data_maps.append({"input": new_input_id, "avd_var": var_path})

                if parent["type"] == "INPUT_FIELD_TYPE_GROUP":
                    parent["group_props"]["members"]["values"].append(new_input_id)
                break

            self._input_fields.update(new_inputs)

    def _add_taggers(self, taggers, parent):
        for tagger_name, tagger_options in taggers.items():
            tagger_key = f"{parent['id']}-tagger_{tagger_name}"
            tagger = {
                "type": "TAGGER",
                "parentKey": parent["id"],
                "key": tagger_key,
                "name": tagger_name,
                "description": tagger_options.get("description", ""),
                "tagType": tagger_options.get("type", "DEVICE").upper(),
                "assignmentType": tagger_options.get("assignment_type", "SINGLE").upper(),
                "columns": [],
            }
            for tag_path, tag_options in tagger_options["tags"].items():
                column = {
                    "tagLabel": tag_options["tag_label"],
                    "suggestedValues": tag_options.get("suggested_values", []),
                }
                tagger["columns"].append(column)
                self._data_maps.append({
                    "tag": tag_options["tag_label"],
                    "avd_var": tag_path,
                    "type": tag_options.get('type')
                })

            self._input_layout.update({tagger_key: tagger})

    def _add_resolvers(self, resolvers, parent):
        for resolver_short_name, resolver_options in resolvers.items():
            resolver_name = f"resolver_{resolver_short_name}"
            resolver_key = f"{parent['id']}-{resolver_name}"
            resolver_group_key = f"{resolver_key}-{resolver_short_name}"
            resolver_group_name = f"{resolver_short_name}"
            if resolver_options.get('prepopulated') and resolver_options.get('resolver_type') == "single":
                display_mode = "RESOLVER_FIELD_DISPLAY_MODE_ALL"
            else:
                display_mode = "RESOLVER_FIELD_DISPLAY_MODE_SPARSE"

            if resolver_options.get('tag_type') == "interface" and resolver_options.get('resolver_type') == "single":
                input_mode = "RESOLVER_FIELD_INPUT_MODE_SINGLE_INTERFACE_TAG"
            elif resolver_options.get('tag_type') == "interface":
                input_mode = "RESOLVER_FIELD_INPUT_MODE_MULTI_INTERFACE_TAG"
            elif resolver_options.get('resolver_type') == "single":
                input_mode = "RESOLVER_FIELD_INPUT_MODE_SINGLE_DEVICE_TAG"
            else:
                input_mode = "RESOLVER_FIELD_INPUT_MODE_MULTI_DEVICE_TAG"

            resolver = {
                "type": "INPUT_FIELD_TYPE_RESOLVER",
                "label": resolver_options.get('display_name', resolver_short_name),
                "id": resolver_key,
                "name": resolver_name,
                "description": resolver_options.get("description", ""),
                "resolver_props": {
                    "base_field_id": resolver_group_key,
                    "display_mode": display_mode,
                    "input_mode": input_mode,
                    "input_tag_label": resolver_options.get("tag_label", ""),
                    "tag_filter_query": resolver_options.get("tag_filter_query", ""),
                }
            }
            resolver_group = {
                "type": "INPUT_FIELD_TYPE_GROUP",
                "label": resolver_options.get('display_name', resolver_name),
                "id": resolver_group_key,
                "name": resolver_group_name,
                "description": resolver_options.get("description", ""),
                "group_props": {
                    "members": {
                        "values": []
                    }
                }
            }

            if resolver_options.get("layout"):
                page_layout = (resolver_options["layout"] == "hierarchical")
                self._input_layout.update({
                    resolver_key: {
                        "key": resolver_key,
                        "type": "INPUT",
                        "isPageLayout": page_layout,
                    }
                })

            self._input_fields.update({resolver_key: resolver, resolver_group_key: resolver_group})

            if parent["type"] == "INPUT_FIELD_TYPE_GROUP":
                parent["group_props"]["members"]["values"].append(resolver_key)

            self._add_inputs(resolver_options['inputs'], self._input_fields[resolver_group_key])
            self._add_taggers(resolver_options.get('taggers', {}), self._input_fields[resolver_group_key])
            self._add_resolvers(resolver_options.get('resolvers', {}), self._input_fields[resolver_group_key])

    def _set_template(self):
        data_maps = self._data_maps
        template = STUDIO_TEMPLATE.replace("DATA_MAPS = []", f"DATA_MAPS = {data_maps}")
        self._template = template


STUDIO_TEMPLATE = '''
<%
import ansible_runner
import json
from arista.tag.v2.services import TagAssignmentServiceStub
from arista.tag.v2.services.gen_pb2 import TagAssignmentStreamRequest
from arista.tag.v2.tag_pb2 import TagAssignment
from arista.studio.v1.services import AssignedTagsServiceStub
from arista.studio.v1.services.gen_pb2 import AssignedTagsRequest
from tagsearch_python.tagsearch_pb2_grpc import TagSearchStub
from tagsearch_python.tagsearch_pb2 import TagMatchRequestV2
from webapp.v2.types import DeviceResolver

DATA_MAPS = []

def __get_studio_devices():
    # First get the query string from the studio
    get_req = AssignedTagsRequest()
    get_req.key.workspace_id.value = ctx.studio.workspaceId
    get_req.key.studio_id.value = ctx.studio.studioId
    tsclient = ctx.getApiClient(AssignedTagsServiceStub)
    tag = tsclient.GetOne(get_req)
    query = tag.value.query.value
    # Now try to search with this query to get the matching devices
    tsclient = ctx.getApiClient(TagSearchStub)
    search_req = TagMatchRequestV2(query=query, workspace_id=ctx.studio.workspaceId, topology_studio_request=True)
    search_res = tsclient.GetTagMatchesV2(search_req)
    return [match.device.device_id for match in search_res.matches] or query

def __get_all_device_tags(device_id):
    get_all_req = TagAssignmentStreamRequest()
    tag_filter = TagAssignment()
    tag_filter.key.workspace_id.value = ctx.studio.workspaceId
    tag_filter.key.element_type = 1
    tag_filter.key.device_id.value = device_id
    get_all_req.partial_eq_filter.append(tag_filter)
    # Create tagstub
    tsclient = ctx.getApiClient(TagAssignmentServiceStub)
    tag_generator = tsclient.GetAll(get_all_req)
    return {tag.value.key.label.value: tag.value.key.value.value for tag in tag_generator}

def __strip_and_resolve(_input, _device):
    # Resolve any nested resolvers and strip empty strings
    if isinstance(_input, DeviceResolver):
        _resolved_input = _input.resolve(device=_device)
        return __strip_and_resolve(_resolved_input, _device)
    if isinstance(_input, dict):
        _data = {}
        for _key in _input:
            _tmp_value = __strip_and_resolve(_input[_key], _device)
            if _tmp_value is None:
                continue
            _data[_key] = _tmp_value
        return _data
    if isinstance(_input, list):
        _data = []
        for _item in _input:
            _tmp_value = __strip_and_resolve(_item, _device)
            if _tmp_value is None:
                continue
            _data.append(_tmp_value)
    if isinstance(_input, str):
        if _input == "":
            return None
    return _input

def __node_groups(_data_maps, _input_data, _tag_data):
    _node_groups = {}
    for _device in sorted(_input_data):
        for _data_map in _data_maps:
            if "tag" in _data_map and _data_map.get("type") == "node_group":
                value = _tag_data.get(_device, {}).get(_data_map["tag"])
                if value is None:
                    break
                _node_groups.setdefault(value, {"nodes": {}})
                _node_groups[value]["nodes"][_device] = {}
                break
    return _node_groups

def __map_data(_data_maps, _input_data, _tag_data, _node_groups):
    _output = {}
    value = None
    for _device in _input_data:
        for _data_map in _data_maps:
            if "input" in _data_map:
                # Get value from _input_data
                data_pointer = _input_data[_device]
                keys = _data_map["input"].split("-")
                # First key in path would be "root" so we skip that
                for key in keys[1:-1]:
                    if data_pointer.get(key) is None:
                        data_pointer = {}
                        break
                    data_pointer = data_pointer[key]
                value = data_pointer.get(keys[-1])
                if value is None:
                    continue

            if "tag" in _data_map:
                # Get value from _tag_data
                value = _tag_data.get(_device, {}).get(_data_map["tag"])
                if value is None:
                    continue
                if _data_map.get("type") == "int":
                    value = int(value)
                elif _data_map.get("type") == "list":
                    value = value.split(',')
                elif _data_map.get("type") == "node_group":
                    value = {str(value): _node_groups.get(value, {})}

            if (not value is None) and "avd_var" in _data_map:
                # Set avd_var with value
                data_pointer = _input_data[_device]
                keys = _data_map["avd_var"].split(".")

                # Hack to insert ex. "l3leaf" instead of "node_type_key"
                if keys[0] == "node_type_key":
                    keys[0] = _tag_data.get(_device, {}).get("Role", "node_type_key")

                for key in keys[:-1]:
                    data_pointer.setdefault(key, {})
                    data_pointer = data_pointer[key]
                data_pointer[keys[-1]] = value

_studio_devices = __get_studio_devices()
_all_devices = [device for device in ctx.topology.getDevices() if device.id in _studio_devices]
_this_hostname = ctx.device.hostName
_tag_data = {}
_input_data = {}
for _device in _all_devices:
    _tag_data[_device.hostName] = __get_all_device_tags(_device.id)
    _input_data[_device.hostName] = {}
    for _input_name, _input in ctx.studio.inputs.items():
        _input_data[_device.hostName][_input_name] = __strip_and_resolve(_input, _device.id)

    _input_data[_device.hostName].update({
        'mgmt_gateway': "10.90.224.1",
        'cvp_instance_ip': "10.90.224.100",
        'local_users': {
            "cvpadmin": {
                "role": "network_admin",
                "privilege": "15",
                "sha512_password": "$6$MfWfHDSxXJ9evpQu$q9gI/9gm8fVaXupIh4NvHoGJ4YcM.7suYc1Y.vy1hDosVO7GX35Xq.OeiYwj/AYbCfuPe//MWLq.zQlwZkPQz/"
            }
        },
        'ntp': {
            "10.90.20.122": {
                "iburst": True,
                "vrf": "MGMT",
            }
        },
        'cvp_ingestauth_key': "",
        'custom_structured_configuration_daemon_terminattr' : {
            'cvauth': {
                'method': 'token',
                'token_file': '/tmp/token'
            }
        }
    })

_node_groups = __node_groups(DATA_MAPS, _input_data, _tag_data)
__map_data(DATA_MAPS, _input_data, _tag_data, _node_groups)

_fabric_name = ctx.studio.inputs.get('fabric_name', "no_fabric_name")

# Run Ansible AVD passing inventory, variables and playbook as arguments.
_runner_result = ansible_runner.interface.run(
    envvars={
        "ANSIBLE_JINJA2_EXTENSIONS": "jinja2.ext.loopcontrols,jinja2.ext.do,jinja2.ext.i18n"
    },
    inventory={
        "all": {
            "children": {
                _fabric_name: {
                    "hosts": _input_data
                }
            }
        }
    },
    skip_tags="documentation",
    verbosity=0,
    limit=_this_hostname,
    playbook=[
        {
            "name": "Run AVD",
            "hosts": _fabric_name,
            "gather_facts": "false",
            "connection": "local",
            "tasks": [
                {
                    "import_role": {
                        "name": "arista.avd.eos_designs",
                        "tasks_from": "studios"
                    },
                },
                {
                    "name": "generate device intended config and documentation",
                    "import_role": {
                        "name": "arista.avd.eos_cli_config_gen",
                        "tasks_from": "studios"
                    }
                },
            ]
        }
    ],
    json_mode=False,
    quiet=True
)
_result = ""
for _event in _runner_result.host_events(_this_hostname):
    _event_data = _event.get('event_data',{})
    if _event_data.get('role') == 'eos_cli_config_gen':
        _result = _event['event_data'].get('res',{}).get('ansible_facts',{}).get('eos_config')
        if _result:
            break
if not _result:
    with _runner_result.stdout as _output:
        _result = _output.read()
%>
! ${f"{_input_data[_this_hostname]}"}
${_result}
'''
