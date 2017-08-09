from multiprocessing import RLock

import logging
from abc import ABCMeta, abstractmethod

from PySiddhi3 import SiddhiLoader
from PySiddhi3.core.event.Event import Event

from future.utils import with_metaclass

_stream_callback_proxy = SiddhiLoader._loadType("org.wso2.siddhi.pythonapi.proxy.core.stream.output.callback.stream_callback.StreamCallbackProxy")

_lock = RLock()

_created_instances = [] #Hold reference to prevent python from GC callback before java does

class StreamCallback(with_metaclass(ABCMeta,object)):
    '''
    StreamCallback is used to receive events from StreamJunction
    This class should be extended if one intends to get events from a Siddhi Stream.
    '''
    #__metaclass__ = ABCMeta

    def __init__(self):
        self._stream_callback_proxy = _stream_callback_proxy()
        stream_callback_self = self
        class ReceiveCallback(SiddhiLoader._PythonJavaClass):
            '''
            Innerclass to wrap around Java Interface
            '''
            __javainterfaces__ = ["org/wso2/siddhi/pythonapi/proxy/core/stream/output/callback/stream_callback/ReceiveCallbackProxy"]

            @SiddhiLoader._java_method(signature='([Lorg/wso2/siddhi/core/event/Event;)V', name="receive")
            def receive(self, events):
                #_lock.acquire()
                if events is not None:
                    events = [Event._fromEventProxy(event) for event in events]
                stream_callback_self.receive(events)
                #_lock.release()

            @SiddhiLoader._java_method(signature='()V', name="gc")
            def gc(self):
                _created_instances.remove(stream_callback_self)
                logging.info("Java Reported GC Collected Stream Callback")

        self._receive_callback_ref = ReceiveCallback() #Hold reference to prevent python from GC callback before java does
        self._stream_callback_proxy.setReceiveCallback(self._receive_callback_ref)
        _created_instances.append(self)
    @abstractmethod
    def receive(self, events):
        pass

