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


import functools
import platform
import sys

from pynpoint import exc
from pynpoint import utils


_registered_providers = []
_provider_mod = "pynpoint.providers"


def load_providers(providers=None, unload_first=True):
    if unload_first:
        _registered_providers = []

    if not providers:
        os_module = str.join(".", (_provider_mod, platform.system().lower()))
        providers = [os_module]  # Some ridiculous list.

    for provider in providers:
        try:
            _registered_providers.append(utils.import_object(provider))
        except exc.ClassNotFound:
            # Shit just went down here.
            raise

    return _registered_providers


def provides(provided, provider=None):
    if not provider:
        provider = _provider_mod

    def wrap(fn):
        def inner(*args, **kwargs):
            return fn(*args, **kwargs)

        _provider = sys.modules[provider]
        setattr(_provider, provided, inner)

        # Hack to make sure we're always displaying the right names.
        getattr(_provider, provided).__name__ = provided

        return inner
    return wrap


def command(*cmd, **kwargs):
    return utils.execute(*cmd, **kwargs).strip()
