from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import yaml
from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleActionFail
from ansible.utils.vars import isidentifier
from ansible.module_utils.common import file
from ansible_collections.arista.avd.plugins.module_utils.strip_empties import strip_null_from_data
from ansible_collections.arista.avd.plugins.plugin_utils.schema.avd_schema import AvdSchemaError, AvdSchema
from datetime import datetime

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = {}

        result = super().run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        if self._task.args and "schema" in self._task.args:
            schema = self._task.args["schema"]
            if not isinstance(schema, dict):
                raise AnsibleActionFail("The argument 'schema' is not a dict")
        else:
            raise AnsibleActionFail("The argument 'schema' must be set")

        AvdSchema(schema).validate(task_vars)

        return result
