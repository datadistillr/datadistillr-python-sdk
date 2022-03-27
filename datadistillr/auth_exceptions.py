"""
   Copyright 2021 DataDistillr Inc.
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


class AuthorizationException(Exception):
    """Exception raised for unauthorized attempts to access DataDistillr

    Attributes:
        url - Url which threw the error
        message - Explanation of the error
    """

    def __init__(self, url, message):
        self.url = url
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return repr(
            "{msg} {type} {url}".format(
                msg=self.message,
                type="Authentication Error: You are not authorized to access this resource: ",
                url=self.url,
            )
        )
