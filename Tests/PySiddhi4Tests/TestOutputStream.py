# Copyright (c) 2016, WSO2 Inc. (http://www.wso2.org) All Rights Reserved.
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

import unittest

import logging

logging.basicConfig(level=logging.INFO)

from time import sleep
from unittest.case import TestCase

from PySiddhi4.core.SiddhiManager import SiddhiManager
from PySiddhi4.core.stream.output.StreamCallback import StreamCallback
from Tests.Util.AtomicInt import AtomicInt


class TestOutputStream(TestCase):
    def setUp(self):
        self.inEventCount = AtomicInt(0)
        self.debugEventCount = AtomicInt(0)

    def getCount(self, event):
        count = 0
        while event != None:
            count += 1
            event = event.getNext()

        return count

    def test_outputstram(self):
        logging.info("OutputStream Test 1: Test reception of events")
        siddhiManager = SiddhiManager()
        cseEventStream = "@config(async = 'true') define stream cseEventStream (symbol string, price float, volume int);"

        query = "@info(name = 'query 1') from cseEventStream select symbol, price, volume insert into OutputStream; "

        siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(cseEventStream + query)

        _self_shaddow = self

        class StreamCallbackImpl(StreamCallback):
            def receive(self, events):
                _self_shaddow.inEventCount.addAndGet(len(events))

        siddhiAppRuntime.addCallback("OutputStream", StreamCallbackImpl())

        inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")

        inputHandler.send(["WSO2", 50.0, 60])
        inputHandler.send(["WSO2", 70.0, 40])

        sleep(1)

        _self_shaddow.assertEqual(2, _self_shaddow.inEventCount.get(), "Invalid number of output events")

        siddhiAppRuntime.shutdown()


if __name__ == '__main__':
    unittest.main()
