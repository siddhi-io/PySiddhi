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


from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass
from PySiddhi import SiddhiLoader

_siddhi_debugger_callback_proxy = SiddhiLoader._loadType(
    "io.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger_callback.SiddhiDebuggerCallbackProxy")


class SiddhiDebuggerCallback(with_metaclass(ABCMeta, object)):
    '''
    Callback to get notification about the events passing through the break points.
    Should be extended by subclass.
    '''

    def __init__(self):
        _siddhi_debugger_callback_self = self
        self._siddhi_debugger_callback_proxy_inst = _siddhi_debugger_callback_proxy()

    @abstractmethod
    def debugEvent(self, complexEvent, queryName, queryTerminal, debugger):
        '''
        Receive the events passing through the registered breakpoints.
        
        :param complexEvent:    ComplexEvent waiting at the breakpoint
        :param queryName:       Name of the query where the current breakpoint is
        :param queryTerminal:   IN or OUT terminal of the query
        :param debugger:        SiddhiDebugger to have control over the debug flow within the event caller
        :return: 
        '''
        pass
