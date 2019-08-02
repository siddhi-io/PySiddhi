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
from PySiddhi.core.debugger.SiddhiDebugger import SiddhiDebugger
from PySiddhi.core.query.output.callback.QueryCallback import QueryCallback
from PySiddhi.core.stream.input.InputHandler import InputHandler
from PySiddhi.core.stream.output.StreamCallback import StreamCallback


class SiddhiAppRuntime(object):
    '''
    Wrapper on io.core.SiddhiAppRuntime
    '''

    def __init__(self):
        '''
        Use SiddhiManager to instantiate SiddhiAppEngine
        '''
        raise NotImplementedError("Initialize SiddhiAppRuntime using Siddhi Manager")

    def __new__(cls):
        bare_instance = object.__new__(cls)
        bare_instance.siddhi_app_runtime_proxy = None
        return bare_instance

    def addCallback(self, queryName, queryCallback):
        '''
        Assign callback interface to SiddhiAppRuntime
        :param queryName:
        :param queryCallback:
        :return:
        '''
        if isinstance(queryCallback, QueryCallback):
            SiddhiLoader.siddhi_api_core_inst.addSiddhiAppRuntimeQueryCallback(self.siddhi_app_runtime_proxy, queryName,
                                                                               queryCallback._query_callback_proxy_inst)
        elif isinstance(queryCallback, StreamCallback):
            SiddhiLoader.siddhi_api_core_inst.addSiddhiAppRuntimeStreamCallback(self.siddhi_app_runtime_proxy,
                                                                                queryName,
                                                                                queryCallback._stream_callback_proxy)
        else:
            raise NotImplementedError("Unknown type of callback")

    def start(self):
        '''
        Start SiddhiAppRuntime
        :return: void
        '''
        self.siddhi_app_runtime_proxy.start()

    def shutdown(self):
        '''
        Shutdown SiddhiAppRuntime
        :return:
        '''
        self.siddhi_app_runtime_proxy.shutdown()
        del self.siddhi_app_runtime_proxy

    def getInputHandler(self, streamId):
        '''
        Retrieve input handler assigned with a stream
        :param streamId: stream id of stream
        :return: InputHandler
        '''
        input_handler_proxy = self.siddhi_app_runtime_proxy.getInputHandler(streamId)
        return InputHandler._fromInputHandlerProxy(input_handler_proxy)

    def debug(self):
        '''
        Retrieve the Siddhi Debugger used to debug the Siddhi app
        :return: SiddhiDebugger
        '''
        # Obtain debugger proxy class
        siddhi_debugger_proxy = self.siddhi_app_runtime_proxy.debug()
        return SiddhiDebugger._fromSiddhiDebuggerProxy(siddhi_debugger_proxy)

    @classmethod
    def _fromSiddhiAppRuntimeProxy(cls, siddhi_app_runtime_proxy):
        '''
        Internal Constructor to wrap around JAVA Class SiddhiAppRuntime
        :param siddhi_app_runtime_proxy:
        :return:
        '''
        instance = cls.__new__(cls)
        instance.siddhi_app_runtime_proxy = siddhi_app_runtime_proxy
        return instance

    def getName(self):
        '''
        Returns name of SiddhiAppContext
        :return: 
        '''
        return self.siddhi_app_runtime_proxy.getName()

    def persist(self):
        '''
        Persists state
        :return: 
        '''
        return self.siddhi_app_runtime_proxy.persist()

    def restoreRevision(self, revision):
        '''
        Restores revision
        :param revision: Revision
        :return: 
        '''
        self.siddhi_app_runtime_proxy.restoreRevision(revision)

    def restoreLastRevision(self):
        '''
        Restores last revision
        :return: 
        '''
        self.siddhi_app_runtime_proxy.restoreLastRevision()

    def snapshot(self):
        '''
        Obtains snapshot 
        :return: byteArray
        '''
        return self.siddhi_app_runtime_proxy.snapshot()
