from abc import ABCMeta, abstractmethod

import logging

import PySiddhi4.core

from future.utils import with_metaclass

from PySiddhi4 import SiddhiLoader

_siddhi_debugger_callback_proxy = SiddhiLoader._loadType("org.wso2.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger_callback.SiddhiDebuggerCallbackProxy")

class SiddhiDebuggerCallback(with_metaclass(ABCMeta,object)):
    def __init__(self):
        _siddhi_debugger_callback_self = self
        self._siddhi_debugger_callback_proxy_inst = _siddhi_debugger_callback_proxy()

    @abstractmethod
    def debugEvent(self, complexEvent, queryName, queryTerminal, debugger):
        pass
