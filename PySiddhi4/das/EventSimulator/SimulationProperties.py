import random

from PySiddhi4.das.ObjectMapping.APIObject import APIObject, NotSet
from PySiddhi4.das.ObjectMapping.FieldMapping import FieldMapping
from PySiddhi4.das.__Util import decodeField

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
