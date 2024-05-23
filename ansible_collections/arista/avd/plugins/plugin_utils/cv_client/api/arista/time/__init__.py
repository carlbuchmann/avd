# Copyright (c) 2024 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: arista/time/time.proto
# plugin: python-aristaproto
# This file has been @generated

from dataclasses import dataclass
from datetime import datetime

try:
    import aristaproto
except ImportError:
    HAS_ARISTAPROTO = False
    from ansible_collections.arista.avd.plugins.plugin_utils.cv_client.mocked_classes import mocked_aristaproto as aristaproto
else:
    HAS_ARISTAPROTO = True


@dataclass(eq=False, repr=False)
class TimeBounds(aristaproto.Message):
    start: datetime = aristaproto.message_field(1)
    end: datetime = aristaproto.message_field(2)
