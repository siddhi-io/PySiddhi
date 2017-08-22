from PySiddhi4.das.EventSimulator.EventSimulatorClient import EventSimulatorClient
from PySiddhi4.das.SiddhiAppManagement.SiddhiAppManagementClient import SiddhiAppManagementClient


class DASClient(object):
    '''
    REST Client to work with WSO2 Data Analytics Server 4.0
    '''
    def __init__(self, host_url):
        '''
        Instantiate REST Client
        :param host_url: host url of DAS4. E.g. http://localhost:9090
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
