from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleActionFail
from ansible_collections.arista.avd.plugins.plugin_utils.schema.avdschema import AristaAvdError, AvdSchema
from ansible.utils.display import Display


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

        mode = self._task.args.get("mode", "warning")

        error_counter = 0
        validation_errors = AvdSchema(schema).validate(task_vars)
        for validation_error in validation_errors:
            error_counter += 1
            if isinstance(validation_error, AristaAvdError):
                if mode == "error":
                    Display().error(f"[{task_vars['inventory_hostname']}]: {validation_error}", False)
                else:
                    Display().warning(f"[{task_vars['inventory_hostname']}]: {validation_error}", False)
        if error_counter:
            result['msg'] = f"{error_counter} errors found during schema validation of input vars."
            result['failed'] = (mode == "error")
        return result
