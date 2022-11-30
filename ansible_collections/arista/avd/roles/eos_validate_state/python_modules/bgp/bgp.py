from functools import cached_property

from ansible_collections.arista.avd.plugins.plugin_utils.avdfacts import AvdFacts
from ansible_collections.arista.avd.plugins.plugin_utils.utils import get


class AvdValidation(AvdFacts):
    @cached_property
    def avd_validation(self):
        service_routing_protocols_model = get(self._hostvars, "service_routing_protocols_model")
        if service_routing_protocols_model == "multi-agent":
            avd_validation = {"commands": []}
            avd_validation["commands"].append({"command": "show ip route summary", "output": "json"})
            avd_validation["tests"] = []
            avd_validation["tests"].append({"category": "NTP", "description": "Synchronized with NTP server"})
        return avd_validation
