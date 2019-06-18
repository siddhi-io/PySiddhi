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

_event_printer_proxy = SiddhiLoader._loadType("io.siddhi.pythonapi.proxy.core.util.EventPrinterProxy")


def PrintEvent(timestamp, inEvents, outEvents):
    '''
    Prints Stream Event to Log
    :param timestamp:
    :param inEvents:
    :param outEvents:
    :return:
    '''
    if inEvents is not None:
        inEvents = [event._event_proxy for event in inEvents]

    if outEvents is not None:
        outEvents = [event._event_proxy for event in outEvents]
    _event_printer_proxy.printEvent(timestamp, inEvents, outEvents)

    # NOTE: We are unable to call io.siddhi.core.util.EventPrinter.print directly
    # because print is a keyword of python
