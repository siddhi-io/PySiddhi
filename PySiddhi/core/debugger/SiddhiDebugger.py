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


import threading
from time import sleep
from PySiddhi import SiddhiLoader
from PySiddhi.DataTypes.DataWrapper import unwrapHashMap
from enum import Enum
from PySiddhi.core.event.ComplexEvent import ComplexEvent


class SiddhiDebugger(object):
    '''
    SiddhiDebugger adds checkpoints, remove checkpoints and provide traversal functions like next and play.
    The given operations are:
    - next: Debug the next checkpoint
    - play: Return to the same
    '''

    class QueryTerminal(Enum):
        '''
        SiddhiDebugger allows to add breakpoints at the beginning and the end of a query.
        '''
        IN = SiddhiLoader._loadType(
            "io.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger.QueryTerminalProxy")().IN()
        OUT = SiddhiLoader._loadType(
            "io.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger.QueryTerminalProxy")().OUT()

        @classmethod
        def _map_value(cls, queryTerminalProxy):
            qt_value = None
            if queryTerminalProxy.isValueOut():
                qt_value = SiddhiDebugger.QueryTerminal.OUT
            elif queryTerminalProxy.isValueIn():
                qt_value = SiddhiDebugger.QueryTerminal.IN
            else:
                raise TypeError("Unknown QueryTerminal Value")
            return SiddhiDebugger.QueryTerminal(qt_value)

    class _EventPoller:
        '''
        Polls Events from SiddhiDebuggerCallback
        '''

        def __init__(self):
            self.pollLock = threading.RLock()  # Lock used to access class resources from polling thread
            self.pollThread = None
            self.debugCallback = None  # Callback registered to receive events from debugger
            self.event_polling_started = False
            self.event_queue = None  # EventQueue proxy class from Java which contains event queue

        def setDebugCallbackEvent(self, debug_callback, event_queue):
            '''
            Registers a debug_callback with event_queue
            :param debug_callback: 
            :param event_queue: 
            :return: 
            '''

            if self.event_queue is not None:
                self.event_queue.interrupt()

            if debug_callback is None:
                with self.pollLock:
                    self.debugCallback = None
                    self.event_polling_started = False
                    return

            with self.pollLock:
                if not self.event_polling_started:
                    self.initEventPolling()

                self.event_queue = event_queue
                self.debugCallback = debug_callback

        def initEventPolling(self):
            '''
            Start event polling
            :return: 
            '''
            if self.event_polling_started:
                # No need init since event polling is already started
                return

            def pollLoop():
                event_polling_started = False

                with self.pollLock:
                    event_polling_started = self.event_polling_started

                while event_polling_started:
                    with self.pollLock:
                        event = self.event_queue.getQueuedEvent()
                        if event is not None:
                            if event.isDebugEvent():
                                debug_callback = self.debugCallback
                                if debug_callback is not None:
                                    complexEvent = event.getComplexEvent(0)
                                    queryName = event.getString(1)
                                    queryTerminal = event.getQueryTerminal(2)
                                    debugger = event.getSiddhiDebugger(3)

                                    complexEvent = ComplexEvent._fromComplexEventProxy(complexEvent)
                                    queryTerminal = SiddhiDebugger.QueryTerminal._map_value(queryTerminal)
                                    debugger = SiddhiDebugger._fromSiddhiDebuggerProxy(debugger)

                                    debug_callback.debugEvent(complexEvent, queryName, queryTerminal, debugger)
                                elif event.isGCEvent():
                                    self.debugCallback = None  # Release reference held with callback since it has been
                                    # destroyed from Java Side

                    sleep(0.005)  # NOTE: Removing this sleep causes changing of Debug Callback to fail
                    # TODO: Investigate why removal of above sleep causes condition in above note

                # Requirement of Pyjnius to call detach before destruction of a thread
                SiddhiLoader._detachThread()

            if self.pollThread is not None:
                self.pollThread.join()  # In case a previous eventPolling is ending, wait for it to end
            self.pollThread = threading.Thread(target=pollLoop)
            self.pollThread.setDaemon(True)
            self.event_polling_started = True
            self.pollThread.start()

    def __init__(self):
        raise NotImplementedError("Not Implemented. Use SiddhiApp.debug() to obtain SiddhiDebugger.")

    @classmethod
    def _fromSiddhiDebuggerProxy(cls, siddhi_debugger_proxy):
        '''
        Internal Constructor to wrap around JAVA Class SiddhiDebugger
        :param siddhi_app_runtime_proxy:
        :return:
        '''
        instance = cls.__new__(cls)
        instance.siddhi_debugger_proxy = siddhi_debugger_proxy
        instance.event_poller = SiddhiDebugger._EventPoller()
        instance.callback = None  # The callback currently listening for debug callbacks
        return instance

    def releaseBreakPoint(self, queryName, queryTerminal):
        '''
        Release the given breakpoint from the SiddhiDebugger.
        :param queryName: name of the Siddhi query
        :param queryTerminal: IN or OUT endpoint of the query
        :return: 
        '''
        self.siddhi_debugger_proxy.releaseBreakPoint(queryName, queryTerminal.value)

    def checkBreakPoint(self, queryName, queryTerminal, complexEvent):
        '''
        Check for active breakpoint at the given endpoint and if there is an active checkpoint, block the thread and 
        send the event for debug callback. 
        
        :param queryName: name of the Siddhi query 
        :param queryTerminal: IN or OUT endpoint of the query 
        :param complexEvent the complexEvent which is waiting at the endpoint
        :return: 
        '''
        self.siddhi_debugger_proxy.checkBreakPoint(queryName, queryTerminal.value, complexEvent._complex_event_proxy)

    def releaseAllBreakPoints(self):
        '''
        Release all the breakpoints from the Siddhi debugger. This may required to before stopping the debugger.
        :return: 
        '''
        self.siddhi_debugger_proxy.releaseAllBreakPoints()

    def getQueryState(self, queryName):
        '''
        Get all the events stored in the snapshotable entities of the given query
        :param queryName: name of the siddhi query
        :return: QueryState internal state of the query
        '''
        return unwrapHashMap(self.siddhi_debugger_proxy.getQueryState(queryName))

    def acquireBreakPoint(self, queryName, queryTerminal):
        '''
        Acquire the given breakpoint
        :param queryName: name of the Siddhi query
        :param queryTerminal: queryTerminal IN or OUT endpoint of the query
        :return: 
        '''

        self.siddhi_debugger_proxy.acquireBreakPoint(queryName, queryTerminal.value)

    def setDebuggerCallback(self, siddhi_debugger_callback):
        if siddhi_debugger_callback is not None:
            self.siddhi_debugger_proxy.setDebuggerCallback(
                siddhi_debugger_callback._siddhi_debugger_callback_proxy_inst)
            self.event_poller.setDebugCallbackEvent(siddhi_debugger_callback,
                siddhi_debugger_callback._siddhi_debugger_callback_proxy_inst.getEventQueue())
        else:
            self.event_poller.setDebugCallbackEvent(None, None)
            self.siddhi_debugger_proxy.setDebuggerCallback(None)

    def play(self):
        '''
        Release the current lock and wait for the next event arrive to the same break point.
        :return: 
        '''
        self.siddhi_debugger_proxy.play()

    def next(self):
        '''
        Release the current lock and wait for the events arrive to the next point. For this to work, the next endpoint
        is not required to be a checkpoint marked by the user.
        For example, if user adds breakpoint only for the IN of query 1, next will track the event in OUT of query 1.
        :return: 
        '''
        self.siddhi_debugger_proxy.next()
