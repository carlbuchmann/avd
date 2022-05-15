from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import yaml
from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleActionFail
from ansible.utils.vars import isidentifier
from ansible.module_utils.common import file
from ansible_collections.arista.avd.plugins.module_utils.strip_empties import strip_null_from_data
from ansible_collections.arista.avd.plugins.plugin_utils.schema.avd_schema import AvdSchemaError, AvdSchema, AvdValidationError
from jsonschema import ValidationError
from datetime import datetime
from ansible.module_utils._text import to_text
from ansible.utils.display import Display


def json_path(absolute_path):
    path = ""
    for elem in absolute_path:
        if isinstance(elem, int):
            path += "[" + str(elem) + "]"
        else:
            path += "." + elem
    return path[1:]


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = {}

        self._result = super().run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        if self._task.args and "schema" in self._task.args:
            schema = self._task.args["schema"]
            if not isinstance(schema, dict):
                raise AnsibleActionFail("The argument 'schema' is not a dict")
        else:
            raise AnsibleActionFail("The argument 'schema' must be set")

        self.validate(schema, task_vars)
        return self._result

    def validate(self, schema, task_vars):
        validation_errors = sorted(AvdSchema(schema).validate(task_vars), key=lambda e: e.path)
        if validation_errors:
            for validation_error in validation_errors:
                if isinstance(validation_error, ValidationError):
                    Display().error(f"'{json_path(validation_error.absolute_path)}': {validation_error.message}", False)
            self._result['msg'] = f"{len(validation_errors)} errors found during schema validation of input vars."
            self._result['failed'] = True
