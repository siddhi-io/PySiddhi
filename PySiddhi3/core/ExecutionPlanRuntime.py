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

from PySiddhi3 import SiddhiLoader
from PySiddhi3.core.query.output.callback.QueryCallback import QueryCallback
from PySiddhi3.core.stream.input.InputHandler import InputHandler
from PySiddhi3.core.stream.output.StreamCallback import StreamCallback


class ExecutionPlanRuntime(object):
    '''
    Wrapper on org.wso2.core.ExecutionPlanRuntime
    '''

    def __init__(self, ):
        raise NotImplementedError("Initialize ExecutionPlanRuntime using Siddhi Manager")

    def __new__(cls):
        bare_instance = object.__new__(cls)
        bare_instance.execution_plan_runtime_proxy = None
        return bare_instance

    def addCallback(self, queryName, queryCallback):
        '''
        Assign callback interface to ExecutionPlanRuntime
        :param queryName:
        :param queryCallback:
        :return:
        '''
        if isinstance(queryCallback, QueryCallback):
            SiddhiLoader.siddhi_api_core_inst.addExecutionPlanRuntimeQueryCallback(self.execution_plan_runtime_proxy,
                                                                                   queryName,
                                                                                   queryCallback._query_callback_proxy_inst)
        elif isinstance(queryCallback, StreamCallback):
            SiddhiLoader.siddhi_api_core_inst.addExecutionPlanRuntimeStreamCallback(self.execution_plan_runtime_proxy,
                                                                                    queryName,
                                                                                    queryCallback._stream_callback_proxy)
        else:
            raise NotImplementedError("Unknown type of callback")

    def start(self):
        '''
        Start ExecutionPlanRuntime
        :return: void
        '''
        self.execution_plan_runtime_proxy.start()

    def shutdown(self):
        '''
        Shutdown ExecutionPlanRuntime
        :return:
        '''
        self.execution_plan_runtime_proxy.shutdown()
        del self.execution_plan_runtime_proxy

    def getInputHandler(self, streamId):
        '''
        Retrieve input handler assigned with a stream
        :param streamId: stream id of stream
        :return: InputHandler
        '''
        input_handler_proxy = self.execution_plan_runtime_proxy.getInputHandler(streamId)
        return InputHandler._fromInputHandlerProxy(input_handler_proxy)

    @classmethod
    def _fromExecutionPlanRuntimeProxy(cls, execution_plan_runtime_proxy):
        '''
        Internal Constructor to wrap around JAVA Class ExecutionPlanRuntime
        :param execution_plan_runtime_proxy:
        :return:
        '''
        instance = cls.__new__(cls)
        instance.execution_plan_runtime_proxy = execution_plan_runtime_proxy
        return instance

    def getName(self):
        '''
        Returns name of ExecutionPlanContext
        :return: 
        '''
        return self.execution_plan_runtime_proxy.getName()

    def persist(self):
        '''
        Persists state
        :return: 
        '''
        return self.execution_plan_runtime_proxy.persist()

    def restoreRevision(self, revision):
        '''
        Restores revision
        :param revision: Revision as a String
        :return: 
        '''
        self.execution_plan_runtime_proxy.restoreRevision(revision)

    def restoreLastRevision(self):
        '''
        Restores last revision
        :return: 
        '''
        self.execution_plan_runtime_proxy.restoreLastRevision()

    def snapshot(self):
        '''
        Obtains snapshot 
        :return: byteArray
        '''
        return self.execution_plan_runtime_proxy.snapshot()

    def restore(self, snapshot):
        '''
        Restores snapshot
        :param snapshot: byteArray
        :return: 
        '''
        self.execution_plan_runtime_proxy.restore(snapshot)
