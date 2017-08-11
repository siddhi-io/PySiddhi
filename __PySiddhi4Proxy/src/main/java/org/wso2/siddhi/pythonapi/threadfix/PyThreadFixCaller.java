package org.wso2.siddhi.pythonapi.threadfix;

import org.wso2.siddhi.pythonapi.proxy.core.SiddhiAPICoreProxy;

/**
 * Created by Madhawa on 8/11/2017.
 */

/**
 * A wrapper on ThreadFix Call
 */
public class PyThreadFixCaller {

    private PyThreadFixCaller(){}

    /**
     * Invokes threadFix if required
     */
    public static void fix(){
        if(System.getProperty("os.name").toLowerCase().startsWith("windows")) //No Threadfix for Windows
            return;
        //Do a version check. The fix is needed in Python 3.4+
        if(SiddhiAPICoreProxy.getPythonVersionMajor() == 3 && SiddhiAPICoreProxy.getPythonVersionMinor() >= 4)
            new PyThreadFix().fix();
    }
}
