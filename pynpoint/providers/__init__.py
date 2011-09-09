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


def inject_provider_caller(package):
    _injections = {"__providers__": [],
                   "gather": lambda: dict([(k, v()) for k, v
                                                    in package.__providers__]),
                  }

    for name, injection in _injections.items():
        if not getattr(package, name, None):
            setattr(package, name, injection)


def provides(provider=_provider_mod):
    def wrap(fn):
        def inner(*args, **kwargs):
            return fn(*args, **kwargs)

        provided = fn.__name__
        _provider = sys.modules[provider]
        _parent = sys.modules[_provider.__package__]
        inject_provider_caller(_parent)
        inject_provider_caller(_provider)
        setattr(_provider, provided, inner)

        # Hack to make sure we're always displaying the right names.
        new_fn = getattr(_provider, provided)
        new_fn.__name__ = provided

        _parent.__providers__.append((provider.split('.')[-1], 
                                      _provider.gather))
        _provider.__providers__.append((provided, new_fn))

        return inner
    return wrap


def command(*cmd, **kwargs):
    split_char = kwargs.pop('split_char', "\n")
    res = str.split(utils.execute(*cmd, **kwargs).strip(), split_char)

    return res if len(res) > 1 else res[0]
