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

import datetime
import re
import time

from pynpoint import providers

__module__ = str.join('.', (__package__, "uptime"))

# todo(chris): Make this work when pynpoint is daemonized.
UPTIME_RE = re.compile("kern.boottime:.*\s+(?P<uptime_secs>\d+),")
m = UPTIME_RE.search(providers.command("sysctl", "kern.boottime"))
UPTIME = int(m.group("uptime_secs"))
CURR_TIME = time.time()


@providers.provides(provider=__module__)
def uptime_secs():
    """Exposes the number of seconds the box has been up."""
    return int(CURR_TIME - UPTIME)


@providers.provides(provider=__module__)
def uptime():
    """Exposes the current uptime of the box in human readable format."""
    cur_dt = datetime.datetime.fromtimestamp(CURR_TIME)
    upt_dt = datetime.datetime.fromtimestamp(UPTIME)

    return str(cur_dt - upt_dt)
