package org.wso2.siddhi.pythonapi.proxy.core.query.output.callback.query_callback;

import org.apache.log4j.Logger;
import org.wso2.siddhi.core.event.Event;
import org.wso2.siddhi.core.query.output.callback.QueryCallback;
import org.wso2.siddhi.pythonapi.proxy.core.stream.output.callback.stream_callback.StreamCallbackProxy;
import org.wso2.siddhi.pythonapi.threadfix.PyThreadFix;
//import org.wso2.siddhi.pythonapi.proxy.core.util.PyThreadFix;

/**
 * Created by madhawa on 5/21/17.
 */
public class QueryCallbackProxy extends QueryCallback {
    private ReceiveCallbackProxy receiveCallback = null;
    public void setReceiveCallback(ReceiveCallbackProxy value){
        this.receiveCallback = value;
    }
    private static final Logger log = Logger.getLogger(StreamCallbackProxy.class);
    public void receive(long timestamp, Event[] inEvents, Event[] ouEvents) {
        new PyThreadFix().fix();

        this.receiveCallback.receive(timestamp,inEvents,ouEvents);
    }

    @Override
    public void finalize() throws java.lang.Throwable {
        //We need to inform Python when Java GC collects so it can remove the references held
        log.info("Java GC Collection");
        this.receiveCallback.gc();
    }
}
