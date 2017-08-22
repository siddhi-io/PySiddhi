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

public class PyThreadFix {
    /**
     * PyThreadFix is used to fix a threading related issue in Python 3.4+.
     * Issue Description:
     *  In Python 3.4+, callbacks to Python from non Python created threads cause Python interpreter to crash.
     *  This could be fixed by calling a set of Python C API functions prior to sending the callback to Python.
     *  The set of Python C API functions required are called in fixThread native method.
     */
    static {
        System.loadLibrary("org_wso2_siddhi_pythonapi_threadfix_pythreadfix"); // Load native library at runtime
    }

    // The native fixThread method which has necessary C code to fix the threading issue
    private native void fixThread();

    /**
     * Invoke fixThread
     */
    public void fix() {
        this.fixThread();
    }

    // Test Driver
    public static void main(String[] args) {
        new PyThreadFix().fixThread();  // invoke the native method
    }
}