# Copyright (c) 2017, WSO2 Inc. (http://www.wso2.org) All Rights Reserved.
#
# WSO2 Inc. licenses this file to you under the Apache License,
# Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

from abc import ABCMeta
from future.utils import with_metaclass

from PySiddhi.sp.__Util import decodeField, encodeField


class NotSet(object):
    '''
    Denotes that a fields value is not set. (null)
    '''

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if isinstance(other, NotSet):
            return True
        return False


class APIObject(with_metaclass(ABCMeta, object)):
    '''
    Abstract Object representing a model used by Rest API
    '''

    def __new__(cls, *args, **kwargs):
        instance = object.__new__(cls)
        instance._field_mapping = None
        return instance

    def _setup(self, field_mapping):
        '''
        Setup the APIObject using field mapping details provided
        :param field_mapping: details on mappings between JSON object fields and  Python Class (model) fields
        :return: 
        '''
        self._field_mapping = field_mapping
        for k, v in field_mapping.items():
            setattr(self, k, v.default_value)

    def __ne__(self, other):
        '''
        Compare inequality between two API Objects
        :param other: 
        :return: 
        '''
        # Note: Python2 requires explicit declaration of __ne__ for proper operation.
        return not self.__eq__(other)

    def __eq__(self, other):
        '''
        Compare equality between two API Objects
        :param other: 
        :return: 
        '''
        if type(self) != type(other):
            return False
        for k, v in self._field_mapping.items():
            v1 = getattr(self, k, v.default_value)
            v2 = getattr(other, k, v.default_value)
            if (getattr(self, k, v.default_value) != getattr(other, k, v.default_value)):
                return False
        return True

    def toJSONObject(self):
        '''
        Obtain JSON object of the APIObject
        :return: 
        '''
        result = {}
        for k, v in self._field_mapping.items():
            val = getattr(self, k, v.default_value)
            if (v.addDefaultField or getattr(self, k, v.default_value) != v.default_value):
                result[k] = encodeField(getattr(self, k, v.default_value), v.encode_function)
        return result

    def _parse(self, jsonObject):
        '''
        Obtain APIObject using JSONObject
        :param jsonObject: 
        :return: 
        '''
        for k, v in self._field_mapping.items():
            if k in jsonObject.keys():
                setattr(self, k, decodeField(jsonObject[k], v.decode_function))
            else:
                setattr(self, k, v.default_value)
