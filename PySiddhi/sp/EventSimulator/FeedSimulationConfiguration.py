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

from PySiddhi.sp.EventSimulator.SimulationProperties import SimulationProperties
from PySiddhi.sp.EventSimulator.SimulationSource import SimulationSource
from PySiddhi.sp.ObjectMapping.APIObject import APIObject
from PySiddhi.sp.ObjectMapping.FieldMapping import FieldMapping, ListFieldMapping


class FeedSimulationConfiguration(APIObject):
    '''
    FeedSimulationConfiguration API Object which could be passed to WSO2 SP Event Simulator via EventSimulatorClient.
    '''

    def __init__(self, simulation_name=None, properties=None):
        '''
        Instantiates FeedSimulationConfiguration.
        :param simulation_name: name of simulation
        :param properties: SimulationProperties
        '''
        self._setup(
            field_mapping={"properties": FieldMapping(SimulationProperties.parse, SimulationProperties.toJSONObject),
                           "sources": ListFieldMapping(SimulationSource.parse, SimulationSource.toJSONObject, [])})
        if properties is not None:
            self.properties = properties
        elif simulation_name is not None:
            self.properties = SimulationProperties(simulationName=simulation_name)
        else:
            self.properties = SimulationProperties()
        self.sources = []

    @classmethod
    def parse(cls, jsonObject):
        '''
        Converts a Python Class Object (from JSON) to FeedSimulationConfiguration.
        :param jsonObject: 
        :return: 
        '''
        result = FeedSimulationConfiguration(simulation_name=jsonObject["properties"]["simulationName"])
        result._parse(jsonObject)
        return result
