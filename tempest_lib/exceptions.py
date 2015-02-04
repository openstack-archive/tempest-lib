# Copyright 2012 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import testtools


class TempestException(Exception):
    """Base Tempest Exception

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """
    message = "An unknown exception occurred"

    def __init__(self, *args, **kwargs):
        super(TempestException, self).__init__()
        try:
            self._error_string = self.message % kwargs
        except Exception:
            # at least get the core message out if something happened
            self._error_string = self.message
        if len(args) > 0:
            # If there is a non-kwarg parameter, assume it's the error
            # message or reason description and tack it on to the end
            # of the exception message
            # Convert all arguments into their string representations...
            args = ["%s" % arg for arg in args]
            self._error_string = (self._error_string +
                                  "\nDetails: %s" % '\n'.join(args))

    def __str__(self):
        return self._error_string


class RestClientException(TempestException,
                          testtools.TestCase.failureException):
    pass


class InvalidHttpSuccessCode(RestClientException):
    message = "The success code is different than the expected one"


class NotFound(RestClientException):
    message = "Object not found"


class Unauthorized(RestClientException):
    message = 'Unauthorized'


class Forbidden(RestClientException):
    message = "Forbidden"


class TimeoutException(RestClientException):
    message = "Request timed out"


class BadRequest(RestClientException):
    message = "Bad request"


class UnprocessableEntity(RestClientException):
    message = "Unprocessable entity"


class RateLimitExceeded(RestClientException):
    message = "Rate limit exceeded"


class OverLimit(RestClientException):
    message = "Quota exceeded"


class ServerFault(RestClientException):
    message = "Got server fault"


class NotImplemented(RestClientException):
    message = "Got NotImplemented error"


class Conflict(RestClientException):
    message = "An object with that identifier already exists"


class ResponseWithNonEmptyBody(RestClientException):
    message = ("RFC Violation! Response with %(status)d HTTP Status Code "
               "MUST NOT have a body")


class ResponseWithEntity(RestClientException):
    message = ("RFC Violation! Response with 205 HTTP Status Code "
               "MUST NOT have an entity")


class InvalidHTTPResponseBody(RestClientException):
    message = "HTTP response body is invalid json or xml"


class InvalidHTTPResponseHeader(RestClientException):
    message = "HTTP response header is invalid"


class InvalidContentType(RestClientException):
    message = "Invalid content type provided"


class UnexpectedResponseCode(RestClientException):
    message = "Unexpected response code received"


class InvalidStructure(TempestException):
    message = "Invalid structure of table with details"


class CommandFailed(Exception):
    def __init__(self, returncode, cmd, output, stderr):
        super(CommandFailed, self).__init__()
        self.returncode = returncode
        self.cmd = cmd
        self.stdout = output
        self.stderr = stderr

    def __str__(self):
        return ("Command '%s' returned non-zero exit status %d.\n"
                "stdout:\n%s\n"
                "stderr:\n%s" % (self.cmd,
                                 self.returncode,
                                 self.stdout,
                                 self.stderr))
