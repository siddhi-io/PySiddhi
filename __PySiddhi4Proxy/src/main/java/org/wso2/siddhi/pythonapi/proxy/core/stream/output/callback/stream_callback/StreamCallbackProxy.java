package org.wso2.siddhi.pythonapi.proxy.core.stream.output.callback.stream_callback;

import org.apache.log4j.Logger;
import org.wso2.siddhi.core.event.Event;
import org.wso2.siddhi.core.stream.output.StreamCallback;
import org.wso2.siddhi.pythonapi.threadfix.PyThreadFix;
import org.wso2.siddhi.pythonapi.threadfix.PyThreadFixCaller;

/**
 * Created by madhawa on 5/26/17.
 */
public class StreamCallbackProxy extends StreamCallback {
    private ReceiveCallbackProxy receiveCallback = null;
    public void setReceiveCallback(ReceiveCallbackProxy value){
        this.receiveCallback = value;
    }
    private static final Logger log = Logger.getLogger(StreamCallbackProxy.class);

    public void receive(Event[] events) {
        PyThreadFixCaller.fix();

        this.receiveCallback.receive(events);
        //log.info("Event Received - Java");
    }

    @Override
    public void finalize() throws java.lang.Throwable {
        //We need to inform Python when Java GC collects so it can remove the references held
        log.info("Java GC Collection");
        this.receiveCallback.gc();
    }
}
