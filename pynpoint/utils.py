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

import os
import subprocess
import sys

from pynpoint import exc


def import_class(import_str):
    """Returns a class from a string including module and class."""
    mod_str, _sep, class_str = import_str.rpartition('.')
    try:
        __import__(mod_str)
        return getattr(sys.modules[mod_str], class_str)
    except (ImportError, ValueError, AttributeError), e:
        raise exc.ClassNotFound(class_name=class_str)


def import_object(import_str):
    """Returns an object including a module or module and class."""
    try:
        __import__(import_str)
        return sys.modules[import_str]
    except ImportError:
        cls = import_class(import_str)
        return cls()


def execute(*cmd, **kwargs):
    """Execute a command."""

    _input = kwargs.pop('input', None)
    _pipe = subprocess.PIPE
    
    cmd = map(str, cmd)
    sub = subprocess.Popen(cmd, env=os.environ.copy(),
                           stdin=_pipe, stderr=_pipe, stdout=_pipe,)

    
    stdout, stderr = sub.communicate(input=_input)

    if sub.returncode or stderr: 
        raise exc.ExecutionError(stdout=stdout,
                                 stderr=stderr,
                                 return_code=sub.returncode,
                                 cmd=str.join(' ', cmd))

    return stdout
