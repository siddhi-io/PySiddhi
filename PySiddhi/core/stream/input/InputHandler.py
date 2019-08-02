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
from PySiddhi.DataTypes.DataWrapper import wrapData

input_handler_proxy = SiddhiLoader._loadType(
    "io.siddhi.pythonapi.proxy.core.stream.input.input_handler.InputHandlerProxy")


class InputHandler(object):
    '''
    Handles input to SiddhiAppRuntime.
    Wrapper on io.siddhi.core.stream.input.InputHandler
    '''

    def __init__(self):
        raise NotImplementedError("Initialize InputHandler using SiddhiAppRuntime")

    def __new__(cls):
        bare_instance = object.__new__(cls)
        bare_instance.input_handler_proxy = None
        return bare_instance

    def send(self, data):
        '''
        Sends data as an event to system.
        :param data: 
        :return: 
        '''
        wrapped_data = wrapData(data)
        input_handler_proxy_inst = input_handler_proxy()
        input_handler_proxy_inst.send(self.input_handler_proxy, wrapped_data)

    @classmethod
    def _fromInputHandlerProxy(cls, input_handler_proxy):
        '''
        Internal Constructor to wrap around JAVA Class InputHandler
        :param input_handler_proxy:
        :return:
        '''
        instance = cls.__new__(cls)
        instance.input_handler_proxy = input_handler_proxy
        return instance
