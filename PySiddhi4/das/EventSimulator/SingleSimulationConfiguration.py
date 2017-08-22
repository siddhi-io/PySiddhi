from PySiddhi4.das.ObjectMapping.APIObject import APIObject
from PySiddhi4.das.ObjectMapping.FieldMapping import FieldMapping, ListFieldMapping


class SingleSimulationConfiguration(APIObject):
    '''
    SingleSimulationConfiguration APIObject which may be passed to WSO2 DAS Event Simulator via EventSimulatorClient.
    '''
    def __init__(self, siddhiAppName, streamName, data):
        '''
        Instantiates SingleSimulationConfiguration
        :param siddhiAppName: 
        :param streamName: 
        :param data: 
        '''
        self._setup(field_mapping={"siddhiAppName":FieldMapping(str),"streamName":FieldMapping(str),
                                   "data":ListFieldMapping(int,str, []), "timestamp":FieldMapping(int)})
        self.siddhiAppName = siddhiAppName
        self.streamName = streamName
        self.data = data
        self.timestamp = None

