package org.wso2.siddhi.pythonapi.proxy.core.stream.input.input_handler;

import org.wso2.siddhi.core.stream.input.InputHandler;
import org.wso2.siddhi.pythonapi.DataWrapProxy;

import java.util.HashMap;

/**
 * Created by madhawa on 6/1/17.
 */
public class InputHandlerProxy {
    public void send(InputHandler target, DataWrapProxy[] data) throws InterruptedException {
        target.send(DataWrapProxy.unwrapArray(data));

        HashMap<String,Object> hm = new HashMap<String, Object>();

    }
}
