from PySiddhi4 import SiddhiLoader
from PySiddhi4.DataTypes import DataWrapper
from PySiddhi4.core.SiddhiAppRuntime import SiddhiAppRuntime


class SiddhiManager(object):
    def __init__(self):
        '''
        ''Initialize a new SiddhiManager
        '''
        SiddhiLoader.loadLibrary()
        self._siddhi_manager_proxy = SiddhiLoader.siddhi_api_core_inst.initSiddhiManager()
    def createSiddhiAppRuntime(self,siddhiApp):
        '''
        Create an Siddhi app Runtime
        :param siddhiApp: SiddhiQuery (string) defining siddhi app
        :return: SiddhiAppRuntime
        '''

        siddhi_app_runtime_proxy = self._siddhi_manager_proxy.createSiddhiAppRuntime(siddhiApp)
        return SiddhiAppRuntime._fromSiddhiAppRuntimeProxy(siddhi_app_runtime_proxy)

    def getExtensions(self):
        '''
        Obtain the dictionary of loaded extensions
        :return: 
        '''
        return DataWrapper.unwrapHashMap(self._siddhi_manager_proxy.getExtensions())

    def setExtension(self, name, clazz):
        '''
        Loads an extension into Siddhi Manager. The Extension Path must be already added via 
        SiddhiLoader.addExtensionPath.
        :param name: Name of extension
        :param clazz: Fully qualified class name of extension
        :return: 
        '''
        if isinstance(clazz,str):
            self._siddhi_manager_proxy.setExtension(name, SiddhiLoader._loadType(clazz))
        else:
            self._siddhi_manager_proxy.setExtension(name,clazz)

    def persist(self):
        '''
        Method used persist state of current Siddhi Manager instance.
        :return: 
        '''
        self._siddhi_manager_proxy.persist()

    def restoreLastState(self):
        '''
        Method used to restore state of Current Siddhi Manager instance.
        :return: 
        '''
        self._siddhi_manager_proxy.restoreLastState()

    def shutdown(self):
        '''
        Shutdown SiddhiManager
        :return:
        '''
        self._siddhi_manager_proxy.shutdown()
        del self._siddhi_manager_proxy


