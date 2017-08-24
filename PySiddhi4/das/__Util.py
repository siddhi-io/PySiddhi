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

def encodeField(value, encode_function=str):
    '''
    Encodes a field value using encode_function
    :param value: 
    :param encode_function: 
    :return: 
    '''
    if value is None:
        return None
    return encode_function(value)


def decodeField(value, decode_function):
    '''
    Decodes a field value using given decode_function
    :param value: 
    :param decode_function: 
    :return: 
    '''
    if value is None:
        return None
    return decode_function(value)


def decodeObject(jsonObject, target, decodeMap):
    '''
    Decodes a JSON Object and assigns attributes to target.
    :param jsonObject: 
    :param target: 
    :param decodeMap: 
    :return: 
    '''
    for (key, value) in jsonObject.items():
        setattr(target, key, decodeField(value, decodeMap[key]))
    return target
