import unittest

import logging
import os
from time import sleep

from PySiddhi4.das.DASClient import DASClient
from PySiddhi4.das.EventSimulator.AttributeConfiguration import AttributeConfiguration
from PySiddhi4.das.EventSimulator.FeedSimulationConfiguration import FeedSimulationConfiguration
from PySiddhi4.das.EventSimulator.SimulationSource import SimulationSource
from PySiddhi4.das.EventSimulator.SingleSimulationConfiguration import SingleSimulationConfiguration

logging.basicConfig(level=logging.INFO)

resources_path = os.path.join(os.path.dirname(__file__), "Resources/")

class EventSimulatorTests(unittest.TestCase):
    def setUp(self):
        self.hostUrl = "http://localhost:9090"
        #self.simulationUrl = self.hostUrl + "/simulation"
        logging.info("Prior to launching tests, make sure DAS 4 is running at " + self.hostUrl)

    def tearDown(self):
        sleep(5) # Sleep to provide sufficient time for DAS 4.0 to update status

    def testSingleSimulation(self):
        logging.info("Test: Simulating a Single Event")

        dasPythonClient = DASClient(self.hostUrl)
        eventSimulatorClient = dasPythonClient.getEventSimulatorClient()

        singleSimulationConfiguration = SingleSimulationConfiguration("TestSiddhiApp","FooStream",[None, 9, 45])

        self.assertTrue(eventSimulatorClient.simulateSingleEvent(singleSimulationConfiguration))
        logging.info("Successfully Simulated Single Event")

    def testCSVUploadAndDelete(self):
        logging.info("Test: Uploading and Deleting a CSV.")

        dasPythonClient = DASClient(self.hostUrl)
        eventSimulatorClient = dasPythonClient.getEventSimulatorClient()

        self.assertTrue(eventSimulatorClient.uploadCSV("sample.csv",path=resources_path+"sample.csv"))
        logging.info("Successfully Uploaded CSV")

        sleep(5)

        self.assertTrue(eventSimulatorClient.deleteCSV("sample.csv"))
        logging.info("Successfully Deleted CSV")


    def testCSVUpdate(self):
        logging.info("Test: Uploading, Updating and Deleting a CSV.")

        dasPythonClient = DASClient(self.hostUrl)
        eventSimulatorClient = dasPythonClient.getEventSimulatorClient()

        self.assertTrue(eventSimulatorClient.uploadCSV("sample.csv",path=resources_path+"sample.csv"))
        logging.info("Successfully Uploaded CSV")

        sleep(5)

        self.assertTrue(eventSimulatorClient.updateCSV("sample.csv","sample2.csv", path=resources_path + "sample.csv"))
        logging.info("Successfully Uploaded CSV")

        sleep(5)

        self.assertTrue(eventSimulatorClient.deleteCSV("sample2.csv"))
        logging.info("Successfully Deleted CSV")


    def testSaveDeleteSimulationFeedConfiguration(self):
        logging.info("Test1: Saving and Deleting simulation feed configuration")

        dasPythonClient = DASClient(self.hostUrl)
        eventSimulatorClient = dasPythonClient.getEventSimulatorClient()

        svr = FeedSimulationConfiguration("simulationPrimitive")
        svr.properties.timestampStartTime = 1488615136958
        svr.properties.timestampEndTime = None
        svr.properties.noOfEvents = 8
        svr.properties.timeInterval = 1000

        sm1 = SimulationSource(simulationType=SimulationSource.Type.RANDOM_DATA_SIMULATION, streamName="FooStream", siddhiAppName="TestSiddhiApp", timestampInterval=5)

        sm1.attributeConfiguration.append(AttributeConfiguration(AttributeConfiguration.Type.PRIMITIVE_BASED, length=10))
        sm1.attributeConfiguration.append(AttributeConfiguration(AttributeConfiguration.Type.PRIMITIVE_BASED, min=35000, max=30000, precision=2))
        sm1.attributeConfiguration.append(AttributeConfiguration(AttributeConfiguration.Type.PRIMITIVE_BASED, min=150, max=300))

        svr.sources.append(sm1)

        self.assertTrue(eventSimulatorClient.saveSimulationFeedConfiguration(svr))
        logging.info("Successfully Saved Simulation Feed Configuration")
        self.assertTrue(eventSimulatorClient.deleteSimulationFeedConfiguration("simulationPrimitive"))
        logging.info("Successfully Deleted Simulation Feed Configuration")

    def testEditSimulationFeedConfiguration(self):
        logging.info("Test1: Saving, Editing and Deleting simulation feed configuration")

        dasPythonClient = DASClient(self.hostUrl)
        eventSimulatorClient = dasPythonClient.getEventSimulatorClient()

        svr = FeedSimulationConfiguration("simulationPrimitive")
        svr.properties.timestampStartTime = 1488615136958
        svr.properties.timestampEndTime = None
        svr.properties.noOfEvents = 8
        svr.properties.timeInterval = 1000

        sm1 = SimulationSource(simulationType=SimulationSource.Type.RANDOM_DATA_SIMULATION, streamName="FooStream", siddhiAppName="TestSiddhiApp", timestampInterval=5)

        sm1.attributeConfiguration.append(AttributeConfiguration(AttributeConfiguration.Type.PRIMITIVE_BASED, length=10))
        sm1.attributeConfiguration.append(AttributeConfiguration(AttributeConfiguration.Type.PRIMITIVE_BASED, min=35000, max=30000, precision=2))
        sm1.attributeConfiguration.append(AttributeConfiguration(AttributeConfiguration.Type.PRIMITIVE_BASED, min=150, max=300))

        svr.sources.append(sm1)

        self.assertTrue(eventSimulatorClient.saveSimulationFeedConfiguration(svr))
        logging.info("Successfully Saved Simulation Feed Configuration")
        sleep(5)

        svr.properties.simulationName = "simulationNewName"
        self.assertTrue(eventSimulatorClient.editSimulationFeedConfiguration("simulationPrimitive",svr))
        logging.info("Successfully Editted Simulation Feed Configuration")
        sleep(5)

        self.assertTrue(eventSimulatorClient.deleteSimulationFeedConfiguration("simulationNewName"))
        logging.info("Successfully Deleted Simulation Feed Configuration")


    def testRetrieveSimulationFeedConfiguration(self):
        logging.info("Test1: Saving, Retrieving and Deleting simulation feed configuration")

        dasPythonClient = DASClient(self.hostUrl)
        eventSimulatorClient = dasPythonClient.getEventSimulatorClient()

        svr = FeedSimulationConfiguration("simulationPrimitive")
        svr.properties.timestampStartTime = 1488615136958
        svr.properties.timestampEndTime = None
        svr.properties.noOfEvents = 8
        svr.properties.timeInterval = 1000

        sm1 = SimulationSource(simulationType=SimulationSource.Type.RANDOM_DATA_SIMULATION, streamName="FooStream", siddhiAppName="TestSiddhiApp", timestampInterval=5)

        sm1.attributeConfiguration.append(AttributeConfiguration(AttributeConfiguration.Type.PRIMITIVE_BASED, length=10))
        sm1.attributeConfiguration.append(AttributeConfiguration(AttributeConfiguration.Type.PRIMITIVE_BASED, min=35000, max=30000, precision=2))
        sm1.attributeConfiguration.append(AttributeConfiguration(AttributeConfiguration.Type.PRIMITIVE_BASED, min=150, max=300))

        svr.sources.append(sm1)

        self.assertTrue(eventSimulatorClient.saveSimulationFeedConfiguration(svr), "Unable to Save "
                                                                                   "SimulationConfiguration")

        sleep(5)
        retrieveObject = eventSimulatorClient.retrieveSimulationFeedConfiguration("simulationPrimitive")
        self.assertTrue(retrieveObject == svr, "Retrieved SimulationConfigurations does not match")

        sleep(5)
        self.assertTrue(eventSimulatorClient.deleteSimulationFeedConfiguration("simulationPrimitive"),"Unable to delete"
                                                                                            "SimulationConfiguration")


    def testRandomSimulationCustomList(self):
        logging.info("Test: Random Simulation using Custom List")

        dasPythonClient = DASClient(self.hostUrl)
        eventSimulatorClient = dasPythonClient.getEventSimulatorClient()

        svr = FeedSimulationConfiguration("sim")
        svr.properties.timestampStartTime = 1488615136958
        svr.properties.timestampEndTime = 1488615136998
        svr.properties.noOfEvents = 5
        svr.properties.timeInterval = 1000

        s1 = SimulationSource(simulationType=SimulationSource.Type.RANDOM_DATA_SIMULATION)
        s1.streamName = "FooStream"
        s1.siddhiAppName = "TestSiddhiApp"
        s1.timestampInterval = 5
        svr.sources.append(s1)

        s1.attributeConfiguration.append(
            AttributeConfiguration(type=AttributeConfiguration.Type.CUSTOM_DATA_BASED,list=["WSO2,AAA","DDD","IBM"]))
        s1.attributeConfiguration.append(
            AttributeConfiguration(type=AttributeConfiguration.Type.CUSTOM_DATA_BASED, list=[1.0,2.0,3.0]))
        s1.attributeConfiguration.append(
            AttributeConfiguration(type=AttributeConfiguration.Type.CUSTOM_DATA_BASED, list=[10, 20, 30]))

        self.assertTrue(eventSimulatorClient.saveSimulationFeedConfiguration(svr))
        logging.info("Successfully Saved Simulation Feed Configuration")

        sleep(5)

        self.assertTrue(eventSimulatorClient.deleteSimulationFeedConfiguration(svr.properties.simulationName))
        logging.info("Successfully Deleted Simulation Feed Configuration")

    def testCSVSimulationSingleSource(self):
        logging.info("Test: CSV Simulation - One Source")

        dasPythonClient = DASClient(self.hostUrl)
        eventSimulatorClient = dasPythonClient.getEventSimulatorClient()

        svr = FeedSimulationConfiguration("simulation1")
        svr.properties.timestampStartTime = None
        svr.properties.timeInterval = 8000

        s1 = SimulationSource(simulationType=SimulationSource.Type.CSV_SIMULATION)
        s1.streamName = "FooStream"
        s1.siddhiAppName = "TestSiddhiApp"
        s1.fileName = "sample.csv"
        s1.timestampInterval = 1000
        s1.isOrdered = True
        s1.delimiter = ","
        svr.sources.append(s1)

        self.assertTrue(eventSimulatorClient.uploadCSV("sample.csv", path=resources_path + "sample.csv"))
        logging.info("Successfully Uploaded CSV")

        sleep(5)

        self.assertTrue(eventSimulatorClient.saveSimulationFeedConfiguration(svr))
        logging.info("Successfully Saved Simulation Feed Configuration")

        sleep(5)

        self.assertTrue(eventSimulatorClient.deleteSimulationFeedConfiguration(svr.properties.simulationName))
        logging.info("Successfully Deleted Simulation Feed Configuration")

        self.assertTrue(eventSimulatorClient.deleteCSV("sample.csv"))
        logging.info("Successfully Deleted CSV")


    def testCSVSimulationTwoSource(self):
        logging.info("Test: CSV Simulation - Two Source")

        dasPythonClient = DASClient(self.hostUrl)
        eventSimulatorClient = dasPythonClient.getEventSimulatorClient()

        svr = FeedSimulationConfiguration("simCSV2")
        svr.properties.timestampStartTime = 1488615136957
        svr.properties.timestampEndTime = 1488615136973
        svr.properties.noOfEvents = 7
        svr.properties.timeInterval = 1000

        s1 = SimulationSource(simulationType=SimulationSource.Type.CSV_SIMULATION)
        s1.streamName = "FooStream"
        s1.siddhiAppName = "TestSiddhiApp"
        s1.fileName = "sample.csv"
        s1.timestampAttribute=0
        s1.isOrdered = True
        s1.delimiter = ","
        svr.sources.append(s1)

        s2 = SimulationSource(simulationType=SimulationSource.Type.CSV_SIMULATION)
        s2.streamName = "FooStream"
        s2.siddhiAppName = "TestSiddhiApp"
        s2.fileName = "sample.csv"
        s2.timestampAttribute = 0
        s2.isOrdered = True
        s2.delimiter = ","
        svr.sources.append(s2)

        self.assertTrue(eventSimulatorClient.uploadCSV("sample.csv", path=resources_path + "sample.csv"))
        logging.info("Successfully Uploaded CSV")

        sleep(5)

        self.assertTrue(eventSimulatorClient.saveSimulationFeedConfiguration(svr))
        logging.info("Successfully Saved Simulation Feed Configuration")

        sleep(5)

        self.assertTrue(eventSimulatorClient.deleteSimulationFeedConfiguration(svr.properties.simulationName))
        logging.info("Successfully Deleted Simulation Feed Configuration")

        self.assertTrue(eventSimulatorClient.deleteCSV("sample.csv"))
        logging.info("Successfully Deleted CSV")



    def testDBSimulationOneSource(self):
        logging.info("Test: DB Simulation - One Source")

        target = {
          "properties": {
            "simulationName": "simDb",
            "timestampStartTime": "1488615136958",
            "timestampEndTime": None,
            "noOfEvents" : None,
            "timeInterval": "1000"
          },
          "sources": [
            {
              "simulationType": "DATABASE_SIMULATION",
              "streamName": "FooStream",
              "siddhiAppName": "TestSiddhiApp",
              "dataSourceLocation": "jdbc:mysql:\/\/localhost:3306\/DatabaseFeedSimulation",
              "driver" : "com.mysql.jdbc.Driver",
              "username": "root",
              "password": "root",
              "tableName": "foostream3",
              "timestampInterval": "1000",
              "columnNamesList": None
            }
          ]
        }

        dasPythonClient = DASClient(self.hostUrl)
        eventSimulatorClient = dasPythonClient.getEventSimulatorClient()

        svr = FeedSimulationConfiguration("simDb")
        svr.properties.timestampStartTime = 1488615136958
        svr.properties.timestampEndTime = None
        svr.properties.noOfEvents = None
        svr.properties.timeInterval = 1000

        s1 = SimulationSource(simulationType=SimulationSource.Type.DATABASE_SIMULATION)
        s1.streamName = "FooStream"
        s1.siddhiAppName = "TestSiddhiApp"
        s1.dataSourceLocation = "jdbc:mysql:\/\/localhost:3306\/DatabaseFeedSimulation"
        s1.driver="com.mysql.jdbc.Driver"
        s1.username="root"
        s1.password="root"
        s1.tableName="foostream3"
        s1.timestampInterval=1000
        s1.columnNamesList=None
        svr.sources.append(s1)

        match = svr.toJSONObject()

        self.assertDictEqual(target,match)

        self.assertTrue(eventSimulatorClient.saveSimulationFeedConfiguration(svr))
        logging.info("Successfully Saved Simulation Feed Configuration")

        sleep(5)

        self.assertTrue(eventSimulatorClient.deleteSimulationFeedConfiguration(svr.properties.simulationName))
        logging.info("Successfully Deleted Simulation Feed Configuration")


    def testDBSimulationTwoSource(self):
        logging.info("Test: DB Simulation - Two Sources")

        dasPythonClient = DASClient(self.hostUrl)
        eventSimulatorClient = dasPythonClient.getEventSimulatorClient()

        svr = FeedSimulationConfiguration("simDb")
        svr.properties.timestampStartTime = 1488615136958
        svr.properties.timestampEndTime = None
        svr.properties.noOfEvents = None
        svr.properties.timeInterval = 1000

        s1 = SimulationSource(simulationType=SimulationSource.Type.DATABASE_SIMULATION)
        s1.streamName = "FooStream"
        s1.siddhiAppName = "TestSiddhiApp"
        s1.dataSourceLocation = "jdbc:mysql:\/\/localhost:3306\/DatabaseFeedSimulation"
        s1.driver = "com.mysql.jdbc.Driver"
        s1.username = "root"
        s1.password = "root"
        s1.tableName = "foostream3"
        s1.timestampInterval = 1000
        s1.columnNamesList = None
        svr.sources.append(s1)


        self.assertTrue(eventSimulatorClient.saveSimulationFeedConfiguration(svr))
        logging.info("Successfully Saved Simulation Feed Configuration")

        sleep(5)

        target = {
                  "properties": {
                    "simulationName": "simDb",
                    "timestampStartTime": "1488615136958",
                    "timestampEndTime": "1488615136961",
                    "timeInterval": "1000"
                  },
                  "sources": [
                    {
                      "simulationType": "DATABASE_SIMULATION",
                      "streamName": "FooStream",
                      "siddhiAppName": "TestSiddhiApp",
                      "dataSourceLocation": "jdbc:mysql:\/\/localhost:3306\/DatabaseFeedSimulation",
                      "driver" : "com.mysql.jdbc.Driver",
                      "username": "root",
                      "password": "root",
                      "tableName": "foostream4",
                      "timestampAttribute": "timestamp",
                      "columnNamesList": "symbol,price,volume"
                    },
                    {
                      "simulationType": "DATABASE_SIMULATION",
                      "streamName": "FooStream",
                      "siddhiAppName": "TestSiddhiApp",
                      "dataSourceLocation": "jdbc:mysql:\/\/localhost:3306\/Simulation",
                      "driver" : "com.mysql.jdbc.Driver",
                      "username": "root",
                      "password": "root",
                      "tableName": "foostream",
                      "timestampAttribute": "timestamp",
                      "columnNamesList": "name,price,volume"
                    }
                  ]
                }


        svr = FeedSimulationConfiguration("simDb")
        svr.properties.timestampStartTime = 1488615136958
        svr.properties.timestampEndTime = 1488615136961
        svr.properties.timeInterval = 1000

        s1 = SimulationSource(simulationType=SimulationSource.Type.DATABASE_SIMULATION)
        s1.streamName = "FooStream"
        s1.siddhiAppName = "TestSiddhiApp"
        s1.dataSourceLocation = "jdbc:mysql:\/\/localhost:3306\/DatabaseFeedSimulation"
        s1.driver="com.mysql.jdbc.Driver"
        s1.username="root"
        s1.password="root"
        s1.tableName="foostream4"
        s1.timestampAttribute="timestamp"
        s1.columnNamesList="symbol,price,volume"
        svr.sources.append(s1)

        s2 = SimulationSource(simulationType=SimulationSource.Type.DATABASE_SIMULATION)
        s2.streamName = "FooStream"
        s2.siddhiAppName = "TestSiddhiApp"
        s2.dataSourceLocation = "jdbc:mysql:\/\/localhost:3306\/Simulation"
        s2.driver = "com.mysql.jdbc.Driver"
        s2.username = "root"
        s2.password = "root"
        s2.tableName = "foostream"
        s2.timestampAttribute = "timestamp"
        s2.columnNamesList = "name,price,volume"
        svr.sources.append(s2)

        match = svr.toJSONObject()

        self.assertDictEqual(target,match)

        self.assertTrue(eventSimulatorClient.runSimulationFeedConfiguration(svr))
        logging.info("Successfully Started Simulation Feed Configuration")

        sleep(5)

        self.assertTrue(eventSimulatorClient.deleteSimulationFeedConfiguration(svr.properties.simulationName))
        logging.info("Successfully Deleted Simulation Feed Configuration")


    def testDBSimulationOneSourceWOColumnNames(self):
        logging.info("Test: DB Simulation - One Source w\o column names")

        target={
          "properties": {
            "simulationName": "simDbNoColumnsList",
            "timestampStartTime": "1488615136958",
            "timestampEndTime": "1488615136961",
            "timeInterval": "1000"
          },
          "sources": [
            {
              "simulationType": "DATABASE_SIMULATION",
              "streamName": "FooStream",
              "siddhiAppName": "TestSiddhiApp",
              "dataSourceLocation": "jdbc:mysql:\/\/localhost:3306\/DatabaseFeedSimulation",
              "driver" : "com.mysql.jdbc.Driver",
              "username": "root",
              "password": "root",
              "tableName": "foostream3",
              "timestampAttribute": "timestamp",
              "columnNamesList": None
            }
          ]
        }

        dasPythonClient = DASClient(self.hostUrl)
        eventSimulatorClient = dasPythonClient.getEventSimulatorClient()

        svr = FeedSimulationConfiguration("simDbNoColumnsList")
        svr.properties.timestampStartTime = 1488615136958
        svr.properties.timestampEndTime = 1488615136961
        svr.properties.timeInterval = 1000

        s1 = SimulationSource(simulationType=SimulationSource.Type.DATABASE_SIMULATION)
        s1.streamName = "FooStream"
        s1.siddhiAppName = "TestSiddhiApp"
        s1.dataSourceLocation = "jdbc:mysql:\/\/localhost:3306\/DatabaseFeedSimulation"
        s1.driver="com.mysql.jdbc.Driver"
        s1.username="root"
        s1.password="root"
        s1.tableName="foostream3"
        s1.timestampAttribute="timestamp"
        s1.columnNamesList=None
        svr.sources.append(s1)

        match = svr.toJSONObject()

        self.assertDictEqual(target,match)

        self.assertTrue(eventSimulatorClient.saveSimulationFeedConfiguration(svr))
        logging.info("Successfully Saved Simulation Feed Configuration")

        sleep(5)

        self.assertTrue(eventSimulatorClient.runSimulationFeedConfiguration(svr))
        logging.info("Successfully Started Simulation Feed Configuration")

        sleep(5)

        self.assertTrue(eventSimulatorClient.deleteSimulationFeedConfiguration(svr.properties.simulationName))
        logging.info("Successfully Deleted Simulation Feed Configuration")


    def testPrimitiveRandomSimulation(self):
        logging.info("Test: Random Simulation - Primitive")

        target = {
          "properties": {
            "simulationName": "simulationPrimitive",
            "timestampStartTime": "1488615136958",
            "timestampEndTime": None,
            "noOfEvents" : "8",
            "timeInterval": "1000"
          },
          "sources": [
           {
          "simulationType": "RANDOM_DATA_SIMULATION",
          "streamName": "FooStream",
          "siddhiAppName": "TestSiddhiApp",
          "timestampInterval": "5",
          "attributeConfiguration": [
            {
              "type": "PRIMITIVE_BASED",
              "length": "10"
            },
            {
              "type": "PRIMITIVE_BASED",
              "min": "35000",
              "max": "30000",
              "precision": "2"
            },
            {
              "type": "PRIMITIVE_BASED",
              "min": "150",
              "max": "300"
            }
          ]
        }
          ]
        }

        dasPythonClient = DASClient(self.hostUrl)
        eventSimulatorClient = dasPythonClient.getEventSimulatorClient()

        svr = FeedSimulationConfiguration("simulationPrimitive")
        svr.properties.timestampStartTime = 1488615136958
        svr.properties.timestampEndTime = None
        svr.properties.noOfEvents=8
        svr.properties.timeInterval = 1000

        s1 = SimulationSource(simulationType=SimulationSource.Type.RANDOM_DATA_SIMULATION, attributeConfiguration=list())
        s1.streamName = "FooStream"
        s1.siddhiAppName = "TestSiddhiApp"
        s1.timestampInterval = 5
        svr.sources.append(s1)

        s1.attributeConfiguration.append(
            AttributeConfiguration(type=AttributeConfiguration.Type.PRIMITIVE_BASED,length=10))
        s1.attributeConfiguration.append(
            AttributeConfiguration(type=AttributeConfiguration.Type.PRIMITIVE_BASED, min=35000, max=30000,precision=2))
        s1.attributeConfiguration.append(
            AttributeConfiguration(type=AttributeConfiguration.Type.PRIMITIVE_BASED, min=150, max=300)
        )

        match = svr.toJSONObject()

        self.assertDictEqual(target, match)

        self.assertTrue(eventSimulatorClient.saveSimulationFeedConfiguration(svr))
        logging.info("Successfully Saved Simulation Feed Configuration")

        sleep(5)

        self.assertTrue(eventSimulatorClient.runSimulationFeedConfiguration(svr))
        logging.info("Successfully Started Simulation Feed Configuration")

        sleep(5)

        self.assertTrue(eventSimulatorClient.deleteSimulationFeedConfiguration(svr.properties.simulationName))
        logging.info("Successfully Deleted Simulation Feed Configuration")



    def testRandomSimulationRegexAndPrimitive(self):
        logging.info("Test: Random Simulation - Regex and Primitive")

        target = {
          "properties": {
            "simulationName": "simRndm",
            "timestampStartTime": "1488615136958",
            "timestampEndTime": "1488615136998",
            "noOfEvents" : None,
            "timeInterval": "1000"
          },
          "sources": [
            {
              "simulationType": "RANDOM_DATA_SIMULATION",
              "streamName": "FooStream",
              "siddhiAppName": "TestSiddhiApp",
              "timestampInterval": "5",
              "attributeConfiguration": [
                {
                  "type": "REGEX_BASED",
                  "pattern": "[a-zA-Z]*"
                },
                {
                  "type": "REGEX_BASED",
                  "pattern": "[0-9]*"
                },
                {
                  "type": "PRIMITIVE_BASED",
                  "primitiveType": "LONG",
                  "min": "1500000",
                  "max": "30000000"
                }
              ]
            }
          ]
        }

        dasPythonClient = DASClient(self.hostUrl)
        eventSimulatorClient = dasPythonClient.getEventSimulatorClient()

        svr = FeedSimulationConfiguration("simRndm")
        svr.properties.timestampStartTime = 1488615136958
        svr.properties.timestampEndTime = 1488615136998
        svr.properties.noOfEvents=None
        svr.properties.timeInterval = 1000

        s1 = SimulationSource(simulationType=SimulationSource.Type.RANDOM_DATA_SIMULATION)
        s1.streamName = "FooStream"
        s1.siddhiAppName = "TestSiddhiApp"
        s1.timestampInterval = 5
        svr.sources.append(s1)

        s1.attributeConfiguration.append(
            AttributeConfiguration(type=AttributeConfiguration.Type.REGEX_BASED,pattern="[a-zA-Z]*"))
        s1.attributeConfiguration.append(
            AttributeConfiguration(type=AttributeConfiguration.Type.REGEX_BASED, pattern="[0-9]*"))
        s1.attributeConfiguration.append(
            AttributeConfiguration(type=AttributeConfiguration.Type.PRIMITIVE_BASED, min=1500000, max=30000000, primitiveType=AttributeConfiguration.PrimitiveType.LONG)
        )

        match = svr.toJSONObject()

        self.assertDictEqual(target, match)

        self.assertTrue(eventSimulatorClient.saveSimulationFeedConfiguration(svr))
        logging.info("Successfully Saved Simulation Feed Configuration")

        sleep(5)

        self.assertTrue(eventSimulatorClient.runSimulationFeedConfiguration(svr))
        logging.info("Successfully Started Simulation Feed Configuration")

        sleep(5)

        self.assertTrue(eventSimulatorClient.deleteSimulationFeedConfiguration(svr.properties.simulationName))
        logging.info("Successfully Deleted Simulation Feed Configuration")


    def testDBandCSVSimulation(self):
        logging.info("Test: Random Simulation - Property and Primitive")

        target = {
          "properties": {
            "simulationName": "simulationCSV",
            "timestampStartTime": "1488615136958",
            "timestampEndTime": "1488615136966",
            "timeInterval": "1000"
          },
          "sources": [
            {
              "simulationType": "DATABASE_SIMULATION",
              "streamName": "FooStream",
              "siddhiAppName": "TestSiddhiApp",
              "dataSourceLocation": "jdbc:mysql:\/\/localhost:3306\/DatabaseFeedSimulation",
              "driver" : "com.mysql.jdbc.Driver",
              "username": "root",
              "password": "root",
              "tableName": "foostream3",
              "timestampAttribute": "timestamp",
              "columnNamesList": "symbol,price,volume"
            },
            {
              "simulationType": "CSV_SIMULATION",
              "streamName": "FooStream",
              "siddhiAppName": "TestSiddhiApp",
              "fileName": "sample.csv",
              "timestampAttribute": "0",
              "isOrdered": "False",
              "delimiter": ","
            }
          ]
        }

        dasPythonClient = DASClient(self.hostUrl)
        eventSimulatorClient = dasPythonClient.getEventSimulatorClient()

        svr = FeedSimulationConfiguration("simulationCSV")
        svr.properties.timestampStartTime = 1488615136958
        svr.properties.timestampEndTime = 1488615136966
        svr.properties.timeInterval = 1000

        s1 = SimulationSource(simulationType=SimulationSource.Type.DATABASE_SIMULATION)
        s1.streamName = "FooStream"
        s1.siddhiAppName = "TestSiddhiApp"
        s1.dataSourceLocation = "jdbc:mysql:\/\/localhost:3306\/DatabaseFeedSimulation"
        s1.driver = "com.mysql.jdbc.Driver"
        s1.username = "root"
        s1.password = "root"
        s1.tableName = "foostream3"
        s1.timestampAttribute = "timestamp"
        s1.columnNamesList = "symbol,price,volume"

        svr.sources.append(s1)

        s2 = SimulationSource(simulationType=SimulationSource.Type.CSV_SIMULATION)
        s2.streamName = "FooStream"
        s2.siddhiAppName = "TestSiddhiApp"
        s2.fileName = "sample.csv"
        s2.timestampAttribute = 0
        s2.isOrdered = False
        s2.delimiter = ","

        svr.sources.append(s2)

        match = svr.toJSONObject()

        self.assertDictEqual(target["sources"][1], match["sources"][1])

        self.assertTrue(eventSimulatorClient.uploadCSV("sample.csv", path=resources_path + "sample.csv"))
        logging.info("Successfully Uploaded CSV")

        sleep(5)


        self.assertTrue(eventSimulatorClient.saveSimulationFeedConfiguration(svr))
        logging.info("Successfully Saved Simulation Feed Configuration")

        sleep(5)

        self.assertTrue(eventSimulatorClient.runSimulationFeedConfiguration(svr))
        logging.info("Successfully Started Simulation Feed Configuration")

        sleep(5)

        self.assertTrue(eventSimulatorClient.deleteSimulationFeedConfiguration(svr.properties.simulationName))
        logging.info("Successfully Deleted Simulation Feed Configuration")


        self.assertTrue(eventSimulatorClient.deleteCSV("sample.csv"))
        logging.info("Successfully Deleted CSV")


    def testRunPausePrimitiveRandom(self):
        logging.info("Test: Random Simulation - Primitive. Save, Run, Pause, Resume, Stop and Delete.")

        dasPythonClient = DASClient(self.hostUrl)
        eventSimulatorClient = dasPythonClient.getEventSimulatorClient()

        svr = FeedSimulationConfiguration("simulationPrimitive")
        svr.properties.noOfEvents=8
        svr.properties.timeInterval = 30000

        s1 = SimulationSource(simulationType=SimulationSource.Type.RANDOM_DATA_SIMULATION)
        s1.streamName = "FooStream"
        s1.siddhiAppName = "TestSiddhiApp"
        s1.timestampInterval = 5
        svr.sources.append(s1)

        s1.attributeConfiguration.append(
            AttributeConfiguration(type=AttributeConfiguration.Type.PRIMITIVE_BASED,length=10))
        s1.attributeConfiguration.append(
            AttributeConfiguration(type=AttributeConfiguration.Type.PRIMITIVE_BASED, min=35000, max=30000,precision=2))
        s1.attributeConfiguration.append(
            AttributeConfiguration(type=AttributeConfiguration.Type.PRIMITIVE_BASED, min=150, max=300)
        )

        self.assertTrue(eventSimulatorClient.saveSimulationFeedConfiguration(svr))
        logging.info("Successfully Saved Simulation Feed Configuration")

        sleep(5)

        self.assertTrue(eventSimulatorClient.runSimulationFeedConfiguration(svr))
        logging.info("Successfully Started Simulation Feed Configuration")

        sleep(5)

        self.assertTrue(eventSimulatorClient.pauseSimulationFeedConfiguration(svr.properties.simulationName))
        logging.info("Successfully Paused Simulation Feed Configuration")

        sleep(5)

        self.assertTrue(eventSimulatorClient.resumeSimulationFeedConfiguration(svr.properties.simulationName))
        logging.info("Successfully Resumed Simulation Feed Configuration")

        sleep(5)

        self.assertTrue(eventSimulatorClient.stopSimulationFeedConfiguration(svr.properties.simulationName))
        logging.info("Successfully Stopped Simulation Feed Configuration")

        sleep(5)

        self.assertTrue(eventSimulatorClient.deleteSimulationFeedConfiguration(svr.properties.simulationName))
        logging.info("Successfully Deleted Simulation Feed Configuration")




if __name__ == '__main__':
    unittest.main()
