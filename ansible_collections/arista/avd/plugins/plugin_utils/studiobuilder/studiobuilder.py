from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.arista.avd.plugins.plugin_utils.schema.avdschemaconverter import AvdSchemaConverter
from ansible_collections.arista.avd.plugins.plugin_utils.schema.avdschema import AvdSchema
from deepmerge import always_merger


class AvdStudioBuilder:
    def __init__(self, avdschema: AvdSchema, ):
        self._converter = AvdSchemaConverter(avdschema)

    def build(self, studio_design: dict):
        self._data_mappings = []
        self._input_fields = {}
        self._input_layout = {}
        self._studio = {
            "display_name": studio_design["display_name"],
            "description": studio_design["description"],
            "input_schema": {
                "fields": {
                    "values": self._input_fields,
                },
                "layout": {
                    "value": self._input_layout,
                },
            }
        }
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
        return self._studio

    def _add_inputs(self, inputs, parent):
        for input_path, input_options in inputs.items():
            # With input path "foo.bar", the variable name should be "bar"
            input_var_name = input_path.split('.')[-1]

            # We could get multiple inputs if the input is a group with nested inputs.
            new_inputs = self._converter.to_studios(input_path, input_var_name)

            # We can only have one input with a matching name.
            for new_input_id, new_input in new_inputs.items():
                if new_input['name'] != input_var_name:
                    continue

                # If input path is more than just a var, we should add a data mapper to the studio template
                if input_path != input_var_name:
                    self._data_mappings.append({"studio_input": new_input_id, "avd_var": input_path})

                if parent["type"] == "INPUT_FIELD_TYPE_GROUP":
                    parent["group_props"]["members"]["values"].append(new_input_id)
                break

            self._input_fields.update(new_inputs)

    def _add_taggers(self, taggers, parent):
        for tagger_name, tagger_options in taggers.items():
            tagger_key = f"{parent['id']}-tagger-{tagger_name}"
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
                self._data_mappings.append({"studio_tag": tag_options["tag_label"], "avd_var": tag_path})

            self._input_layout.update({tagger_key: tagger})

    def _add_resolvers(self, resolvers, parent):
        for resolver_name, resolver_options in resolvers.items():
            resolver_key = f"{parent['id']}-resolver-{resolver_name}"
            resolver_group_key = f"{parent['id']}-resolver-group-{resolver_name}"
            resolver_group_name = f"{resolver_name}-group"
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
                "label": resolver_options.get('display_name',resolver_name),
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
                "label": resolver_options.get('display_name',resolver_name),
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
