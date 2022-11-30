from functools import cached_property

from ansible_collections.arista.avd.plugins.plugin_utils.avdfacts import AvdFacts
from ansible_collections.arista.avd.plugins.plugin_utils.utils import get


class AvdAsserts(AvdFacts):
    @cached_property
    def avd_asserts(self):
        avd_asserts = []

        avd_validation_tests = get(self._hostvars, "avd_validation[tests]")
        for avd_validation_test in avd_validation_tests:
            return avd_asserts
