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

__module__ = str.join('.', (__package__, "kernel"))


MEMADDR_RE_STR = "(0x[0-9a-f]+)"
KERNEL_MODULE_RE = re.compile(r"(?P<index>\d+)\s+"
                              r"(?P<refs>(\d+))\s+"
                              r"(?P<address>%(MEMADDR_RE_STR)s)\s+"
                              r"(?P<size>%(MEMADDR_RE_STR)s)\s+"
                              r"(?P<wired>%(MEMADDR_RE_STR)s)\s+"
                              r"(?P<name>([a-zA-Z0-9\.]+)) "
                              r"\((?P<version>[0-9\.]+)\)" % locals())


@providers.provides(provider=__module__)
def kernel():
    _kernel = {}
    _kernel["name"] = providers.command("uname", "-s")
    _kernel["release"] = providers.command("uname", "-v")
    _kernel["machine"] = providers.command("uname", "-m")
    _kernel["version"] = providers.command("uname", "-r")

    return _kernel


@providers.provides(provider=__module__)
def modules():
    def munge(k, v):
        if re.match(MEMADDR_RE_STR, v) or k == "refs":
            v = int(v, 0)

        return k, v

    _modules = {}
    for module in providers.command("kextstat", "-k", "-l"):
        match = KERNEL_MODULE_RE.search(module)
        if match:
            match = dict([munge(k, v) for k, v in match.groupdict().items()])
            _modules[match.pop('name')] = match
    return _modules
