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

from PySiddhi.sp.ObjectMapping.APIObject import NotSet
from PySiddhi.sp.__Util import encodeField, decodeField


def strOrInt(v):
    '''
    Determines whether v is String or Integer and returns appropriate object.
    :param v: 
    :return: 
    '''
    v = str(v)
    if str.isnumeric(v):
        return int(v)
    else:
        return v


class FieldMapping(object):
    '''
    Describes a mapping of a field between JSON Object and APIObject
    '''

    def __init__(self, decode_function, encode_function=str, default_value=NotSet(), addDefaultField=False):
        '''
        Creates a field mapping between JSON Object field and API Object field
        :param decode_function: converts JSON field value to APIObject field value 
        :param encode_function: converts APIObject field value JSON Object field value 
        :param default_value: default value of APIObject field
        :param addDefaultField: set True to include the field in JSON Object even if the value is default
        '''
        self.encode_function = encode_function
        self.decode_function = decode_function
        self.default_value = default_value
        self.addDefaultField = addDefaultField


class ListFieldMapping(FieldMapping):
    '''
    Describes a mapping between List of API Objects and a List of JSON Objects
    '''

    def __init__(self, decode_function, encode_function, default_value=[]):
        '''
        Creates a mapping between a List of API Objects and a List of JSON Objects
        :param decode_function: converts a JSON Object List item APIObject List item
        :param encode_function: converts an APIObject List item to JSON Object List item
        :param default_value: default value to be used when field (associating List) is absent
        '''

        def encode_func(input_object):
            result_object = []
            for item in input_object:
                result_object.append(encodeField(item, encode_function))
            return result_object

        def decode_func(input_object):
            result_object = []
            for item in input_object:
                result_object.append(decodeField(item, decode_function))
            return result_object

        FieldMapping.__init__(self, decode_func, encode_func, default_value)
