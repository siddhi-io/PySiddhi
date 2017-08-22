import os
import unittest

import logging
from time import sleep

from PySiddhi4.das.DASClient import DASClient
from PySiddhi4.das.SiddhiAppManagement.SiddhiAppManagementClient import UpdateAppStatusResponse

logging.basicConfig(level=logging.INFO)


resources_path = os.path.join(os.path.dirname(__file__), "Resources")


class EventSimulatorTests(unittest.TestCase):
    def setUp(self):
        self.hostUrl = "http://localhost:9090"
        logging.info("Prior to launching tests, make sure DAS 4 is running at " + self.hostUrl)

    def tearDown(self):
        sleep(5) # Sleep to provide sufficient time for DAS 4.0 to update status

    def testRetrieveSiddhiAppStatus(self):
        logging.info("Test1: Retrieving a Siddhi App Status")
        dasPythonClient = DASClient(self.hostUrl)
        siddhiAppManagementClient = dasPythonClient.getSiddhiAppManagementClient()

        status = siddhiAppManagementClient.retrieveStatusSiddhiApp("TestSiddhiApp")

        self.assertEqual(status,"active")

    def testRetrieveSiddhiApp(self):
        logging.info("Test1: Retrieving a Siddhi App")

        dasPythonClient = DASClient(self.hostUrl)
        siddhiAppManagementClient = dasPythonClient.getSiddhiAppManagementClient()

        app = siddhiAppManagementClient.retrieveSiddhiApp("TestSiddhiApp")

        lines = []
        with open(resources_path + "/TestSiddhiApp.siddhi","rb") as f:
            lines = [line.decode() for line in f.readlines()]

        target_app = "".join(lines)

        logging.info(target_app)

        logging.info(app)
        self.assertEqual(app,target_app)


    def testListSiddhiApps(self):
        logging.info("Test1: List Siddhi Apps")

        dasPythonClient = DASClient(self.hostUrl)
        siddhiAppManagementClient = dasPythonClient.getSiddhiAppManagementClient()

        lines = []
        with open(resources_path + "/TestSiddhiApp1.siddhi", "rb") as f:
            lines = [line.decode() for line in f.readlines()]

        siddhiApp = "".join(lines)

        result = siddhiAppManagementClient.saveSiddhiApp(siddhiApp)
        self.assertTrue(result)

        sleep(5)

        apps = siddhiAppManagementClient.listSiddhiApps()
        print(apps)
        self.assertTrue("TestSiddhiApp1" in apps)
        logging.info(apps)

        apps = siddhiAppManagementClient.listSiddhiApps(isActive=True)
        self.assertTrue("TestSiddhiApp1" in apps)
        logging.info(apps)

        apps = siddhiAppManagementClient.listSiddhiApps(isActive=False)
        self.assertTrue("TestSiddhiApp1" not in apps)
        logging.info(apps)

        result = siddhiAppManagementClient.deleteSiddhiApp("TestSiddhiApp1")
        self.assertTrue(result)




    def testSaveAndDeleteSiddhiApp(self):
        logging.info("Test1: Save and Delete Siddhi App")

        dasPythonClient = DASClient(self.hostUrl)
        siddhiAppManagerClient = dasPythonClient.getSiddhiAppManagementClient()

        lines = []
        with open(resources_path + "/TestSiddhiApp1.siddhi", "rb") as f:
            lines = [line.decode() for line in f.readlines()]

        siddhiApp = "".join(lines)

        result = siddhiAppManagerClient.saveSiddhiApp(siddhiApp)
        self.assertTrue(result)


        sleep(5)

        result = siddhiAppManagerClient.deleteSiddhiApp("TestSiddhiApp1")
        self.assertTrue(result)


    def testUpdateAndDeleteSiddhiApp(self):
        logging.info("Test: Update and Delete Siddhi App")

        dasPythonClient = DASClient(self.hostUrl)
        siddhiAppManagerClient = dasPythonClient.getSiddhiAppManagementClient()

        lines = []
        with open(resources_path + "/TestSiddhiApp1.siddhi", "rb") as f:
            lines = [line.decode() for line in f.readlines()]

        siddhiApp = "".join(lines)

        result = siddhiAppManagerClient.updateSiddhiApp(siddhiApp)
        self.assertTrue(result.name == UpdateAppStatusResponse.savedNew.name)

        sleep(5)

        result = siddhiAppManagerClient.updateSiddhiApp(siddhiApp)
        self.assertTrue(result.name == UpdateAppStatusResponse.updated.name)

        sleep(5)

        result = siddhiAppManagerClient.deleteSiddhiApp("TestSiddhiApp1")
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
