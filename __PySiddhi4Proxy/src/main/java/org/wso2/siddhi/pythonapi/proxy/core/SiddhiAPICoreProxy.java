package org.wso2.siddhi.pythonapi.proxy.core;

import org.wso2.siddhi.core.SiddhiAppRuntime;
import org.wso2.siddhi.core.SiddhiManager;
import org.wso2.siddhi.pythonapi.proxy.core.query.output.callback.query_callback.QueryCallbackProxy;
import org.wso2.siddhi.pythonapi.proxy.core.stream.output.callback.stream_callback.StreamCallbackProxy;

/**
 * Created by madhawa on 5/21/17.
 */
public class SiddhiAPICoreProxy {
    /**
     * Initiates a new Siddhi Manager and return instance to Python API
     * @return new SiddhiManager Instance
     */

    public SiddhiAPICoreProxy(int versionMajor, int versionMinor)
    {
        SiddhiAPICoreProxy.setPythonVersionMajor(versionMajor);
        SiddhiAPICoreProxy.setPythonVersionMinor(versionMinor);
    }

    public SiddhiManager initSiddhiManager(){
        //new PyThreadFix().fix();
        return new SiddhiManager();
    }

    private static int python_version_major = -1;
    private static int python_version_minor = -1;

    public void addSiddhiAppRuntimeQueryCallback(SiddhiAppRuntime siddhiAppRuntime, String name, final QueryCallbackProxy queryCallbackProxy)
    {
        siddhiAppRuntime.addCallback(name, queryCallbackProxy);

    }


    public void addSiddhiAppRuntimeStreamCallback(SiddhiAppRuntime siddhiAppRuntime, String name, final StreamCallbackProxy streamCallbackProxy)
    {
        siddhiAppRuntime.addCallback(name, streamCallbackProxy);

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
