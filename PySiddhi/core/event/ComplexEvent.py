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
from PySiddhi import SiddhiLoader
from PySiddhi.DataTypes.DataWrapper import unwrapData, wrapData


class ComplexEvent(object):
    '''
    Wrapper on @io.siddhi.core.event.ComplexEvent
    '''

    class Type(Enum):
        CURRENT = SiddhiLoader._loadType(
            "io.siddhi.pythonapi.proxy.core.event.complex_event.TypeProxy")().CURRENT(),
        EXPIRED = SiddhiLoader._loadType(
            "io.siddhi.pythonapi.proxy.core.event.complex_event.TypeProxy")().EXPIRED(),
        TIMER = SiddhiLoader._loadType("io.siddhi.pythonapi.proxy.core.event.complex_event.TypeProxy")().TIMER(),
        RESET = SiddhiLoader._loadType("io.siddhi.pythonapi.proxy.core.event.complex_event.TypeProxy")().RESET()

        @classmethod
        def _map_value(cls, type_proxy):
            type_value = None
            if type_proxy.isValueCurrent():
                type_value = ComplexEvent.Type.CURRENT
            elif type_proxy.isValueExpired():
                type_value = ComplexEvent.Type.EXPIRED
            elif type_proxy.isValueTimer():
                type_value = ComplexEvent.Type.TIMER
            elif type_proxy.isValueReset():
                type_value = ComplexEvent.Type.RESET
            else:
                raise TypeError("Unknown Complex Event Type")
            return ComplexEvent.Type(type_value)

    def __init__(self, ):
        raise NotImplementedError("Complex Event is Abstract")

    def __new__(cls):
        bare_instance = object.__new__(cls)
        bare_instance._complex_event_proxy = None
        return bare_instance

    @classmethod
    def _fromComplexEventProxy(cls, complex_event_proxy):
        '''
        Internal Constructor to wrap around JAVA Interface Complex Event
        :param complex_event_proxy:
        :return:
        '''
        if complex_event_proxy is None:
            return None
        instance = cls.__new__(cls)
        instance._complex_event_proxy = complex_event_proxy
        return instance

    def getNext(self):
        next_proxy = self._complex_event_proxy.getNext()
        return ComplexEvent._fromComplexEventProxy(next_proxy)

    def setNext(self, next_event):
        self._complex_event_proxy.setNext(next_event._complex_event_proxy)

    next = property(getNext, setNext)

    def getOutputData(self):
        complex_event_static_proxy = SiddhiLoader._loadType(
            "io.siddhi.pythonapi.proxy.core.event.complex_event.ComplexEventProxy")()
        output_data = unwrapData(complex_event_static_proxy.getOutputData(self._complex_event_proxy))
        return output_data

    def setOutputData(self, datum, index):
        complex_event_static_proxy = SiddhiLoader._loadType(
            "io.siddhi.pythonapi.proxy.core.event.complex_event.ComplexEventProxy")()
        complex_event_static_proxy.setOutputData(self._complex_event_proxy, wrapData(datum), index)

    def getTimestamp(self):
        return self._complex_event_proxy.getTimestamp()

    timestamp = property(fget=getTimestamp, fset=None)

    def getAttribute(self, position):
        return self._complex_event_proxy.getAttribute(position)

    def setAttribute(self, value, position):
        # TODO: Improve logic here by adding support to long. Will need to make a java wrapping for handling long
        self._complex_event_proxy.setAttribute(value, position)

    def getType(self):
        raw_type_proxy = self._complex_event_proxy.getType()
        type_proxy = SiddhiLoader._loadType("io.siddhi.pythonapi.proxy.core.event.complex_event.TypeProxy")(
            raw_type_proxy)
        return ComplexEvent.Type._map_value(type_proxy)

    def setType(self, type):
        self._complex_event_proxy.setType(type.value())

    type = property(getType, setType)
