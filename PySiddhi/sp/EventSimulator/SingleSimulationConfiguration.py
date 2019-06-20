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

from PySiddhi.sp.ObjectMapping.APIObject import APIObject
from PySiddhi.sp.ObjectMapping.FieldMapping import FieldMapping, ListFieldMapping


class SingleSimulationConfiguration(APIObject):
    '''
    SingleSimulationConfiguration APIObject which may be passed to WSO2 SP Event Simulator via EventSimulatorClient.
    '''

    def __init__(self, siddhiAppName, streamName, data):
        '''
        Instantiates SingleSimulationConfiguration
        :param siddhiAppName: 
        :param streamName: 
        :param data: 
        '''
        self._setup(field_mapping={"siddhiAppName": FieldMapping(str), "streamName": FieldMapping(str),
                                   "data": ListFieldMapping(int, str, []), "timestamp": FieldMapping(int)})
        self.siddhiAppName = siddhiAppName
        self.streamName = streamName
        self.data = data
        self.timestamp = None
