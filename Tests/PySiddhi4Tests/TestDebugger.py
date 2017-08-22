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

import unittest
import logging

logging.basicConfig(level=logging.INFO)

import time
from time import sleep
from unittest.case import TestCase

from PySiddhi4.core.SiddhiManager import SiddhiManager
from PySiddhi4.core.debugger.SiddhiDebugger import SiddhiDebugger
from PySiddhi4.core.debugger.SiddhiDebuggerCallback import SiddhiDebuggerCallback
from PySiddhi4.core.stream.output.StreamCallback import StreamCallback
from Tests.Util.AtomicInt import AtomicInt

import threading


class TestDebugger(TestCase):
    def setUp(self):
        self.inEventCount = AtomicInt(0)
        self.debugEventCount = AtomicInt(0)

    def getCount(self, event):
        count = 0
        while event != None:
            count += 1
            event = event.getNext()

        return count

    def test_Debugger1(self):
        logging.info("Siddi Debugger Test 1: Test next traversal in a simple query")

        siddhiManager = SiddhiManager()
        cseEventStream = "@config(async = 'true') " \
                         "define stream cseEventStream (symbol string, price float, volume int);"

        query = "@info(name = 'query 1') from cseEventStream select symbol, price, volume insert into OutputStream; "

        siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(cseEventStream + query)

        _self_shaddow = self

        class StreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        siddhiAppRuntime.addCallback("OutputStream", StreamCallbackImpl())  # Causes GC Error

        inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = siddhiAppRuntime.debug()
        siddhiDebugger.acquireBreakPoint("query 1", SiddhiDebugger.QueryTerminal.IN)

        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):
                logging.info("Query: " + queryName + ":" + queryTerminal.name)
                logging.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))
                if count == 1:
                    _self_shaddow.assertEquals("query 1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 50.0, 60], event.getOutputData(),
                                                  "Incorrect debug event received at IN")

                elif count == 2:
                    _self_shaddow.assertEqual("query 1OUT", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 50.0, 60], event.getOutputData(),
                                                  "Incorrect debug event received at OUT")

                elif count == 3:
                    _self_shaddow.assertEqual("query 1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 70.0, 40], event.getOutputData(),
                                                  "Incorrect debug event received at IN")
                elif count == 4:
                    _self_shaddow.assertEquals("query 1OUT", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 70.0, 40], event.getOutputData(),
                                                  "Incorrect debug event received at OUT")

                debugger.next()

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])

        sleep(0.1)

        self.assertEquals(2, _self_shaddow.inEventCount.get(), "Invalid number of output events")
        self.assertEquals(4, _self_shaddow.debugEventCount.get(), "Invalid number of debug events")

        siddhiAppRuntime.shutdown()
        siddhiManager.shutdown()

    def test_debugger2(self):
        logging.info("Siddi Debugger Test 2: Test next traversal in a query with length batch window")

        siddhiManager = SiddhiManager()

        cseEventStream = "@config(async = 'true') " \
                         "define stream cseEventStream (symbol string, price float, volume int);"
        query = "@info(name = 'query1') " \
                "from cseEventStream#window.lengthBatch(3) select symbol, price, volume insert into OutputStream; "

        siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(cseEventStream + query)

        _self_shaddow = self

        class OutputStreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        siddhiAppRuntime.addCallback("OutputStream", OutputStreamCallbackImpl())

        inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = siddhiAppRuntime.debug()

        siddhiDebugger.acquireBreakPoint("query1", SiddhiDebugger.QueryTerminal.IN)

        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):
                logging.info("Query: " + queryName + ":" + queryTerminal.name)
                logging.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))

                if count == 1:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 50.0, 60], event.getOutputData(),
                                                  "Incorrect debug event received at IN")
                elif count == 2:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 70.0, 40], event.getOutputData(),
                                                  "Incorrect debug event received at IN")
                elif count == 3:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 60.0, 50], event.getOutputData(),
                                                  "Incorrect debug event received at IN")
                elif count == 4:
                    _self_shaddow.assertEquals("query1OUT", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertEquals(3, _self_shaddow.getCount(event), "Incorrect number of events received")

                debugger.next()

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])
        inputHandler.send(["WSO2", 60.0, 50])

        sleep(0.1)

        self.assertEquals(3, self.inEventCount.get(), "Invalid number of output events")
        self.assertEquals(6, self.debugEventCount.get(), "Invalid number of debug events")

        siddhiAppRuntime.shutdown()
        siddhiManager.shutdown()

    def test_debugger3(self):
        logging.info("Siddi Debugger Test 3: Test next traversal in a query with time batch window")

        siddhiManager = SiddhiManager()

        cseEventStream = "define stream cseEventStream (symbol string, price float, volume int);"
        query = "@info(name = 'query1')" \
                + "from cseEventStream#window.timeBatch(3 sec) " \
                + "select symbol, price, volume " + "insert into OutputStream; "

        siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(cseEventStream + query)

        _self_shaddow = self

        class OutputStreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        siddhiAppRuntime.addCallback("OutputStream", OutputStreamCallbackImpl())

        inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = siddhiAppRuntime.debug()

        siddhiDebugger.acquireBreakPoint("query1", SiddhiDebugger.QueryTerminal.IN)

        current_milli_time = lambda: int(round(time.time() * 1000))

        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):
                logging.info("Query: " + queryName + "\t" + str(current_milli_time()))
                logging.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))

                if count == 1:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 50.0, 60], event.getOutputData(),
                                                  "Incorrect debug event received at IN")
                elif count == 2:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 70.0, 40], event.getOutputData(),
                                                  "Incorrect debug event received at IN")
                elif count == 3:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 60.0, 50], event.getOutputData(),
                                                  "Incorrect debug event received at IN")

                # next call will not reach OUT since there is a window
                debugger.next()

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])
        inputHandler.send(["WSO2", 60.0, 50])

        sleep(4)

        self.assertEquals(3, self.inEventCount.get(), "Invalid number of output events")
        self.assertEquals(3, self.debugEventCount.get(), "Invalid number of debug events")

        siddhiAppRuntime.shutdown()
        siddhiManager.shutdown()

    def test_debugger4(self):
        logging.info(
            "Siddi Debugger Test 4: Test next traversal in a query with time batch window where next call delays 1 sec")

        siddhiManager = SiddhiManager()

        cseEventStream = "define stream cseEventStream (symbol string, price float, volume int);"
        query = "@info(name = 'query1')" + \
                "from cseEventStream#window.timeBatch(1 sec) " + \
                "select symbol, price, volume " + \
                "insert into OutputStream;"

        siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(cseEventStream + query)

        _self_shaddow = self

        class OutputStreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))
                _self_shaddow.assertEquals(1, len(events), "Cannot emit all three in one time")

        siddhiAppRuntime.addCallback("OutputStream", OutputStreamCallbackImpl())

        inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = siddhiAppRuntime.debug()

        siddhiDebugger.acquireBreakPoint("query1", SiddhiDebugger.QueryTerminal.IN)

        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):
                logging.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))

                if count != 1 and queryTerminal.name == SiddhiDebugger.QueryTerminal.IN.name:
                    sleep(1.1)

                # next call will not reach OUT since there is a window
                debugger.next()

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])
        inputHandler.send(["WSO2", 60.0, 50])

        sleep(1.5)

        self.assertEquals(3, self.inEventCount.get(), "Invalid number of output events")
        self.assertEquals(3, self.debugEventCount.get(), "Invalid number of debug events")

        siddhiAppRuntime.shutdown()
        siddhiManager.shutdown()

    def test_debugger5(self):
        logging.info("Siddi Debugger Test 5: Test play in a simple query")

        siddhiManager = SiddhiManager()

        cseEventStream = "@config(async = 'true') define stream cseEventStream (symbol string, price float, " + \
                         "volume int);"
        query = "@info(name = 'query1')" + \
                "from cseEventStream " + \
                "select symbol, price, volume " + \
                "insert into OutputStream; "

        siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(cseEventStream + query)

        _self_shaddow = self

        class OutputStreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        siddhiAppRuntime.addCallback("OutputStream", OutputStreamCallbackImpl())

        inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = siddhiAppRuntime.debug()

        siddhiDebugger.acquireBreakPoint("query1", SiddhiDebugger.QueryTerminal.IN)

        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):
                logging.info("Query: " + queryName + ":" + queryTerminal.name)
                logging.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))

                if count == 1:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 50.0, 60], event.getOutputData(),
                                                  "Incorrect debug event received at IN")
                elif count == 2:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 70.0, 40], event.getOutputData(),
                                                  "Incorrect debug event received at OUT")

                debugger.play()

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])

        sleep(0.1)

        self.assertEquals(2, self.inEventCount.get(), "Invalid number of output events")
        self.assertEquals(2, self.debugEventCount.get(), "Invalid number of debug events")

        siddhiAppRuntime.shutdown()
        siddhiManager.shutdown()

    def test_debugger6(self):
        logging.info("Siddi Debugger Test 6: Test play traversal in a query with length batch window")

        siddhiManager = SiddhiManager()

        cseEventStream = "@config(async = 'true') define stream cseEventStream (symbol string, price float, " + \
                         "volume int);"
        query = "@info(name = 'query1')" + \
                "from cseEventStream#window.lengthBatch(3) " + \
                "select symbol, price, volume " + \
                "insert into OutputStream; "

        siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(cseEventStream + query)

        _self_shaddow = self

        class OutputStreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        siddhiAppRuntime.addCallback("OutputStream", OutputStreamCallbackImpl())

        inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = siddhiAppRuntime.debug()

        siddhiDebugger.acquireBreakPoint("query1", SiddhiDebugger.QueryTerminal.IN)

        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):
                logging.info("Query: " + queryName + ":" + queryTerminal.name)
                logging.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))

                if count == 1:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 50.0, 60], event.getOutputData(),
                                                  "Incorrect debug event received at IN")
                elif count == 2:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 70.0, 40], event.getOutputData(),
                                                  "Incorrect debug event received at IN")
                elif count == 3:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 60.0, 50], event.getOutputData(),
                                                  "Incorrect debug event received at IN")

                debugger.play()

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])
        inputHandler.send(["WSO2", 60.0, 50])

        sleep(0.1)

        self.assertEquals(3, self.inEventCount.get(), "Invalid number of output events")
        self.assertEquals(3, self.debugEventCount.get(), "Invalid number of debug events")

        siddhiAppRuntime.shutdown()
        siddhiManager.shutdown()

    def test_debugger7(self):
        logging.info("Siddi Debugger Test 7: Test play traversal in a query with time batch window")

        siddhiManager = SiddhiManager()

        cseEventStream = "define stream cseEventStream (symbol string, price float, volume int);";
        query = "@info(name = 'query1')" + \
                "from cseEventStream#window.timeBatch(3 sec) " + \
                "select symbol, price, volume " + \
                "insert into OutputStream; "

        siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(cseEventStream + query)

        _self_shaddow = self

        class OutputStreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        siddhiAppRuntime.addCallback("OutputStream", OutputStreamCallbackImpl())

        inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = siddhiAppRuntime.debug()

        siddhiDebugger.acquireBreakPoint("query1", SiddhiDebugger.QueryTerminal.IN)

        current_milli_time = lambda: int(round(time.time() * 1000))

        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):
                logging.info("Query: " + queryName + "\t" + str(current_milli_time()))
                logging.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))

                if count == 1:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 50.0, 60], event.getOutputData(),
                                                  "Incorrect debug event received at IN")
                elif count == 2:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 70.0, 40], event.getOutputData(),
                                                  "Incorrect debug event received at IN")
                elif count == 3:
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 60.0, 50], event.getOutputData(),
                                                  "Incorrect debug event received at IN")

                debugger.play()

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])
        inputHandler.send(["WSO2", 60.0, 50])

        sleep(3.5)

        self.assertEquals(3, self.inEventCount.get(), "Invalid number of output events")
        self.assertEquals(3, self.debugEventCount.get(), "Invalid number of debug events")

        siddhiAppRuntime.shutdown()
        siddhiManager.shutdown()

    def test_debugger8(self):
        logging.info(
            "Siddi Debugger Test 8: Test play traversal in a query with time batch window where play call delays" + \
            " 1 sec")

        siddhiManager = SiddhiManager()

        cseEventStream = "define stream cseEventStream (symbol string, price float, volume int);"
        query = "@info(name = 'query1')" + \
                "from cseEventStream#window.timeBatch(1 sec) " + \
                "select symbol, price, volume " + \
                "insert into OutputStream; "

        siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(cseEventStream + query)

        _self_shaddow = self

        class OutputStreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        siddhiAppRuntime.addCallback("OutputStream", OutputStreamCallbackImpl())

        inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = siddhiAppRuntime.debug()

        siddhiDebugger.acquireBreakPoint("query1", SiddhiDebugger.QueryTerminal.IN)

        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):
                logging.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))

                _self_shaddow.assertEquals(1, _self_shaddow.getCount(event),
                                           "Only one event can be emitted from the window")

                if count != 1 and "query1IN" == queryName:
                    sleep(1)

                debugger.play()

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])
        inputHandler.send(["WSO2", 60.0, 50])

        sleep(1.5)

        self.assertEquals(3, self.inEventCount.get(), "Invalid number of output events")
        self.assertEquals(3, self.debugEventCount.get(), "Invalid number of debug events")

        siddhiAppRuntime.shutdown()
        siddhiManager.shutdown()

    def test_debugger9(self):
        logging.info("Siddi Debugger Test 9: Test state traversal in a simple query")

        siddhiManager = SiddhiManager()

        cseEventStream = "@config(async = 'true') define stream cseEventStream (symbol string, price float, " + \
                         "volume int);"
        query = "@info(name = 'query1')" + \
                "from cseEventStream#window.length(3) " + \
                "select symbol, price, sum(volume) as volume " + \
                "insert into OutputStream; "

        siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(cseEventStream + query)

        _self_shaddow = self

        class OutputStreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        siddhiAppRuntime.addCallback("OutputStream", OutputStreamCallbackImpl())

        inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = siddhiAppRuntime.debug()

        siddhiDebugger.acquireBreakPoint("query1", SiddhiDebugger.QueryTerminal.IN)

        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):
                logging.info("Query: " + queryName + ":" + queryTerminal.name)
                logging.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))

                if count == 2:
                    queryState = debugger.getQueryState(queryName)
                    logging.info(queryState)

                    streamEvent = None
                    # Order of the query state items is unpredictable
                    for (k, v) in queryState.items():
                        if k.startswith("AbstractStreamProcessor"):
                            streamEvent = v["ExpiredEventChunk"]
                            break

                    _self_shaddow.assertListEqual(streamEvent.getOutputData(), ["WSO2", 50.0, None])

                debugger.next()

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])

        sleep(1)

        self.assertEquals(2, self.inEventCount.get(), "Invalid number of output events")
        self.assertEquals(4, self.debugEventCount.get(), "Invalid number of debug events")

        siddhiAppRuntime.shutdown()
        siddhiManager.shutdown()

    def test_debugger10(self):
        logging.info("Siddi Debugger Test 10: Test next traversal in a query with two consequent streams")

        siddhiManager = SiddhiManager()

        cseEventStream = "@config(async = 'true') " + \
                         "define stream cseEventStream (symbol string, price float, volume int); " + \
                         "define stream stockEventStream (symbol string, price float, volume int); "

        query = "@info(name = 'query1')" + \
                "from cseEventStream " + \
                "select symbol, price, volume " + \
                "insert into stockEventStream; " + \
                "@info(name = 'query2')" + \
                "from stockEventStream " + \
                "select * " + \
                "insert into OutputStream;"

        siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(cseEventStream + query)

        _self_shaddow = self

        class OutputStreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        siddhiAppRuntime.addCallback("OutputStream", OutputStreamCallbackImpl())

        inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = siddhiAppRuntime.debug()

        siddhiDebugger.acquireBreakPoint("query1", SiddhiDebugger.QueryTerminal.IN)

        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):
                logging.info("Query: " + queryName + ":" + queryTerminal.name)
                logging.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))
                if 1 <= count <= 4:
                    # First four events
                    _self_shaddow.assertListEqual(["WSO2", 50.0, 60], event.getOutputData(),
                                                  "Incorrect debug event received")
                else:
                    # Next four events
                    _self_shaddow.assertListEqual(["WSO2", 70.0, 40], event.getOutputData(),
                                                  "Incorrect debug event received")

                if (count == 1 or count == 5):
                    _self_shaddow.assertEquals("query1IN", queryName + queryTerminal.name, "Incorrect break point")
                elif (count == 2 or count == 6):
                    _self_shaddow.assertEquals("query1OUT", queryName + queryTerminal.name, "Incorrect break point")
                elif (count == 3 or count == 7):
                    _self_shaddow.assertEquals("query2IN", queryName + queryTerminal.name, "Incorrect break point")
                else:
                    _self_shaddow.assertEquals("query2OUT", queryName + queryTerminal.name, "Incorrect break point")

                debugger.next()

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])

        sleep(0.1)

        self.assertEquals(2, self.inEventCount.get(), "Invalid number of output events")
        self.assertEquals(8, self.debugEventCount.get(), "Invalid number of debug events")

        siddhiAppRuntime.shutdown()
        siddhiManager.shutdown()

    def test_debugger11(self):
        logging.info("Siddi Debugger Test 11: Modify events during debug mode")

        siddhiManager = SiddhiManager()

        cseEventStream = "@config(async = 'true') " + \
                         "define stream cseEventStream (symbol string, price float, volume int); " + \
                         "define stream stockEventStream (symbol string, price float, volume int); "

        query = "@info(name = 'query1')" + \
                "from cseEventStream " + \
                "select symbol, price, volume " + \
                "insert into stockEventStream; " + \
                "@info(name = 'query2')" + \
                "from stockEventStream " + \
                "select * " + \
                "insert into OutputStream;"

        siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(cseEventStream + query)

        _self_shaddow = self

        class OutputStreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        siddhiAppRuntime.addCallback("OutputStream", OutputStreamCallbackImpl())

        inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = siddhiAppRuntime.debug()

        siddhiDebugger.acquireBreakPoint("query1", SiddhiDebugger.QueryTerminal.IN)

        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):
                logging.info("Query: " + queryName + ":" + queryTerminal.name)
                logging.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))

                if (count == 1 or count == 2):
                    # WSO2 in stream 1
                    _self_shaddow.assertListEqual(["WSO2", 50.0, 60], event.getOutputData(),
                                                  "Incorrect debug event received")
                else:
                    # IBM in stream 2
                    _self_shaddow.assertListEqual(["IBM", 50.0, 60], event.getOutputData(),
                                                  "Incorrect debug event received")

                if count == 2:
                    # Modify the event at the end of the first stream
                    # TODO Improve the logic to use assignment operator (writeBacks by assignment operator)
                    event.setOutputData("IBM", 0)

                debugger.next()

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])

        sleep(0.1)

        self.assertEquals(1, self.inEventCount.get(), "Invalid number of output events")
        self.assertEquals(4, self.debugEventCount.get(), "Invalid number of debug events")

        siddhiAppRuntime.shutdown()
        siddhiManager.shutdown()

    def test_debugger12(self):
        logging.info("Siddi Debugger Test 12: Test debugging two queries with concurrent input")

        siddhiManager = SiddhiManager()

        cseEventStream = "@config(async = 'true') " + \
                         "define stream cseEventStream (symbol string, price float, volume int); " + \
                         "define stream stockEventStream (symbol string, price float, volume int); "

        query = "@info(name = 'query1')" + \
                "from cseEventStream " + \
                "select * " + \
                "insert into OutputStream1; " + \
                "@info(name = 'query2')" + \
                "from stockEventStream " + \
                "select * " + \
                "insert into OutputStream2;"

        siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(cseEventStream + query)

        _self_shaddow = self

        class OutputStreamCallbackImpl1(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        siddhiAppRuntime.addCallback("OutputStream1", OutputStreamCallbackImpl1())

        class OutputStreamCallbackImpl2(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        siddhiAppRuntime.addCallback("OutputStream2", OutputStreamCallbackImpl2())

        cseEventStreamInputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")
        stockEventStreamInputHandler = siddhiAppRuntime.getInputHandler("stockEventStream")

        siddhiDebugger = siddhiAppRuntime.debug()

        siddhiDebugger.acquireBreakPoint("query1", SiddhiDebugger.QueryTerminal.IN)
        siddhiDebugger.acquireBreakPoint("query2", SiddhiDebugger.QueryTerminal.IN)

        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def __init__(self):
                SiddhiDebuggerCallback.__init__(self)
                self.queryOneResumed = AtomicInt(0)

            def debugEvent(self, event, queryName, queryTerminal, debugger):
                logging.info("Query: " + queryName + ":" + queryTerminal.name)
                logging.info(event)

                _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))

                if ("query1IN" == queryName):
                    sleep(1)
                    self.queryOneResumed.set(1)

                    _self_shaddow.assertListEqual(["WSO2", 50.0, 60], event.getOutputData(),
                                                  "Incorrect debug event received")
                elif "query2IN" == queryName:
                    # If query2IN is reached, query1IN must left that break point
                    _self_shaddow.assertTrue(self.queryOneResumed.get(),
                                             "Query 2 thread enterted the checkpoint before query 1 is debugged")
                    _self_shaddow.assertListEqual(["IBM", 45.0, 80], event.getOutputData(),
                                                  "Incorrect debug event received")
                debugger.next()

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        def thread1_worker():
            cseEventStreamInputHandler.send(["WSO2", 50.0, 60])

        thread1 = threading.Thread(target=thread1_worker)
        thread1.start()

        def thread2_worker():
            stockEventStreamInputHandler.send(["IBM", 45.0, 80])

        thread2 = threading.Thread(target=thread2_worker)
        thread2.start()

        sleep(2)

        self.assertEquals(2, self.inEventCount.get(), "Invalid number of output events")
        self.assertEquals(4, self.debugEventCount.get(), "Invalid number of debug events")

        siddhiAppRuntime.shutdown()
        siddhiManager.shutdown()

    def test_set_debugger_callback(self):
        logging.info("Siddi Debugger Wrapper Test 1: Set Debugger Callback")

        siddhiManager = SiddhiManager()
        cseEventStream = "@config(async = 'true') define stream cseEventStream (symbol string, price float, volume int);"

        query = "@info(name = 'query 1') from cseEventStream select symbol, price, volume insert into OutputStream; "

        siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(cseEventStream + query)

        _self_shaddow = self

        class StreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        siddhiAppRuntime.addCallback("OutputStream", StreamCallbackImpl())  # Causes GC Error

        inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = siddhiAppRuntime.debug()

        # Callback1
        class SiddhiDebuggerCallbackImpl1(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):
                logging.info("Query: " + queryName + ":" + queryTerminal.name)
                logging.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))
                if count == 1:
                    _self_shaddow.assertEquals("query 1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 50.0, 60], event.getOutputData(),
                                                  "Incorrect debug event received at IN")
                else:
                    # No more events should be received
                    _self_shaddow.fail("The callback has not been released")

                debugger.play()

        # Callback2
        class SiddhiDebuggerCallbackImpl2(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):
                logging.info("Query: " + queryName + ":" + queryTerminal.name)
                logging.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))
                if count == 2:
                    _self_shaddow.assertEquals("query 1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 70.0, 40], event.getOutputData(),
                                                  "Incorrect debug event received at IN")
                else:
                    # No more events should be received
                    _self_shaddow.fail("Invalid event count")

                debugger.play()

        siddhiDebugger.acquireBreakPoint("query 1", SiddhiDebugger.QueryTerminal.IN)

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl1())

        inputHandler.send(["WSO2", 50.0, 60])

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl2())

        inputHandler.send(["WSO2", 70.0, 40])

        self.assertEquals(2, _self_shaddow.inEventCount.get(), "Invalid number of output events")
        self.assertEquals(2, _self_shaddow.debugEventCount.get(), "Invalid number of debug events")

        siddhiAppRuntime.shutdown()
        siddhiManager.shutdown()

    def test_acquire_release_breakpoint(self):
        logging.info("Siddi Debugger Wrapper Test 2: Acquire and Release Break Point")

        siddhiManager = SiddhiManager()
        cseEventStream = "@config(async = 'true') " \
                         "define stream cseEventStream (symbol string, price float, volume int);"

        query = "@info(name = 'query 1') from cseEventStream select symbol, price, volume insert into OutputStream; "

        siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(cseEventStream + query)

        _self_shaddow = self

        class StreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        siddhiAppRuntime.addCallback("OutputStream", StreamCallbackImpl())  # Causes GC Error

        inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")

        siddhiDebugger = siddhiAppRuntime.debug()

        class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
            def debugEvent(self, event, queryName, queryTerminal, debugger):
                logging.info("Query: " + queryName + ":" + queryTerminal.name)
                logging.info(event)

                count = _self_shaddow.debugEventCount.addAndGet(_self_shaddow.getCount(event))
                if count == 1:
                    _self_shaddow.assertEquals("query 1IN", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 50.0, 60], event.getOutputData(),
                                                  "Incorrect debug event received at IN")
                elif count == 2:
                    _self_shaddow.assertEquals("query 1OUT", queryName + queryTerminal.name, "Incorrect break point")
                    _self_shaddow.assertListEqual(["WSO2", 50.0, 60], event.getOutputData(),
                                                  "Incorrect debug event received at IN")

                else:
                    # No more events should be received
                    _self_shaddow.fail("The breakpoint has not been released")

                debugger.play()

        siddhiDebugger.acquireBreakPoint("query 1", SiddhiDebugger.QueryTerminal.IN)

        siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

        inputHandler.send(["WSO2", 50.0, 60])

        siddhiDebugger.releaseBreakPoint("query 1", SiddhiDebugger.QueryTerminal.IN)

        inputHandler.send(["WSO2", 70.0, 40])

        sleep(0.1)

        self.assertEquals(2, _self_shaddow.inEventCount.get(), "Invalid number of output events")
        self.assertEquals(1, _self_shaddow.debugEventCount.get(), "Invalid number of debug events")

        siddhiAppRuntime.shutdown()
        siddhiManager.shutdown()


if __name__ == '__main__':
    unittest.main()
