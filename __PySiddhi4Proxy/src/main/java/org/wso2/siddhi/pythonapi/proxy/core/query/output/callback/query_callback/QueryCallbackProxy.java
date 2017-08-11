package org.wso2.siddhi.pythonapi.proxy.core.query.output.callback.query_callback;

import org.apache.log4j.Logger;
import org.wso2.siddhi.core.event.Event;
import org.wso2.siddhi.core.query.output.callback.QueryCallback;
import org.wso2.siddhi.pythonapi.threadfix.PyThreadFixCaller;

/**
 * Created by madhawa on 5/21/17.
 */
public class QueryCallbackProxy extends QueryCallback {
    private ReceiveCallbackProxy receiveCallback = null;

    public void setReceiveCallback(ReceiveCallbackProxy value){
        this.receiveCallback = value;
    }


    private static final Logger log = Logger.getLogger(QueryCallbackProxy.class);
    public void receive(long timestamp, Event[] inEvents, Event[] ouEvents) {
        PyThreadFixCaller.fix();

        if(this.receiveCallback != null)
            this.receiveCallback.receive(timestamp,inEvents,ouEvents);


    }

    @Override
    public void finalize() throws java.lang.Throwable {
        //We need to inform Python when Java GC collects so it can remove the references held
        log.info("Java GC Collection");
        this.receiveCallback.gc();
    }
}
