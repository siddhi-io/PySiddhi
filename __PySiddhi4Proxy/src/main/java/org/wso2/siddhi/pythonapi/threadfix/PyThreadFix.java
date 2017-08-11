
/**
 * Created by madhawa on 5/29/17.
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
    public void fix(){
        this.fixThread();
    }

    // Test Driver
    public static void main(String[] args) {
        new PyThreadFix().fixThread();  // invoke the native method
    }
}