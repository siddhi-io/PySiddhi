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

import json
import logging

from PySiddhi.sp.__Communication.RestClient import RestClient
from PySiddhi.sp.EventSimulator.FeedSimulationConfiguration import FeedSimulationConfiguration
from requests.auth import HTTPBasicAuth


class EventSimulatorClient(RestClient):
    '''
    Client used to access SP Event Simulator End Points
    '''

    def __init__(self, event_simulator_url):
        '''
        Instantiates EventSimulatorClient
        :param event_simulator_url: url to event_simulator endpoint (e.g. root_url + '/simulation')
        '''
        RestClient.__init__(self, event_simulator_url)

    def saveSimulationFeedConfiguration(self, simulationConfiguration, username, password):
        '''
        Saves a SimulationFeedConfiguration in WSO2 SP Event Simulator
        :param simulationConfiguration: 
        :return: 
        '''
        r = self._sendPostRequest("/feed", data=json.dumps(simulationConfiguration.toJSONObject()),
                                  auth=HTTPBasicAuth(username, password))
        if r.status_code == 201:
            return True
        elif r.status_code == 409:
            raise Exception("EventSimulationConfiguration with same name already exists.")
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def runSimulationFeedConfiguration(self, simulationConfiguration, username, password):
        '''
        Runs a SimulationFeedConfiguration in WSO2 SP Event Simulator
        :param simulationConfiguration: 
        :return: 
        '''
        r = self._sendPostRequest("/feed/" + simulationConfiguration.properties.simulationName + "/?action=run",
                                  data=json.dumps(simulationConfiguration.toJSONObject()),
                                  auth=HTTPBasicAuth(username, password))
        if r.status_code == 200:
            return True
        elif r.status_code == 404:
            raise Exception("EventSimulationConfiguration with given name does not exist.")
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def pauseSimulationFeedConfiguration(self, simulationName, username, password):
        '''
        Pauses a SimulationFeedConfiguration in WSO2 SP Event Simulator
        :param simulationName: 
        :return: 
        '''
        r = self._sendPostRequest("/feed/" + simulationName + "/?action=pause", auth=HTTPBasicAuth(username, password))
        if r.status_code == 200:
            return True
        elif r.status_code == 404:
            raise Exception("EventSimulationConfiguration with given name does not exist.")
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def resumeSimulationFeedConfiguration(self, simulationName, username, password):
        '''
        Resumes a SimulationFeedConfiguration in WSO2 SP Event Simulator
        :param simulationName: 
        :return: 
        '''
        r = self._sendPostRequest("/feed/" + simulationName + "/?action=resume", auth=HTTPBasicAuth(username, password))
        if r.status_code == 200:
            return True
        elif r.status_code == 404:
            raise Exception("EventSimulationConfiguration with given name does not exist.")
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def stopSimulationFeedConfiguration(self, simulationName, username, password):
        '''
        Stops a SimulationFeedConfiguration in WSO2 SP Event Simulator
        :param simulationName: 
        :return: 
        '''
        r = self._sendPostRequest("/feed/" + simulationName + "/?action=stop", auth=HTTPBasicAuth(username, password))
        if r.status_code == 200:
            return True
        elif r.status_code == 404:
            raise Exception("EventSimulationConfiguration with given name does not exist.")
        elif r.status_code == 409:
            raise Exception("EventSimulation is already stopped.")
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def editSimulationFeedConfiguration(self, simulationName, simulationConfiguration, username, password):
        '''
        Edits a SimulationFeedConfiguration in WSO2 SP Event Simulator
        :param simulationName: 
        :param simulationConfiguration: new simulationNameConfiguration
        :return: 
        '''
        r = self._sendPutRequest("/feed/" + simulationName, data=json.dumps(simulationConfiguration.toJSONObject()),
                                 auth=HTTPBasicAuth(username, password))
        if r.status_code == 200:
            return True
        elif r.status_code == 404:
            raise Exception("EventSimulationConfiguration with specified name does not exist.")
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def deleteSimulationFeedConfiguration(self, simulationName, username, password):
        '''
        Deletes a SimulationFeedConfiguration in WSO2 SP Event Simulator
        :param simulationName: 
        :return: 
        '''
        r = self._sendDeleteRequest("/feed/" + simulationName, auth=HTTPBasicAuth(username, password))
        if r.status_code == 200:
            return True
        elif r.status_code == 404:
            raise Exception("EventSimulationConfiguration with specified name does not exist.")
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def retrieveSimulationFeedConfiguration(self, simulationName, username, password):
        '''
        Retrieves a SimulationFeedConfiguration from WSO2 SP Event Simulator
        :param simulationName: 
        :return: 
        '''
        r = self._sendGetRequest("/feed/" + simulationName, auth=HTTPBasicAuth(username, password))
        if r.status_code == 200:
            result = r.json()
            if result["status"].lower() == "ok":
                jsonObject = json.loads(result["message"])["Simulation configuration"]
                return FeedSimulationConfiguration.parse(jsonObject)
            else:
                raise Exception("Respose says not ok")
        elif r.status_code == 404:
            raise Exception("EventSimulationConfiguration with specified name does not exist.")
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def simulateSingleEvent(self, singleSimulationConfiguration, username, password):
        '''
        Invokes a Single Simulation in WSO2 SP Event Simulator
        :param singleSimulationConfiguration: 
        :return: 
        '''
        logging.info("Sending: " + json.dumps(singleSimulationConfiguration.toJSONObject()))
        r = self._sendPostRequest("/single", data=json.dumps(singleSimulationConfiguration.toJSONObject()),
                                  auth=HTTPBasicAuth(username, password))
        if r.status_code == 200:
            logging.info("Received: " + r.text)
            result = r.json()
            if result["status"].lower() == "ok":
                return True
            else:
                raise Exception("Respose says not ok")
        elif r.status_code == 409:
            raise Exception("EventSimulationConfiguration with same name already exists.")
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def uploadCSV(self, fileName, username, password, stream=None, path=None):
        '''
        Uploads a CSV to WSO2 SP Event Simulator. Only one of the parameters stream or path should be given.
        :param fileName: fileName of file to be uploaded
        :param stream: stream of file to be uploaded
        :param path: path of file to be uploaded
        :return: 
        '''
        files = {}
        if stream is not None:
            files = {"file": (fileName, stream)}
        else:
            files = {"file": (fileName, open(path, "rb"))}
        r = self._sendPostRequest("/files", files=files, auth=HTTPBasicAuth(username, password))

        logging.info(r)

        if r.status_code == 201:
            return True
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def updateCSV(self, uploadedFileName, newFileName, username, password, stream=None, path=None):
        '''
        Updates a CSV file uploaded to WSO2 SP Event Simulator. Only one of parameters stream or path should
        be provided.
        :param uploadedFileName: previous file name
        :param newFileName: new file name
        :param stream: stream of file to be uploaded
        :param path: path of file to be uploaded
        :return: 
        '''
        files = {}
        if stream is not None:
            files = {"file": (newFileName, stream)}
        else:
            files = {"file": (newFileName, open(path, "rb"))}
        r = self._sendPutRequest("/files/" + uploadedFileName, files=files, auth=HTTPBasicAuth(username, password))

        logging.info(r)

        if r.status_code == 200:
            return True
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def deleteCSV(self, fileName, username, password):
        '''
        Deletes a CSV file uploaded to WSO2 SP Event Simulator
        :param fileName: 
        :return: 
        '''
        r = self._sendDeleteRequest("/files/" + fileName, auth=HTTPBasicAuth(username, password))
        logging.info(r)

        if r.status_code == 200:
            return True
        else:
            raise Exception(str(r.status_code) + ": " + r.text)
