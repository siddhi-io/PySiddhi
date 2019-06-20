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

from enum import Enum

from PySiddhi.sp.ObjectMapping.APIObject import APIObject, NotSet
from PySiddhi.sp.ObjectMapping.FieldMapping import FieldMapping, ListFieldMapping
from PySiddhi.sp.__Util import decodeField, decodeObject


class AttributeConfiguration(APIObject):
    '''
    Attribute Configuration API Object, which is an attribute of SimulationSource
    '''

    class Type(Enum):
        '''
        Type of Attribute Configuration
        '''
        CUSTOM_DATA_BASED = "CUSTOM_DATA_BASED"
        PRIMITIVE_BASED = "PRIMITIVE_BASED"
        REGEX_BASED = "REGEX_BASED"
        PROPERTY_BASED = "PROPERTY_BASED"

        @classmethod
        def encode(cls, v):
            return v.value

        @classmethod
        def decode(cls, v):
            return AttributeConfiguration.Type(v)

    class PrimitiveType(Enum):
        '''
        Type of primitive data type involved
        '''
        LONG = "LONG"
        INT = "INT"
        STRING = "STRING"
        FLOAT = "FLOAT"
        DOUBLE = "DOUBLE"

        @classmethod
        def encode(cls, v):
            return v.value

        @classmethod
        def decode(cls, v):
            return AttributeConfiguration.Type(v)

    def __init__(self, type, min=NotSet(), max=NotSet(), length=NotSet(), precision=NotSet(), list=NotSet(),
                 pattern=NotSet(),
                 primitiveType=NotSet(), property=NotSet()):
        '''
        Instantiates Attribute Configuration API Object
        :param type: Type of AttributeConfiguration
        :param min: 
        :param max: 
        :param length: 
        :param precision: 
        :param list: 
        :param pattern: 
        :param primitiveType: PrimitiveType involved
        :param property: 
        '''
        self._setup(
            field_mapping={"type": FieldMapping(AttributeConfiguration.Type.decode, AttributeConfiguration.Type.encode),
                           "length": FieldMapping(int),
                           "min": FieldMapping(int), "max": FieldMapping(int),
                           "precision": FieldMapping(int), "list": ListFieldMapping(str, str, NotSet()),
                           "pattern": FieldMapping(str), "property": FieldMapping(str),
                           "primitiveType": FieldMapping(AttributeConfiguration.PrimitiveType.decode,
                                                         AttributeConfiguration.PrimitiveType.encode)})
        self.type = type
        self.length = length
        self.min = min
        self.max = max
        self.precision = precision
        self.list = list
        self.pattern = pattern
        self.primitiveType = primitiveType
        self.property = property

    @classmethod
    def parse(cls, jsonObject):
        '''
        Converts a Python Class Object (from JSON) to AttributeConfiguration
        :param jsonObject: 
        :return: 
        '''
        result = AttributeConfiguration(type=decodeField(jsonObject["type"], str))
        result._parse(jsonObject)
        return result
