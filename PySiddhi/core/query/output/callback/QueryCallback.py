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

import logging

from abc import ABCMeta, abstractmethod

from PySiddhi import SiddhiLoader
from PySiddhi.core.event.Event import Event

from future.utils import with_metaclass

_query_callback_proxy = SiddhiLoader._loadType(
    "io.siddhi.pythonapi.proxy.core.query.output.callback.query_callback.QueryCallbackProxy")

_created_instances = []  # Hold references to prevent python from GCing Callbacks until Java does


class QueryCallback(with_metaclass(ABCMeta, object)):
    '''
    Callback to receive events from SiddhiAppRuntime. Should be extended by child class.
    Wrapper on io.siddhi.core.query.output.callback.QueryCallback
    '''

    def __init__(self):
        self._query_callback_proxy_inst = _query_callback_proxy()
        query_callback_self = self

        class ReceiveCallback(SiddhiLoader._PythonJavaClass):
            '''
            Innerclass to wrap around Java Interface
            '''
            __javainterfaces__ = [
                "io/siddhi/pythonapi/proxy/core/query/output/callback/query_callback/ReceiveCallbackProxy"]

            @SiddhiLoader._java_method(
                signature='(J[Lio/siddhi/core/event/Event;[Lio/siddhi/core/event/Event;)V',
                name="receive")
            def receive(self, timestamp, inEvents, outEvents):
                # _lock.acquire()
                if inEvents is not None:
                    inEvents = [Event._fromEventProxy(event) for event in inEvents]
                if outEvents is not None:
                    outEvents = [Event._fromEventProxy(event) for event in outEvents]
                query_callback_self.receive(timestamp, inEvents, outEvents)
                # _lock.release()

            @SiddhiLoader._java_method(signature='()V', name="gc")
            def gc(self):
                _created_instances.remove(query_callback_self)
                logging.info("Java Reported GC Collected Query Callback")

        self._receive_callback_ref = ReceiveCallback()  # Hold reference to prevent python from GC before java does
        self._query_callback_proxy_inst.setReceiveCallback(self._receive_callback_ref)
        _created_instances.append(self)

    @abstractmethod
    def receive(self, timestamp, inEvents, outEvents):
        '''
        Receives callback from SiddhiAppRuntime
        :param timestamp: 
        :param inEvents: 
        :param outEvents: 
        :return: 
        '''
        pass
