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


package io.siddhi.pythonapi.proxy.core;

import io.siddhi.core.SiddhiAppRuntime;
import io.siddhi.core.SiddhiManager;
import io.siddhi.pythonapi.proxy.core.query.output.callback.query_callback.QueryCallbackProxy;
import io.siddhi.pythonapi.proxy.core.stream.output.callback.stream_callback.StreamCallbackProxy;

public class SiddhiAPICoreProxy {
    /**
     * Instatiate API
     *
     * @param versionMajor Major Version of Python
     * @param versionMinor Minor Version of Python
     */
    public SiddhiAPICoreProxy(int versionMajor, int versionMinor) {
        SiddhiAPICoreProxy.setPythonVersionMajor(versionMajor);
        SiddhiAPICoreProxy.setPythonVersionMinor(versionMinor);
    }

    /**
     * Initiates a new Siddhi Manager and return instance to Python API
     *
     * @return new SiddhiManager Instance
     */
    public SiddhiManager initSiddhiManager() {
        return new SiddhiManager();
    }

    private static int python_version_major = -1;
    private static int python_version_minor = -1;

    /**
     * Register a SiddhiAppRuntimeQueryCallback with SiddhiAppRuntime
     *
     * @param siddhiAppRuntime
     * @param name
     * @param queryCallbackProxy
     */
    public void addSiddhiAppRuntimeQueryCallback(SiddhiAppRuntime siddhiAppRuntime, String name,
                                                 final QueryCallbackProxy queryCallbackProxy) {
        siddhiAppRuntime.addCallback(name, queryCallbackProxy);
    }

    /**
     * Register a SiddhiAppRuntimeStreamCallback with SiddhiAppRuntime
     *
     * @param siddhiAppRuntime
     * @param name
     * @param queryCallbackProxy
     */
    public void addSiddhiAppRuntimeStreamCallback(SiddhiAppRuntime siddhiAppRuntime, String name,
                                                  final StreamCallbackProxy streamCallbackProxy) {
        siddhiAppRuntime.addCallback(name, streamCallbackProxy);

    }

    /**
     * Retrieve Major Python Version
     *
     * @return
     */
    public static int getPythonVersionMajor() {
        return python_version_major;
    }

    /**
     * Sets Major Python Version
     *
     * @param python_version_major
     */
    public static void setPythonVersionMajor(int python_version_major) {
        SiddhiAPICoreProxy.python_version_major = python_version_major;
    }

    /**
     * Retrieve Major Python Version
     *
     * @return
     */
    public static int getPythonVersionMinor() {
        return python_version_minor;
    }

    /**
     * Sets Major Python Version
     *
     * @param python_version_minor
     */
    public static void setPythonVersionMinor(int python_version_minor) {
        SiddhiAPICoreProxy.python_version_minor = python_version_minor;
    }
}
