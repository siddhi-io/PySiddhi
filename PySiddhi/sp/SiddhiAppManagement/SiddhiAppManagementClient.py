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

from enum import Enum
from requests.auth import HTTPBasicAuth

from PySiddhi.sp.__Communication.RestClient import RestClient


class UpdateAppStatusResponse(Enum):
    '''
    Response from WSO2 SP on updateSidhdiApp call of SiddhiAppManagementClient.
    '''
    savedNew = 201,
    updated = 200


class SiddhiAppManagementClient(RestClient):
    '''
    Client for Siddhi App Management (publish, edit, list, retrieve etc.) in WSO2 SP.
    '''

    def __init__(self, siddhi_apps_url):
        '''
        Instantiates SiddhiAppMangementClient. 
        :param siddhi_apps_url: url to siddhi_apps endpoint (e.g. root_url + '/siddhi-apps')
        '''
        RestClient.__init__(self, siddhi_apps_url)

    def retrieveSiddhiApp(self, siddhiAppName, username, password):
        '''
        Retrieve siddhiApp stored in WSO2 SP.
        :param siddhiAppName: 
        :return: 
        '''
        r = self._sendGetRequest("/" + siddhiAppName, auth=HTTPBasicAuth(username, password))
        if r.status_code == 200:
            result = r.json()
            if "content" in result.keys():
                siddhiApp = result["content"]
                return siddhiApp
            else:
                raise Exception("No content defined in response")
        elif r.status_code == 404:
            raise Exception("Siddhi App with specified name does not exist.")
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def deleteSiddhiApp(self, siddhiAppName, username, password):
        '''
        Deletes a SiddhiApp stored in WSO2 SP.
        :param siddhiAppName: 
        :return: 
        '''
        r = self._sendDeleteRequest("/" + siddhiAppName, auth=HTTPBasicAuth(username, password))
        if r.status_code == 200:
            return True
        elif r.status_code == 400:
            raise Exception("Siddhi App name provided is invalid.")
        elif r.status_code == 404:
            raise Exception("Siddhi App with specified name does not exist.")
        elif r.status_code == 500:
            raise Exception(str(r.status_code) + ": " + r.text)
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def retrieveStatusSiddhiApp(self, siddhiAppName, username, password):
        '''
        Retrieve the status of a SiddhiApp in WSO2 SP.
        :param siddhiAppName: 
        :return: 
        '''
        r = self._sendGetRequest("/" + siddhiAppName + "/status", auth=HTTPBasicAuth(username, password))
        if r.status_code == 200:
            result = r.json()
            if "status" in result.keys():
                status = result["status"]
                return status
            else:
                raise Exception("No content defined in response")
        elif r.status_code == 404:
            raise Exception("Siddhi App with specified name does not exist.")
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def listSiddhiApps(self,username, password, isActive=None):
        '''
        Obtains the list of Siddhi Apps in WSO2 SP.
        :param isActive: 
        :return: 
        '''
        params = None
        if isActive is not None:
            params = {"isActive": isActive}
        r = self._sendGetRequest("/", params=params, auth=HTTPBasicAuth(username, password))
        if r.status_code == 200:
            result = r.json()
            return result
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def updateSiddhiApp(self, siddhiApp, username, password):
        '''
        Updates a Siddhi App in WSO2 SP.
        :param siddhiApp: 
        :return: 
        '''
        r = self._sendPutRequest("/", data=siddhiApp, auth=HTTPBasicAuth(username, password))
        if r.status_code == 200 or r.status_code == 201:
            result = r.json()
            if result["type"] == "success":
                if r.status_code == 200:
                    return UpdateAppStatusResponse.updated
                elif r.status_code == 201:
                    return UpdateAppStatusResponse.savedNew
            else:
                raise Exception("Result 'type' not 'success'")
        elif r.status_code == 400:
            raise Exception("A validation error occured.")
        elif r.status_code == 500:
            raise Exception("An unexpected error occured.")
        else:
            raise Exception(str(r.status_code) + ": " + r.text)

    def saveSiddhiApp(self, siddhiApp, username, password):
        '''
        Saves a Siddhi App to WSO2 SP.
        :param siddhiApp: 
        :return: 
        '''
        r = self._sendPostRequest("/", data=siddhiApp, auth=HTTPBasicAuth(username, password))
        if r.status_code == 201:
            result = r.json()
            if result["type"] == "success":
                return True
            else:
                raise Exception("Result 'type' not 'success'")
        elif r.status_code == 400:
            raise Exception("A validation error occured.")
        elif r.status_code == 409:
            raise Exception("A Siddhi Application with the given name already exists.")
        elif r.status_code == 500:
            raise Exception("An unexpected error occured.")
        else:
            raise Exception(str(r.status_code) + ": " + r.text)
