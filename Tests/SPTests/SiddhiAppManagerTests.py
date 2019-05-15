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

import os
import unittest

import logging
from time import sleep

from PySiddhi5.sp.SPClient import SPClient
from PySiddhi5.sp.SiddhiAppManagement.SiddhiAppManagementClient import UpdateAppStatusResponse

logging.basicConfig(level=logging.INFO)

resources_path = os.path.join(os.path.dirname(__file__), "Resources")


class EventSimulatorTests(unittest.TestCase):
    def setUp(self):
        self.hostUrl = "http://localhost:9090"
        logging.info("Prior to launching tests, make sure SP 4 is running at " + self.hostUrl)

    def tearDown(self):
        sleep(5)  # Sleep to provide sufficient time for SP 4.0 to update status

    def testRetrieveSiddhiAppStatus(self):
        logging.info("Test1: Retrieving a Siddhi App Status")
        spPythonClient = SPClient(self.hostUrl)
        siddhiAppManagementClient = spPythonClient.getSiddhiAppManagementClient()

        status = siddhiAppManagementClient.retrieveStatusSiddhiApp("TestSiddhiApp", username="admin",
                                                                   password="admin")

        self.assertEqual(status, "active")

    def testRetrieveSiddhiApp(self):
        logging.info("Test1: Retrieving a Siddhi App")

        spPythonClient = SPClient(self.hostUrl)
        siddhiAppManagementClient = spPythonClient.getSiddhiAppManagementClient()

        app = siddhiAppManagementClient.retrieveSiddhiApp("TestSiddhiApp", username="admin",
                                                          password="admin")

        lines = []
        with open(resources_path + "/TestSiddhiApp.siddhi", "rb") as f:
            lines = [line.decode() for line in f.readlines()]

        target_app = "".join(lines)

        logging.info(target_app)

        logging.info(app)
        self.assertEqual(app, target_app)

    def testListSiddhiApps(self):
        logging.info("Test1: List Siddhi Apps")

        spPythonClient = SPClient(self.hostUrl)
        siddhiAppManagementClient = spPythonClient.getSiddhiAppManagementClient()

        lines = []
        with open(resources_path + "/TestSiddhiApp1.siddhi", "rb") as f:
            lines = [line.decode() for line in f.readlines()]

        siddhiApp = "".join(lines)

        result = siddhiAppManagementClient.saveSiddhiApp(siddhiApp, username="admin",
                                                         password="admin")
        self.assertTrue(result)

        sleep(5)

        apps = siddhiAppManagementClient.listSiddhiApps(username="admin",
                                                        password="admin")
        logging.info(apps)
        self.assertTrue("TestSiddhiApp1" in apps)
        logging.info(apps)

        apps = siddhiAppManagementClient.listSiddhiApps(username="admin",
                                                        password="admin", isActive=True)
        self.assertTrue("TestSiddhiApp1" in apps)
        logging.info(apps)

        apps = siddhiAppManagementClient.listSiddhiApps(username="admin",
                                                        password="admin", isActive=False)
        self.assertTrue("TestSiddhiApp1" not in apps)
        logging.info(apps)

        result = siddhiAppManagementClient.deleteSiddhiApp("TestSiddhiApp1", username="admin",
                                                           password="admin")
        self.assertTrue(result)

    def testSaveAndDeleteSiddhiApp(self):
        logging.info("Test1: Save and Delete Siddhi App")

        spPythonClient = SPClient(self.hostUrl)
        siddhiAppManagerClient = spPythonClient.getSiddhiAppManagementClient()

        lines = []
        with open(resources_path + "/TestSiddhiApp1.siddhi", "rb") as f:
            lines = [line.decode() for line in f.readlines()]

        siddhiApp = "".join(lines)

        result = siddhiAppManagerClient.saveSiddhiApp(siddhiApp, username="admin",
                                                      password="admin")
        self.assertTrue(result)

        sleep(5)

        result = siddhiAppManagerClient.deleteSiddhiApp("TestSiddhiApp1", username="admin",
                                                        password="admin")
        self.assertTrue(result)

    def testUpdateAndDeleteSiddhiApp(self):
        logging.info("Test: Update and Delete Siddhi App")

        spPythonClient = SPClient(self.hostUrl)
        siddhiAppManagerClient = spPythonClient.getSiddhiAppManagementClient()

        lines = []
        with open(resources_path + "/TestSiddhiApp1.siddhi", "rb") as f:
            lines = [line.decode() for line in f.readlines()]

        siddhiApp = "".join(lines)

        result = siddhiAppManagerClient.updateSiddhiApp(siddhiApp, username="admin",
                                                        password="admin")
        self.assertTrue(result.name == UpdateAppStatusResponse.savedNew.name)

        sleep(5)

        result = siddhiAppManagerClient.updateSiddhiApp(siddhiApp, username="admin",
                                                        password="admin")
        self.assertTrue(result.name == UpdateAppStatusResponse.updated.name)

        sleep(5)

        result = siddhiAppManagerClient.deleteSiddhiApp("TestSiddhiApp1", username="admin",
                                                        password="admin")
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
