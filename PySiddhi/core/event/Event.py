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

from PySiddhi.DataTypes import DataWrapper
from PySiddhi.core.event import ComplexEvent

_event_class = SiddhiLoader._loadType("io.siddhi.core.event.Event")
_event_proxy_class = SiddhiLoader._loadType("io.siddhi.pythonapi.proxy.core.event.event.EventProxy")
_event_proxy_class_inst = _event_proxy_class()


class Event(object):
    '''
    Wrapper on @io.siddhi.core.event.Event
    '''

    @classmethod
    def _fromEventProxy(cls, event_proxy):
        '''
        Internal Constructor to wrap around JAVA class Event
        :param event_proxy:
        :return:
        '''
        if event_proxy is None:
            return None
        instance = cls.__new__(cls)
        instance._event_proxy = event_proxy
        return instance

    def __init__(self, dataSizeOrTimeStamp=None, data=None, dataSize=None, timeStamp=None):
        '''
        Constructor. Refer the Java Documentation for optional parameters and possible combinations.
        :param dataSizeOrTimeStamp: DataSize or TimeStamp of event
        :param data: Data as a List of same type objects
        :param dataSize: Size of Data
        :param timeStamp: Timestamp
        '''
        if dataSizeOrTimeStamp is None and data is None and dataSize is None and timeStamp is None:
            self._event_proxy = _event_class()
        elif dataSizeOrTimeStamp is not None and data is None and dataSize is None and timeStamp is None:
            self._event_proxy = _event_class(int(dataSizeOrTimeStamp))
        elif dataSizeOrTimeStamp is not None and data is not None and dataSize is None and timeStamp is None:
            self._event_proxy = _event_proxy_class_inst.createEvent(dataSizeOrTimeStamp, DataWrapper.wrapDataList(data))
        elif dataSizeOrTimeStamp is None and data is None and timeStamp is None and dataSize is not None:
            self._event_proxy = _event_class(int(dataSize))
        elif dataSizeOrTimeStamp is None and data is not None and timeStamp is not None and dataSize is None:
            self._event_proxy = _event_class(timeStamp, data)
        else:
            raise NotImplementedError("Unknown constructor parameter combination")

    def __str__(self):
        '''
        ToString
        :return: 
        '''
        return self._event_proxy.toString()

    def getId(self):
        '''
        Get event id
        :return: 
        '''
        return self._event_proxy.getId()

    def setId(self, value):
        '''
        Set event id
        :param value: 
        :return: 
        '''
        self._event_proxy.setId(value)

    def getTimestamp(self):
        '''
        Retrieve timestamp
        :return: 
        '''
        return self._event_proxy.getTimestamp()

    def setTimestamp(self, value):
        '''
        Set timestamp
        :param value: 
        :return: 
        '''
        self._event_proxy.setTimestamp(value)

    def getData(self, index=None):
        '''
        Retrieve data as a list (if index not specified) or datum at index (if index specified)
        :param index: Index (optional)
        :return: 
        '''
        if index is None:
            return DataWrapper.unwrapDataList(_event_proxy_class_inst.getData(self._event_proxy))
        else:
            data = _event_proxy_class_inst.getDataItem(self._event_proxy, index)
            if data is None:
                return None
            return DataWrapper.unwrapDataItem(data)

    def setData(self, data):
        '''
        Set data as a list
        :param data: 
        :return: 
        '''
        _event_proxy_class_inst.setData(self._event_proxy, DataWrapper.wrapDataList(data))

    def isExpired(self):
        '''
        Retrieve whether event has expired
        :return: 
        '''
        return self._event_proxy.isExpired()

    def setExpired(self, value):
        '''
        Set whether event has expired
        :param value: 
        :return: 
        '''
        if value:
            _event_proxy_class_inst.makeExpired(self._event_proxy)
        else:
            _event_proxy_class_inst.makeUnExpired(self._event_proxy)

    def copyFrom(self, event):
        '''
        Copy values from an event
        :param event: source event
        :return: 
        '''
        if isinstance(event, Event):
            self._event_proxy.copyFrom(event._event_proxy)
        elif isinstance(event, ComplexEvent.ComplexEvent):
            self._event_proxy.copyFrom(event._complex_event_proxy)

    def __eq__(self, other):
        '''
        Test for equality
        :param other: 
        :return: 
        '''
        if isinstance(other, Event):
            return self._event_proxy.equals(other._event_proxy)
        else:
            return False

    def equals(self, other):
        '''
        Test for equality with other event
        :param other: 
        :return: 
        '''
        return self == other

    def __hash__(self):
        '''
        Obtains hashCode of event
        :return: 
        '''
        return self._event_proxy.hashCode()
