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

from PySiddhi import SiddhiLoader
from PySiddhi.DataTypes import DataWrapper
from PySiddhi.core.SiddhiAppRuntime import SiddhiAppRuntime


class SiddhiManager(object):
    '''
     This is the main interface class of Siddhi where users will interact when using Siddhi as a library.
    '''

    def __init__(self):
        '''
        ''Initialize a new SiddhiManager
        '''
        SiddhiLoader.loadLibrary()
        self._siddhi_manager_proxy = SiddhiLoader.siddhi_api_core_inst.initSiddhiManager()

    def createSiddhiAppRuntime(self, siddhiApp):
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
        if isinstance(clazz, str):
            self._siddhi_manager_proxy.setExtension(name, SiddhiLoader._loadType(clazz))
        else:
            self._siddhi_manager_proxy.setExtension(name, clazz)

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
