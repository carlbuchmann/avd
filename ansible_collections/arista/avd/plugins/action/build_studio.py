from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleActionFail
from ansible_collections.arista.avd.plugins.plugin_utils.schema.avdschema import AvdSchema
from ansible_collections.arista.avd.plugins.plugin_utils.studiobuilder.studiobuilder import AvdStudioBuilder


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = {}

        result = super().run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        if self._task.args and "avd_schema" in self._task.args:
            avd_schema = self._task.args["avd_schema"]
            if not isinstance(avd_schema, dict):
                raise AnsibleActionFail("The argument 'avd_schema' is not a dict")
        else:
            raise AnsibleActionFail("The argument 'avd_schema' must be set")

        if self._task.args and "studio_design" in self._task.args:
            studio_design = self._task.args["studio_design"]
            if not isinstance(studio_design, dict):
                raise AnsibleActionFail("The argument 'studio_design' is not a dict")
        else:
            raise AnsibleActionFail("The argument 'studio_design' must be set")

        avdschema = AvdSchema(avd_schema)

        builder = AvdStudioBuilder(avdschema)
        result["ansible_facts"] = {}
        result["ansible_facts"]["studio"] =  builder.build(studio_design)
        return result
