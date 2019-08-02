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

from PySiddhi.sp.EventSimulator.EventSimulatorClient import EventSimulatorClient
from PySiddhi.sp.SiddhiAppManagement.SiddhiAppManagementClient import SiddhiAppManagementClient


class SPClient(object):
    '''
    REST Client to work with WSO2 Stream Processor 4.x.x
    '''

    def __init__(self, host_url):
        '''
        Instantiate REST Client
        :param host_url: host url of SP worker. E.g. http://localhost:9090
        '''
        self.host_url = host_url

    def getSiddhiAppManagementClient(self):
        '''
        Obtain client for managing Siddhi Apps
        :return: 
        '''
        return SiddhiAppManagementClient(self.host_url + "/siddhi-apps")

    def getEventSimulatorClient(self):
        '''
        Obtain client on event simulator
        :return: 
        '''
        return EventSimulatorClient(self.host_url + "/simulation")
