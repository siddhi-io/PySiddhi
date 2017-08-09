from PySiddhi3.DataTypes import DataWrapper

import PySiddhi3.core
from PySiddhi3 import SiddhiLoader
from PySiddhi3.core.ExecutionPlanRuntime import ExecutionPlanRuntime

class SiddhiManager(object):
    def __init__(self):
        '''
        ''Initialize a new SiddhiManager
        '''
        SiddhiLoader.loadLibrary()
        self._siddhi_manager_proxy = SiddhiLoader.siddhi_api_core_inst.initSiddhiManager()

    def createExecutionPlanRuntime(self,executionPlan):
        '''
        Create an Execution Plan Runtime
        :param executionPlan: SiddhiQuery (string) defining execution plan
        :return: ExecutionPlanRuntime
        '''
        execution_plan_runtime_proxy = self._siddhi_manager_proxy.createExecutionPlanRuntime(executionPlan)
        return ExecutionPlanRuntime._fromExecutionPlanRuntimeProxy(execution_plan_runtime_proxy)

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

    def shutdown(self):
        '''
        Shutdown SiddhiManager
        :return:
        '''
        self._siddhi_manager_proxy.shutdown()
        del self._siddhi_manager_proxy


