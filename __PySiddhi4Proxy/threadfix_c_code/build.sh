#!/usr/bin/env bash
# ---------------------------------------------------------------------------
#  Copyright (c) 2017, WSO2 Inc. (http://www.wso2.org) All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

echo "Compiling C++ Code used for fixing threading issue"
echo "Invoking G++ Compiler"

if [["$OSTYPE" == "darwin"*]]; then
    g++ -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/darwin" -I "$PYTHONHOME" -shared -fPIC -o liborg_wso2_siddhi_pythonapi_threadfix_pythreadfix.so org_wso2_siddhi_pythonapi_threadfix_PyThreadFix.c
elif [["$OSTYPE" == "linux-gnu"]]; then
    g++ -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/linux" -I "$PYTHONHOME" -shared -fPIC -o liborg_wso2_siddhi_pythonapi_threadfix_pythreadfix.so org_wso2_siddhi_pythonapi_threadfix_PyThreadFix.c
fi

echo "Copying output library to ../../../../SiddhiCEP4"
cp liborg_wso2_siddhi_pythonapi_threadfix_pythreadfix.so ../../../liborg_wso2_siddhi_pythonapi_threadfix_pythreadfix.so
echo "All is well!"