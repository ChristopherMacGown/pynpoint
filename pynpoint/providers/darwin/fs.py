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

__module__ = str.join('.', (__package__, "fs"))


BLOCK_SIZE_RE = re.compile(r"Filesystem\s+(?P<block_size>\d+)-blocks")
DF_RE = re.compile(r"(?P<device>.*?)\s+"
                   r"(?P<blocks>\d+)\s+"
                   r"(?P<blocks_used>\d+)\s+"
                   r"(?P<blocks_avail>\d+)\s+"
                   r"(?P<percent_used>\d+)%\s+"
                   r"(?P<mountpoint>.*)")
MOUNTS_RE = re.compile(r"(?P<device>.*)\s+on\s+"
                       r"(?P<mountpoint>.*?)\s+"
                       r"\((?P<fs_type>.*?),\s+"
                       r"(?P<options>.*)\)")


@providers.provides(provider=__module__)
def mount():
    _mounts = {}
    for mount in providers.command("mount"):
        match = MOUNTS_RE.search(mount)
        if match:
            match = match.groupdict()
            match['options'] = str.split(match['options'], ', ')
            _mounts[match.pop('device')] = match
    return _mounts


@providers.provides(provider=__module__)
def df():
    def munge(k, v):
        if re.match("\d+", v):
            v = int(v)
            if "blocks" in k:
                k = re.sub("blocks", "kb", k)
                v = v / (1024 / _block_size)
        return k, v

    _df = providers.command("df")
    _block_size = int(BLOCK_SIZE_RE.search(_df[0]).group("block_size"))

    _mounts = {}
    for mount in _df:
        match = DF_RE.search(mount)
        if match:
            match = dict([munge(k, v) for k, v in match.groupdict().items()])
            _mounts[match.pop('device')] = match
    return _mounts
