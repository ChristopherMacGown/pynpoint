# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2011 Christopher MacGown. All Rights Reserved.
# Copyright 2011 Piston Cloud Computer, Inc. All Rights Reserved.
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

__module__ = str.join('.', (__package__, "network"))


INTERFACE_RE = re.compile("(?P<int>\w+):\s+flags=(?P<flags>.*?)\s+"
                          "mtu\s+(?P<mtu>\d+)")

INTERFACE_CONFIG_REGEXES = {
    "ether": re.compile("\s+ether\s+(?P<mac>([a-zA-Z0-9]{2}:){5}"
                        "[a-zA-Z0-9]{2})"),
    "inet6": re.compile("\s+inet6\s+(?P<inet6>.*)\s+prefixlen\s+"
                        "(?P<prefixlen>\d+)\s+scopeid\s+"
                        "(?P<scopeid>[a-fA-Fx0-9]+)"),
    "inet": re.compile("\s+inet\s+(?P<inet>(\d+\.){3}\d+)\s+netmask\s+"
                       "(?P<netmask>[0-9a-fA-Fx]+)\s+broadcast\s+"
                       "(?P<broadcast>(\d+\.){3}\d+)"),
    "options": re.compile("\s+options=(?P<options>.*)"),
    "media": re.compile("\s+media:\s+(?P<media>.*)"),
    "status": re.compile("\s+status:\s+(?P<status>.*)"),
}


@providers.provides(provider=__module__)
def interfaces():
    _interfaces = {}

    current_interface = None

    for line in providers.command("ifconfig", "-a"):
        match = INTERFACE_RE.match(line)
        if match:
            match = match.groupdict()
            
            interface = match.pop('int')
            current_interface = _interfaces[interface] = match
        else:
            if not current_interface:
                continue
            
            for key, regex in INTERFACE_CONFIG_REGEXES.items():
                match = regex.match(line)

                if match:
                    match = match.groupdict()

                    if "inet" in key:
                        if not current_interface.get(key):
                            current_interface[key] = []
                        current_interface[key].append(match)
                    else:
                        current_interface.update(match)
                    break
    return _interfaces


@providers.provides(provider=__module__)
def routes():
    _routes = {}

    for route in providers.command("netstat", "-rn"):
        if "default" in route:


