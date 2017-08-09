package org.wso2.siddhi.pythonapi.proxy.core.query.output.callback.query_callback;

import org.wso2.siddhi.core.event.Event;

/**
 * Created by madhawa on 3/18/17.
 */
public interface ReceiveCallbackProxy {
    void receive(long l, Event[] events, Event[] events1);
    void gc();

}
