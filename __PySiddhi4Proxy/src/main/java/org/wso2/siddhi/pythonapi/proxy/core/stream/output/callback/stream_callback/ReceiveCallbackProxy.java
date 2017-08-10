package org.wso2.siddhi.pythonapi.proxy.core.stream.output.callback.stream_callback;

import org.wso2.siddhi.core.event.Event;

/**
 * Created by madhawa on 5/26/17.
 */
public interface ReceiveCallbackProxy {
    void receive(Event[] events);
    void gc();
}
