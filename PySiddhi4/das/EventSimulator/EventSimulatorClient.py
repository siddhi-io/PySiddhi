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

from PySiddhi4.das.__Communication.RestClient import RestClient
from PySiddhi4.das.EventSimulator.FeedSimulationConfiguration import FeedSimulationConfiguration


class EventSimulatorClient(RestClient):
    '''
    Client used to access DAS Event Simulator End Points
    '''

    def __init__(self, event_simulator_url):
        '''
        Instantiates EventSimulatorClient
        :param event_simulator_url: url to event_simulator endpoint (e.g. root_url + '/simulation')
        '''
        RestClient.__init__(self, event_simulator_url)

    def saveSimulationFeedConfiguration(self, simulationConfiguration):
        '''
        Saves a SimulationFeedConfiguration in WSO2 DAS Event Simulator
        :param simulationConfiguration: 
        :return: 
        '''
        r = self._sendPostRequest("/feed", data=json.dumps(simulationConfiguration.toJSONObject()))
        if r.status_code == 201:
            return True
        elif r.status_code == 409:
            raise Exception("EventSimulationConfiguration with same name already exists.")
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def runSimulationFeedConfiguration(self, simulationConfiguration):
        '''
        Runs a SimulationFeedConfiguration in WSO2 DAS Event Simulator
        :param simulationConfiguration: 
        :return: 
        '''
        r = self._sendPostRequest("/feed/" + simulationConfiguration.properties.simulationName + "/?action=run",
                                  data=json.dumps(simulationConfiguration.toJSONObject()))
        if r.status_code == 200:
            return True
        elif r.status_code == 404:
            raise Exception("EventSimulationConfiguration with given name does not exist.")
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def pauseSimulationFeedConfiguration(self, simulationName):
        '''
        Pauses a SimulationFeedConfiguration in WSO2 DAS Event Simulator
        :param simulationName: 
        :return: 
        '''
        r = self._sendPostRequest("/feed/" + simulationName + "/?action=pause")
        if r.status_code == 200:
            return True
        elif r.status_code == 404:
            raise Exception("EventSimulationConfiguration with given name does not exist.")
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def resumeSimulationFeedConfiguration(self, simulationName):
        '''
        Resumes a SimulationFeedConfiguration in WSO2 DAS Event Simulator
        :param simulationName: 
        :return: 
        '''
        r = self._sendPostRequest("/feed/" + simulationName + "/?action=resume")
        if r.status_code == 200:
            return True
        elif r.status_code == 404:
            raise Exception("EventSimulationConfiguration with given name does not exist.")
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def stopSimulationFeedConfiguration(self, simulationName):
        '''
        Stops a SimulationFeedConfiguration in WSO2 DAS Event Simulator
        :param simulationName: 
        :return: 
        '''
        r = self._sendPostRequest("/feed/" + simulationName + "/?action=stop")
        if r.status_code == 200:
            return True
        elif r.status_code == 404:
            raise Exception("EventSimulationConfiguration with given name does not exist.")
        elif r.status_code == 409:
            raise Exception("EventSimulation is already stopped.")
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def editSimulationFeedConfiguration(self, simulationName, simulationConfiguration):
        '''
        Edits a SimulationFeedConfiguration in WSO2 DAS Event Simulator
        :param simulationName: 
        :param simulationConfiguration: new simulationNameConfiguration
        :return: 
        '''
        r = self._sendPutRequest("/feed/" + simulationName, data=json.dumps(simulationConfiguration.toJSONObject()))
        if r.status_code == 200:
            return True
        elif r.status_code == 404:
            raise Exception("EventSimulationConfiguration with specified name does not exist.")
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def deleteSimulationFeedConfiguration(self, simulationName):
        '''
        Deletes a SimulationFeedConfiguration in WSO2 DAS Event Simulator
        :param simulationName: 
        :return: 
        '''
        r = self._sendDeleteRequest("/feed/" + simulationName)
        if r.status_code == 200:
            return True
        elif r.status_code == 404:
            raise Exception("EventSimulationConfiguration with specified name does not exist.")
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def retrieveSimulationFeedConfiguration(self, simulationName):
        '''
        Retrieves a SimulationFeedConfiguration from WSO2 DAS Event Simulator
        :param simulationName: 
        :return: 
        '''
        r = self._sendGetRequest("/feed/" + simulationName)
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

    def simulateSingleEvent(self, singleSimulationConfiguration):
        '''
        Invokes a Single Simulation in WSO2 DAS Event Simulator
        :param singleSimulationConfiguration: 
        :return: 
        '''
        logging.info("Sending: " + json.dumps(singleSimulationConfiguration.toJSONObject()))
        r = self._sendPostRequest("/single", data=json.dumps(singleSimulationConfiguration.toJSONObject()))
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

    def uploadCSV(self, fileName, stream=None, path=None):
        '''
        Uploads a CSV to WSO2 DAS Event Simulator. Only one of the parameters stream or path should be given.
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
        r = self._sendPostRequest("/files", files=files)

        logging.info(r)

        if r.status_code == 201:
            return True
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def updateCSV(self, uploadedFileName, newFileName, stream=None, path=None):
        '''
        Updates a CSV file uploaded to WSO2 DAS Event Simulator. Only one of parameters stream or path should 
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
        r = self._sendPutRequest("/files/" + uploadedFileName, files=files)

        logging.info(r)

        if r.status_code == 200:
            return True
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def deleteCSV(self, fileName):
        '''
        Deletes a CSV file uploaded to WSO2 DAS Event Simulator
        :param fileName: 
        :return: 
        '''
        r = self._sendDeleteRequest("/files/" + fileName)
        logging.info(r)

        if r.status_code == 200:
            return True
        else:
            raise Exception(str(r.status_code) + ": " + r.text)
