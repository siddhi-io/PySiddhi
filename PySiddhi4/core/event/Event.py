import PySiddhi4.core
from PySiddhi4 import SiddhiLoader

from PySiddhi4.DataTypes import DataWrapper
from PySiddhi4.DataTypes.LongType import LongType
from PySiddhi4.core.event import ComplexEvent

_event_class = SiddhiLoader._loadType("org.wso2.siddhi.core.event.Event")
_event_proxy_class = SiddhiLoader._loadType("org.wso2.siddhi.pythonapi.proxy.core.event.event.EventProxy")
_event_proxy_class_inst = _event_proxy_class()

class Event(object):
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


    def __init__(self, dataSizeOrTimeStamp=None,data=None, dataSize = None, timeStamp = None):
        if dataSizeOrTimeStamp is None and data is None and dataSize is None and timeStamp is None:
            self._event_proxy = _event_class()
        elif dataSizeOrTimeStamp is not None and data is None and dataSize is None and timeStamp is None:
            self._event_proxy = _event_class(int(dataSizeOrTimeStamp))
        elif dataSizeOrTimeStamp is not None and data is not None and dataSize is None and timeStamp is None:
            self._event_proxy = _event_proxy_class_inst.createEvent(dataSizeOrTimeStamp, DataWrapper.wrapDataList(data))
        elif dataSizeOrTimeStamp is None and data is None and timeStamp is None and dataSize is not None:
            self._event_proxy = _event_class(int(dataSize))
        elif dataSizeOrTimeStamp is None and data is not None and timeStamp is not None and dataSize is None:
            self._event_proxy = _event_class(timeStamp,data)
        else:
            raise NotImplementedError("Unknown constructor parameter combination")

    def __str__(self):
        return self._event_proxy.toString()

    def getId(self):
        return self._event_proxy.getId()

    def setId(self, value):
        self._event_proxy.setId(value)

    def getTimestamp(self):
        return self._event_proxy.getTimestamp()

    def setTimestamp(self,value):
        self._event_proxy.setTimestamp(value)

    def getData(self, index=None):
        if index is None:
            return DataWrapper.unwrapDataList(_event_proxy_class_inst.getData(self._event_proxy))
        else:
            data = _event_proxy_class_inst.getDataItem(self._event_proxy, index)
            if data is None:
                return None
            return DataWrapper.unwrapDataItem(data)

    def setData(self, data):
         _event_proxy_class_inst.setData(self._event_proxy, DataWrapper.wrapDataList(data))

    def isExpired(self):
        return self._event_proxy.isExpired()

    def setExpired(self,value):
        if value:
            _event_proxy_class_inst.makeExpired(self._event_proxy)
        else:
            _event_proxy_class_inst.makeUnExpired(self._event_proxy)

    def copyFrom(self, event):
        if isinstance(event,Event):
            self._event_proxy.copyFrom(event._event_proxy)
        elif isinstance(event,ComplexEvent.ComplexEvent):
            self._event_proxy.copyFrom(event._complex_event_proxy)

    def __eq__(self, other):
        if isinstance(other,Event):
            return self._event_proxy.equals(other._event_proxy)
        else:
            return False

    def equals(self,other):
        return self == other

    def __hash__(self):
        return self._event_proxy.hashCode()

