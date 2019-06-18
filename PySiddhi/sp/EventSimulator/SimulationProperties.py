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

import random

from PySiddhi.sp.ObjectMapping.APIObject import APIObject, NotSet
from PySiddhi.sp.ObjectMapping.FieldMapping import FieldMapping
from PySiddhi.sp.__Util import decodeField

ran = random


class SimulationProperties(APIObject):
    '''
    SimulationProperties API Object of FeedSimulationConfiguration.
    '''

    def __init__(self, simulationName="Simulation_" + str(random.randint(1, 1000)), timestampStartTime=NotSet(),
                 timestampEndTime=NotSet(), noOfEvents=NotSet(), timeInterval=NotSet()):
        '''
        Instantiates SimulationProperties
        :param simulationName: name of simulation
        :param timestampStartTime: 
        :param timestampEndTime: 
        :param noOfEvents: 
        :param timeInterval: 
        '''
        self._setup(field_mapping={"simulationName": FieldMapping(str), "timestampStartTime": FieldMapping(int),
                                   "timestampEndTime": FieldMapping(int), "noOfEvents": FieldMapping(int),
                                   "timeInterval": FieldMapping(int)})

        self.simulationName = simulationName
        self.timestampStartTime = timestampStartTime
        self.timestampEndTime = timestampEndTime
        self.noOfEvents = noOfEvents
        self.timeInterval = timeInterval

    @classmethod
    def parse(cls, jsonObject):
        '''
        Converts a Python Class Object (from JSON) to SimulationProperties Object.
        :param jsonObject: 
        :return: 
        '''
        result = SimulationProperties(simulationName=decodeField(jsonObject["simulationName"], str))
        result._parse(jsonObject)
        return result
