# GNU General Public License v3.0+
#
# Copyright 2022 Arista Networks
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

DOCUMENTATION = r'''
---
module: validate
version_added: "3.6.0"
author: Arista Ansible Team (@aristanetworks)
short_description: Validate input data according to Schema
description:
  - The `arista.avd.validate` Action Plugin validates the input variables according to the supplied Schema
  - This is used in `arista.avd.eos_designs` and `arista.avd.eos_cli_config_gen`.
  - The Action Plugin supports both warning mode and error mode, to either block the playbook or just warn the user.
options:
  schema:
    description: Schema conforming to "AVD Meta Schema"
    required: True
    type: dict
  mode:
    description: Run the validation in either "error" or "warning" mode.
    required: False
    default: "warning"
    type: str
    choices: [ "error", "warning" ]
'''

EXAMPLES = r'''
- name: Validate input vars according to AVD eos_designs schema
  tags: [validate]
  arista.avd.validate:
    schema: "{{ lookup('ansible.builtin.file', schema_path) | from_yaml }}"
  delegate_to: localhost
'''
