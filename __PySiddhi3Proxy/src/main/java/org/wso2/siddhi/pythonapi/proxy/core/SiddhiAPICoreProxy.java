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

package org.wso2.siddhi.pythonapi.proxy.core;

import org.wso2.siddhi.core.ExecutionPlanRuntime;
import org.wso2.siddhi.core.SiddhiManager;
import org.wso2.siddhi.pythonapi.proxy.core.query.output.callback.query_callback.QueryCallbackProxy;
import org.wso2.siddhi.pythonapi.proxy.core.stream.output.callback.stream_callback.StreamCallbackProxy;

public class SiddhiAPICoreProxy {
    /**
     * Initiates a new Siddhi Manager and return instance to Python API
     *
     * @return new SiddhiManager Instance
     */

    public SiddhiAPICoreProxy(int versionMajor, int versionMinor) {
        SiddhiAPICoreProxy.setPythonVersionMajor(versionMajor);
        SiddhiAPICoreProxy.setPythonVersionMinor(versionMinor);
    }

    public SiddhiManager initSiddhiManager() {
        //new PyThreadFix().fix();
        return new SiddhiManager();
    }

    private static int python_version_major = -1;
    private static int python_version_minor = -1;

    public void addExecutionPlanRuntimeQueryCallback(ExecutionPlanRuntime executionPlanRuntime, String name,
                                                     final QueryCallbackProxy queryCallbackProxy) {
        executionPlanRuntime.addCallback(name, queryCallbackProxy);


    }

    public void addExecutionPlanRuntimeStreamCallback(ExecutionPlanRuntime executionPlanRuntime, String name,
                                                      final StreamCallbackProxy streamCallbackProxy) {
        executionPlanRuntime.addCallback(name, streamCallbackProxy);

    }

    public static int getPythonVersionMajor() {
        return python_version_major;
    }

    public static void setPythonVersionMajor(int python_version_major) {
        SiddhiAPICoreProxy.python_version_major = python_version_major;
    }

    public static int getPythonVersionMinor() {
        return python_version_minor;
    }

    public static void setPythonVersionMinor(int python_version_minor) {
        SiddhiAPICoreProxy.python_version_minor = python_version_minor;
    }
}
