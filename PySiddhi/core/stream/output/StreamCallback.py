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

from multiprocessing import RLock

import logging

from abc import ABCMeta, abstractmethod

from PySiddhi import SiddhiLoader
from PySiddhi.core.event.Event import Event

from future.utils import with_metaclass

_stream_callback_proxy = SiddhiLoader._loadType(
    "io.siddhi.pythonapi.proxy.core.stream.output.callback.stream_callback.StreamCallbackProxy")

_lock = RLock()

_created_instances = []  # Hold reference to prevent python from GC callback before java does


class StreamCallback(with_metaclass(ABCMeta, object)):
    '''
    StreamCallback is used to receive events from StreamJunction
    This class should be extended if one intends to get events from a Siddhi Stream.
    '''

    # __metaclass__ = ABCMeta

    def __init__(self):
        self._stream_callback_proxy = _stream_callback_proxy()
        stream_callback_self = self

        class ReceiveCallback(SiddhiLoader._PythonJavaClass):
            '''
            Innerclass to wrap around Java Interface
            '''
            __javainterfaces__ = [
                "io/siddhi/pythonapi/proxy/core/stream/output/callback/stream_callback/ReceiveCallbackProxy"]

            @SiddhiLoader._java_method(signature='([Lio/siddhi/core/event/Event;)V', name="receive")
            def receive(self, events):
                if events is not None:
                    events = [Event._fromEventProxy(event) for event in events]
                stream_callback_self.receive(events)

            @SiddhiLoader._java_method(signature='()V', name="gc")
            def gc(self):
                _created_instances.remove(stream_callback_self)
                logging.info("Java Reported GC Collected Stream Callback")

        self._receive_callback_ref = ReceiveCallback()  # Hold reference to prevent python
        # from GC callback before java does
        self._stream_callback_proxy.setReceiveCallback(self._receive_callback_ref)
        _created_instances.append(self)

    @abstractmethod
    def receive(self, events):
        pass
