from functools import cached_property

from ansible_collections.arista.avd.plugins.plugin_utils.avdfacts import AvdFacts
from ansible_collections.arista.avd.plugins.plugin_utils.utils import get


class AvdValidation(AvdFacts):
    @cached_property
    def avd_validation(self):
        avd_validation = {"commands": []}
        ntp_servers = get(self._hostvars, "ntp.servers")
        if ntp_servers is not None:
            avd_validation["commands"].append({"command": "show ntp status", "output": "json"})
            avd_validation["tests"] = []
            avd_validation["tests"].append(
                {"category": "NTP", "description": "Synchronized with NTP server", "asserts": [{"path": "show_ntp_status['status']", "result": "synchronised"}]}
            )
            return avd_validation
