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


from PySiddhi import SiddhiLoader
from PySiddhi.DataTypes.DoubleType import DoubleType
from PySiddhi.DataTypes.LongType import LongType

'''
Data Wrapping is used because python 3 doesn't distinctly support long and double data types
'''


def unwrapDataItem(d):
    '''
    Unwraps a data item (String, float, int, long) sent from Java Proxy Classes
    :param d: 
    :return: 
    '''
    if d.isNull():
        return None
    elif d.isLong():
        return LongType(d.getData())
    elif d.isDouble():
        return DoubleType(d.getData())
    return d.getData()


def unwrapDataList(d):
    '''
    Unwraps a list of data sent from Java Proxy Classes
    :param d: 
    :return: 
    '''
    results = []
    for r in d:
        results.append(unwrapDataItem(r))
    return results


def unwrapData(data):
    '''
    Unwraps a data object sent from Java Proxy Classes
    :param data: 
    :return: 
    '''
    if isinstance(data, list):
        return unwrapDataList(data)
    else:
        return unwrapDataItem(data)


def wrapDataItem(d):
    '''
    Wraps a data item (int, long, string or float) , making it suitable to be transfered to Java Proxy
    :param d: 
    :return: 
    '''
    wrapped_data_proxy = SiddhiLoader._loadType("io.siddhi.pythonapi.DataWrapProxy")
    wrapped_data = None
    if d is None:
        # Constructor for null type
        wrapped_data = wrapped_data_proxy(0, False, True)
    elif type(d) is LongType:
        # Consutrctor for Long Type
        wrapped_data = wrapped_data_proxy(d, True)
    elif type(d) is DoubleType:
        wrapped_data = wrapped_data_proxy(d, False, False, True)
    else:
        wrapped_data = wrapped_data_proxy(d)
    return wrapped_data


def wrapDataList(data):
    '''
    Wraps a list of data, making it suitable for transfer to java proxy classes
    :param data: 
    :return: 
    '''
    results = []
    for d in data:
        results.append(wrapData(d))
    return results


def wrapData(data):
    '''
    Wraps a data object (List or item) to suite transmission to Java proxy classes
    :param data: 
    :return: 
    '''
    if isinstance(data, list):
        return wrapDataList(data)
    else:
        return wrapDataItem(data)


def unwrapHashMap(map):
    '''
    Obtains a copy of a Java HashMap as a Dictionary
    :param map: 
    :return: 
    '''
    if (not isinstance(map, SiddhiLoader._JavaClass)) or (
            map.__javaclass__ != "java/util/Map" and map.__javaclass__ != "java/util/HashMap"):
        return map
        # TODO: Should prevent exposure of subtypes of ComplexEvent
    results = {}
    entry_set = map.entrySet().toArray()
    for v in entry_set:
        if v.value is None:
            results[v.key] = None
        else:
            results[v.key] = unwrapHashMap(v.value)
    return results
