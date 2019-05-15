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

import unittest
import logging

logging.basicConfig(level=logging.INFO)

from PySiddhi5.DataTypes.LongType import LongType
from PySiddhi5.core.event.Event import Event


class BasicTests(unittest.TestCase):
    def test_data(self):
        logging.info("Test GetData and SetData Methods")

        event = Event(1, [2, LongType(3)])
        self.assertListEqual(event.getData(), [2, LongType(3)], "GetData not equal to data given in constructor")
        self.assertTrue(type(event.getData(1)) == LongType, "Type of Parameter is not LongType")

        event.setData([1, 2])
        self.assertListEqual(event.getData(), [1, 2], "GetData not equal to data set by SetData")

    def test_copyFromAndToString(self):
        logging.info("Test CopyFrom and ToString methods")

        event = Event(1, [2, LongType(3)])
        event2 = Event(2)
        event2.copyFrom(event)

        self.assertEqual(str(event), str(event2), "ToString forms of copy is not equal")

    def test_Equals(self):
        logging.info("Test CopyFrom and ToString methods")

        event = Event(1, [2, LongType(3)])
        event2 = Event(1, [2, LongType(3)])

        self.assertEqual(event, event2, "Copy is not equal")

        event2 = Event(1, [2, 3])
        self.assertNotEqual(event, event2, "Should not be equal due to Type diference")


if __name__ == '__main__':
    unittest.main()
