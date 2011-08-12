"""
   Copyright 2010 Christopher MacGown

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

class RequestError(Exception):
    """ Common exception for Request Handlers """
    pass


class ProtocolError(Exception):
    """ A generic protocol error class """
    # TODO(chris): Handle logging here.
    pass


class ClassNotFound(IOError):
    def __init__(self, class_name=None):
        message = "Could not import %(class_name)s" % locals()

        super(IOError, self).__init__(message)


class ExecutionError(IOError):
    def __init__(self, stdout=None, stderr=None, return_code=None, cmd=None): 
        message = ("Command failed: %(cmd)s\n"
                   "return_code: %(return_code)s\n"
                   "stdout: %(stdout)r\n"
                   "stderr: %(stderr)r\n" % locals())

        super(IOError, self).__init__(message)
