from PySiddhi4.das.EventSimulator.SimulationProperties import SimulationProperties
from PySiddhi4.das.EventSimulator.SimulationSource import SimulationSource
from PySiddhi4.das.ObjectMapping.APIObject import APIObject
from PySiddhi4.das.ObjectMapping.FieldMapping import FieldMapping, ListFieldMapping


class FeedSimulationConfiguration(APIObject):
    '''
    FeedSimulationConfiguration API Object which could be passed to WSO2 DAS Event Simulator via EventSimulatorClient.
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
