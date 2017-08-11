#!/usr/bin/python3
from subprocess import call
import os
from PySiddhi3 import SiddhiLoader

# Download extension jars
if os.name == "nt": # Shell=True necessary for Windows
    call(["mvn", "install"],shell=True, cwd=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) ,os.path.join("Resources","Extensions3")))
else: # shell=True causes cwd to be ignored in Linux
    call(["mvn", "install"], cwd=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                          os.path.join("Resources", "Extensions3")))
# Add extensions
extensions_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/Resources/Extensions3/jars/*"
SiddhiLoader.addExtensionPath(extensions_path)

import unittest
import logging
from time import sleep


from PySiddhi3.DataTypes.LongType import LongType
from PySiddhi3.core.SiddhiManager import SiddhiManager
from PySiddhi3.core.query.output.callback.QueryCallback import QueryCallback
from PySiddhi3.core.util.EventPrinter import PrintEvent

logging.basicConfig(level=logging.INFO)


from unittest.case import TestCase

from Tests.Util.AtomicInt import AtomicInt


class TestExtensions(TestCase):
    def setUp(self):
        self.eventArrived = False
        self.count = AtomicInt(0)

    def testTimeSeriesSimpleLinearRegression(self):
        logging.info("Simple Regression TestCase")

        siddhiManager = SiddhiManager()

        siddhiManager.setExtension("timeseries:regress", "org.wso2.extension.siddhi.execution.timeseries.LinearRegressionStreamProcessor")

        inputStream = "define stream InputStream (y int, x int);"
        siddhiApp = "@info(name = 'query1') from InputStream#timeseries:regress(1, 100, 0.95, y, x) " + \
                     "select * " + \
                     "insert into OutputStream;"
        siddhiAppRuntime = siddhiManager.createExecutionPlanRuntime(inputStream + siddhiApp)
        self.betaZero = 0
        _self_shaddow = self
        class QueryCallbackImpl(QueryCallback):
            def receive(self, timestamp, inEvents, outEvents):
                PrintEvent(timestamp,inEvents,outEvents)
                _self_shaddow.count.addAndGet(len(inEvents))
                _self_shaddow.betaZero = inEvents[len(inEvents)-1].getData(3)
                
        siddhiAppRuntime.addCallback("query1", QueryCallbackImpl())
       
        inputHandler = siddhiAppRuntime.getInputHandler("InputStream")
        siddhiAppRuntime.start()

        inputHandler.send([2500.00, 17.00])
        inputHandler.send([2600.00, 18.00])
        inputHandler.send([3300.00, 31.00])
        inputHandler.send([2475.00, 12.00])
        inputHandler.send([2313.00, 8.00])
        inputHandler.send([2175.00, 26.00])
        inputHandler.send([600.00, 14.00])
        inputHandler.send([460.00, 3.00])
        inputHandler.send([240.00, 1.00])
        inputHandler.send([200.00, 10.00])
        inputHandler.send([177.00, 0.00])
        inputHandler.send([140.00, 6.00])
        inputHandler.send([117.00, 1.00])
        inputHandler.send([115.00, 0.00])
        inputHandler.send([2600.00, 19.00])
        inputHandler.send([1907.00, 13.00])
        inputHandler.send([1190.00, 3.00])
        inputHandler.send([990.00, 16.00])
        inputHandler.send([925.00, 6.00])
        inputHandler.send([365.00, 0.00])
        inputHandler.send([302.00, 10.00])
        inputHandler.send([300.00, 6.00])
        inputHandler.send([129.00, 2.00])
        inputHandler.send([111.00, 1.00])
        inputHandler.send([6100.00, 18.00])
        inputHandler.send([4125.00, 19.00])
        inputHandler.send([3213.00, 1.00])
        inputHandler.send([2319.00, 38.00])
        inputHandler.send([2000.00, 10.00])
        inputHandler.send([1600.00, 0.00])
        inputHandler.send([1394.00, 4.00])
        inputHandler.send([935.00, 4.00])
        inputHandler.send([850.00, 0.00])
        inputHandler.send([775.00, 5.00])
        inputHandler.send([760.00, 6.00])
        inputHandler.send([629.00, 1.00])
        inputHandler.send([275.00, 6.00])
        inputHandler.send([120.00, 0.00])
        inputHandler.send([2567.00, 12.00])
        inputHandler.send([2500.00, 28.00])
        inputHandler.send([2350.00, 21.00])
        inputHandler.send([2317.00, 3.00])
        inputHandler.send([2000.00, 12.00])
        inputHandler.send([715.00, 1.00])
        inputHandler.send([660.00, 9.00])
        inputHandler.send([650.00, 0.00])
        inputHandler.send([260.00, 0.00])
        inputHandler.send([250.00, 1.00])
        inputHandler.send([200.00, 13.00])
        inputHandler.send([180.00, 6.00])

        sleep(1)

        self.assertEqual(50, self.count.get(),"No of events: ")
        # Condition Loosened from equality due to floating point error
        self.assertTrue(573.1418421169493-0.001<self.betaZero<573.1418421169493+0.001,"Beta0: " + str(573.1418421169493 - self.betaZero))

        siddhiAppRuntime.shutdown()


    def testMathRandomFunctionWithSeed(self):
        logging.info("RandomFunctionExtension TestCase, with seed")

        # Creating SiddhiManager
        siddhiManager = SiddhiManager()

        siddhiManager.setExtension("math:rand",
                                   "org.wso2.extension.siddhi.execution.math.RandomFunctionExtension")

        # Creating Query
        streamDefinition = "define stream inputStream (symbol string, price long, volume long);"
        query ="@info(name = 'query1') from inputStream select symbol , math:rand(12) as randNumber " + \
            "insert into outputStream;"


        # Setting up ExecutionPlan
        executionPlanRuntime = siddhiManager.createExecutionPlanRuntime(streamDefinition + query)

        # Setting up callback
        _self_shaddow = self

        class ConcreteQueryCallback(QueryCallback):
            def receive(self, timestamp, inEvents, outEvents):
                PrintEvent(timestamp, inEvents, outEvents)
                _self_shaddow.count.addAndGet(len(inEvents))
                _self_shaddow.eventArrived = True
                if len(inEvents) == 3:
                    randNumbers = [0,0,0]
                    randNumbers[0] = inEvents[0].getData(1)
                    randNumbers[1] = inEvents[1].getData(1)
                    randNumbers[2] = inEvents[2].getData(1)
                    isDuplicatePresent = False

                    logging.info(randNumbers[0] + ", " + randNumbers[1])

                    if randNumbers[0] == randNumbers[1] or randNumbers[0] == randNumbers[2] or randNumbers[1] == randNumbers[2]:
                        isDuplicatePresent = True

                    _self_shaddow.assertEquals(False, isDuplicatePresent)



        executionPlanRuntime.addCallback("query1", ConcreteQueryCallback())

        # Retrieving input handler to push events into Siddhi
        inputHandler = executionPlanRuntime.getInputHandler("inputStream")
        # Starting event processing
        executionPlanRuntime.start()

        # Sending events to Siddhi
        inputHandler.send(["IBM", 700.0, LongType(100)])
        inputHandler.send(["WSO2", 60.5, LongType(200)])
        inputHandler.send(["XYZ", 60.5, LongType(200)])
        sleep(0.5)

        self.assertEqual(self.count.get(), 3)
        self.assertTrue(self.eventArrived)

        siddhiManager.shutdown()

    def testMathRandomFunctionWithoutSeed(self):
        logging.info("RandomFunctionExtension TestCase, without seed")

        # Creating SiddhiManager
        siddhiManager = SiddhiManager()

        # Creating Query
        streamDefinition = "define stream inputStream (symbol string, price long, volume long);"
        query ="@info(name = 'query1') from inputStream select symbol , math:rand() as randNumber " + \
            "insert into outputStream;"


        # Setting up ExecutionPlan
        executionPlanRuntime = siddhiManager.createExecutionPlanRuntime(streamDefinition + query)

        # Setting up callback
        _self_shaddow = self

        class ConcreteQueryCallback(QueryCallback):
            def receive(self, timestamp, inEvents, outEvents):
                PrintEvent(timestamp, inEvents, outEvents)
                _self_shaddow.count.addAndGet(len(inEvents))
                _self_shaddow.eventArrived = True
                if len(inEvents) == 3:
                    randNumbers = [0,0,0]
                    randNumbers[0] = inEvents[0].getData(1)
                    randNumbers[1] = inEvents[1].getData(1)
                    randNumbers[2] = inEvents[2].getData(1)
                    isDuplicatePresent = False
                    if randNumbers[0] == randNumbers[1] or randNumbers[0] == randNumbers[2] or randNumbers[1] == randNumbers[2]:
                        isDuplicatePresent = True

                    _self_shaddow.assertEquals(False, isDuplicatePresent)



        executionPlanRuntime.addCallback("query1", ConcreteQueryCallback())

        # Retrieving input handler to push events into Siddhi
        inputHandler = executionPlanRuntime.getInputHandler("inputStream")
        # Starting event processing
        executionPlanRuntime.start()

        # Sending events to Siddhi
        inputHandler.send(["IBM", 700.0, LongType(100)])
        inputHandler.send(["WSO2", 60.5, LongType(200)])
        inputHandler.send(["XYZ", 60.5, LongType(200)])
        sleep(0.1)

        self.assertEqual(self.count.get(), 3)
        self.assertTrue(self.eventArrived)

        siddhiManager.shutdown()

    def testStringRegexpFunction(self):
        logging.info("RegexpFunctionExtensionTestCase TestCase")

        # Creating SiddhiManager
        siddhiManager = SiddhiManager()

        # Creating Query
        streamDefinition = "define stream inputStream (symbol string, price long, regex string);"
        query = "@info(name = 'query1') from inputStream select symbol , " + \
                "str:regexp(symbol, regex) as beginsWithWSO2 " + \
                "insert into outputStream"


        # Setting up ExecutionPlan
        executionPlanRuntime = siddhiManager.createExecutionPlanRuntime(streamDefinition + query)

        # Setting up callback
        _self_shaddow = self

        class ConcreteQueryCallback(QueryCallback):
            def receive(self, timestamp, inEvents, outEvents):
                PrintEvent(timestamp, inEvents, outEvents)
                for inEvent in inEvents:
                    _self_shaddow.count.addAndGet(1)
                    if _self_shaddow.count.get() == 1:
                        _self_shaddow.assertEqual(False, inEvent.getData(1))

                    if _self_shaddow.count.get() == 2:
                        _self_shaddow.assertEqual(True, inEvent.getData(1))

                    if _self_shaddow.count.get() == 3:
                        _self_shaddow.assertEqual(False, inEvent.getData(1))

                _self_shaddow.eventArrived = True

        executionPlanRuntime.addCallback("query1", ConcreteQueryCallback())

        # Retrieving input handler to push events into Siddhi
        inputHandler = executionPlanRuntime.getInputHandler("inputStream")
        # Starting event processing
        executionPlanRuntime.start()

        # Sending events to Siddhi
        inputHandler.send(["hello hi hello", 700.0, "^WSO2(.*)"])
        inputHandler.send(["WSO2 abcdh", 60.5, "WSO(.*h)"])
        inputHandler.send(["aaWSO2 hi hello", 60.5, "^WSO2(.*)"])
        sleep(0.5)

        self.assertEqual(self.count.get(), 3)
        self.assertTrue(self.eventArrived)

        siddhiManager.shutdown()

    def testStringContainsFunction(self):
        logging.info("ContainsFunctionExtensionTestCase TestCase")

        # Creating SiddhiManager
        siddhiManager = SiddhiManager()

        # Creating Query
        streamDefinition = "define stream inputStream (symbol string, price long, volume long);"
        query = "@info(name = 'query1') " + \
                 "from inputStream " + \
                 "select symbol , str:contains(symbol, 'WSO2') as isContains " + \
                 "insert into outputStream;"

        # Setting up Execution Plan
        executionPlanRuntime = siddhiManager.createExecutionPlanRuntime(streamDefinition + query)

        # Setting up callback
        _self_shaddow = self
        class ConcreteQueryCallback(QueryCallback):
            def receive(self, timestamp, inEvents, outEvents):
                PrintEvent(timestamp, inEvents, outEvents)
                for inEvent in inEvents:
                    _self_shaddow.count.addAndGet(1)
                    if _self_shaddow.count.get() == 1:
                        _self_shaddow.assertEqual(False, inEvent.getData(1))

                    if _self_shaddow.count.get() == 2:
                        _self_shaddow.assertEqual(True, inEvent.getData(1))

                    if _self_shaddow.count.get() == 3:
                        _self_shaddow.assertEqual(True, inEvent.getData(1))

                _self_shaddow.eventArrived = True


        executionPlanRuntime.addCallback("query1", ConcreteQueryCallback())

        # Retrieving input handler to push events into Siddhi
        inputHandler = executionPlanRuntime.getInputHandler("inputStream")
        # Starting event processing
        executionPlanRuntime.start()

        # Sending events to Siddhi
        inputHandler.send(["IBM", 700.0, LongType(100)])
        inputHandler.send(["WSO2", 60.5, LongType(200)])
        inputHandler.send(["One of the best middleware is from WSO2.", 60.5, LongType(200)])
        sleep(0.5)

        self.assertEqual(self.count.get(),3)
        self.assertTrue(self.eventArrived)

        siddhiManager.shutdown()


