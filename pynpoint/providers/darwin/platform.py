# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2011 Christopher MacGown. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

from pynpoint import providers

__module__ = str.join('.', (__package__, "platform"))

# todo(chris): Clean this up when daemonized.
__platform__ =  dict([str.split(l, ":\t") for l
                                          in providers.command(
                                                        "/usr/bin/sw_vers")])


@providers.provides(provider=__module__)
def platform():
    return __platform__["ProductName"]


@providers.provides(provider=__module__)
def platform_version():
    return __platform__["ProductVersion"]


@providers.provides(provider=__module__)
def platform_build():
    return __platform__["BuildVersion"]
