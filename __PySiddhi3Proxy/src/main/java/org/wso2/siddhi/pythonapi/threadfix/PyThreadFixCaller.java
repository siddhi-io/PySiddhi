/*
 * Copyright (c) 2017, WSO2 Inc. (http://www.wso2.org) All Rights Reserved.
 *
 * WSO2 Inc. licenses this file to you under the Apache License,
 * Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied. See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

package org.wso2.siddhi.pythonapi.threadfix;

import org.wso2.siddhi.pythonapi.proxy.core.SiddhiAPICoreProxy;


/**
 * A wrapper on ThreadFix Call
 */
public class PyThreadFixCaller {

    private PyThreadFixCaller() {
    }

    /**
     * Invokes threadFix if required
     */
    public static void fix() {
        if (System.getProperty("os.name").toLowerCase().startsWith("windows")) //No Threadfix for Windows
            return;
        //Do a version check. The fix is needed in Python 3.4+
        if (SiddhiAPICoreProxy.getPythonVersionMajor() == 3 && SiddhiAPICoreProxy.getPythonVersionMinor() >= 4)
            new PyThreadFix().fix();
    }
}
