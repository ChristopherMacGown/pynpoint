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

__module__ = str.join('.', (__package__, "ps"))

PS_RE = re.compile(r"(?P<uid>\d+)\s+"
                   r"(?P<pid>\d+)\s+"
                   r"(?P<ppid>\d+)\s+"
                   r"(?P<cpu>\d+)\s+"
                   r"(?P<start_time>.*?)\s+"
                   r"(?P<tty>\?\?|ttys\d+)\s+"
                   r"(?P<time>.*?)\s+"
                   r"(?P<command>.*)")

@providers.provides(provider=__module__)
def ps():
    _processes = []
    for process in providers.command("ps", "-ef"):
        match = PS_RE.search(process)
        if match:
            _processes.append(match.groupdict())
    return _processes
