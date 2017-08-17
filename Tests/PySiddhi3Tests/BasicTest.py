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
from multiprocessing import Lock
from time import sleep

from PySiddhi3.DataTypes.LongType import LongType
from PySiddhi3.core.SiddhiManager import SiddhiManager
from PySiddhi3.core.query.output.callback.QueryCallback import QueryCallback
from PySiddhi3.core.util.EventPrinter import PrintEvent

import logging

logging.basicConfig(level=logging.INFO)


class BasicTests(unittest.TestCase):
    def setUp(self):
        # Creating SiddhiManager
        self.siddhiManager = SiddhiManager()
        self.executionPlan = "define stream cseEventStream (symbol string, price float, volume long); " +\
                             "@info(name = 'query1') " + "from cseEventStream[volume < 150] " +\
                             "select symbol,price " + "insert into outputStream ;"
        # Generating runtime
        self.executionPlanRuntime = self.siddhiManager.createExecutionPlanRuntime(self.executionPlan)

    def test_insput_handler(self):
        logging.info("Test1: Test Input Handler")

        # Retrieving input handler to push events into Siddhi
        inputHandler = self.executionPlanRuntime.getInputHandler("cseEventStream")
        # Starting event processing
        self.executionPlanRuntime.start()

        # Sending events to Siddhi
        inputHandler.send(["IBM", 700.0, LongType(100)])
        inputHandler.send(["WSO2", 60.5, LongType(200)])
        inputHandler.send(["GOOG", 50, LongType(30)])
        inputHandler.send(["IBM", 76.6, LongType(400)])
        inputHandler.send(["WSO2", 45.6, LongType(50)])

    def test_execution_plan_runtime_callback(self):
        logging.info("Test2: Test Execution Plan Runtime Callback")
        # Adding callback to retrieve output events from query
        lock = Lock()

        global hitCount
        hitCount = 3

        class ConcreteQueryCallback(QueryCallback):
            def receive(self, timestamp, inEvents, outEvents):
                PrintEvent(timestamp, inEvents, outEvents)
                global hitCount
                hitCount -= 1

        self.executionPlanRuntime.addCallback("query1", ConcreteQueryCallback())

        # Retrieving input handler to push events into Siddhi
        inputHandler = self.executionPlanRuntime.getInputHandler("cseEventStream")
        # Starting event processing
        self.executionPlanRuntime.start()

        # Sending events to Siddhi
        inputHandler.send(["IBM", 700.0, LongType(100)])
        inputHandler.send(["WSO2", 60.5, LongType(200)])
        inputHandler.send(["GOOG", 50, LongType(30)])
        inputHandler.send(["IBM", 76.6, LongType(400)])
        inputHandler.send(["WSO2", 45.6, LongType(50)])

        sleep(0.5)
        self.assertEqual(hitCount, 0)

    def tearDown(self):
        # shutting down the runtime
        self.executionPlanRuntime.shutdown()

        # shutting down Siddhi
        self.siddhiManager.shutdown()


if __name__ == '__main__':
    unittest.main()
