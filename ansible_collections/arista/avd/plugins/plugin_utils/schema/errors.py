from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import jsonschema


class AristaAvdError(Exception):
    def __init__(self, message="An Error has occured in an arista.avd plugin"):
        self.message = message
        super().__init__(self.message)

    def _json_path_to_jinja(self, json_path):
        path = ""
        for index, elem in enumerate(json_path):
            if isinstance(elem, int):
                path += "[" + str(elem) + "]"
            else:
                if index == 0:
                    path += elem
                    continue
                path += "." + elem
        return path

class AvdSchemaError(AristaAvdError):
    def __init__(self, message = "Schema Error", error: jsonschema.SchemaError = None):
        if isinstance(error, jsonschema.SchemaError):
            self.message = f"'Schema Error: {self._json_path_to_jinja(error.absolute_path)}': {error.message}"
        else:
            self.message = message
        super().__init__(self.message)


class AvdValidationError(AristaAvdError):
    def __init__(self, message: str = "Schema Error", error: jsonschema.ValidationError = None):
        if isinstance(error, (jsonschema.ValidationError)):
            self.message = f"'Validation Error: {self._json_path_to_jinja(error.absolute_path)}': {error.message}"
        else:
            self.message = message
        super().__init__(self.message)
