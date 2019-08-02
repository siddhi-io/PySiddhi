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

from PySiddhi.sp.EventSimulator.AttributeConfiguration import AttributeConfiguration
from PySiddhi.sp.ObjectMapping.APIObject import APIObject, NotSet
from PySiddhi.sp.ObjectMapping.FieldMapping import FieldMapping, ListFieldMapping, strOrInt


class SimulationSource(APIObject):
    '''
    SimulationSource APIObject which can be added to sources of FeedSimulationConfiguration
    '''

    class Type(Enum):
        '''
        Type of SimulationSource
        '''
        RANDOM_DATA_SIMULATION = "RANDOM_DATA_SIMULATION"
        CSV_SIMULATION = "CSV_SIMULATION"
        DATABASE_SIMULATION = "DATABASE_SIMULATION"

        @classmethod
        def encode(cls, v):
            return v.value

        @classmethod
        def decode(cls, v):
            return SimulationSource.Type(v)

    def __init__(self, simulationType=Type.RANDOM_DATA_SIMULATION, streamName=NotSet(), siddhiAppName=NotSet(),
                 timestampInterval=NotSet(), attributeConfiguration=NotSet(),
                 fileName=NotSet(), isOrdered=NotSet(), delimiter=NotSet(), timestampAttribute=NotSet(),
                 dataSourceLocation=NotSet(), driver=NotSet(),
                 username=NotSet(), password=NotSet(), tableName=NotSet(), columnNamesList=NotSet()):
        '''
        Instantiates Simulation Source. Refer SP4 Documentation for details on parameters
        :param simulationType: Type of SimulationSource
        :param streamName: 
        :param siddhiAppName: 
        :param timestampInterval: 
        :param attributeConfiguration: 
        :param fileName: for File Access
        :param isOrdered: 
        :param delimiter: 
        :param timestampAttribute: 
        :param dataSourceLocation: 
        :param driver: for DB Access
        :param username: for DB access
        :param password: for DB Access
        :param tableName: for DB Access
        :param columnNamesList: for DB Access
        '''
        self._setup(
            field_mapping={"simulationType": FieldMapping(SimulationSource.Type.decode, SimulationSource.Type.encode),
                           "streamName": FieldMapping(str),
                           "siddhiAppName": FieldMapping(str), "timestampInterval": FieldMapping(int),
                           "attributeConfiguration": ListFieldMapping(AttributeConfiguration.parse,
                                                                      AttributeConfiguration.toJSONObject, []),
                           "fileName": FieldMapping(str), "isOrdered": FieldMapping(bool),
                           "delimiter": FieldMapping(str),
                           "timestampAttribute": FieldMapping(strOrInt), "dataSourceLocation": FieldMapping(str),
                           "driver": FieldMapping(str),
                           "username": FieldMapping(str), "password": FieldMapping(str), "tableName": FieldMapping(str),
                           "columnNamesList": FieldMapping(str)})

        self.simulationType = simulationType
        self.streamName = streamName
        self.siddhiAppName = siddhiAppName
        self.timestampInterval = timestampInterval
        if attributeConfiguration == NotSet():
            self.attributeConfiguration = []
        else:
            self.attributeConfiguration = attributeConfiguration
        self.fileName = fileName
        self.isOrdered = isOrdered
        self.delimiter = delimiter
        self.timestampAttribute = timestampAttribute
        self.dataSourceLocation = dataSourceLocation
        self.driver = driver
        self.username = username
        self.password = password
        self.tableName = tableName
        self.columnNamesList = columnNamesList

    @classmethod
    def parse(cls, jsonObject):
        '''
        Converts a Python Class Object (from JSON) to SimulationSource Object.
        :param jsonObject: 
        :return: 
        '''
        result = SimulationSource()
        result._parse(jsonObject)
        return result
