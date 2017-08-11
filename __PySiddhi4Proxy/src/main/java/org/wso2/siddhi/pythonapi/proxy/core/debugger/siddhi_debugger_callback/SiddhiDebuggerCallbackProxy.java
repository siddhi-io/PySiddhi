package org.wso2.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger_callback;

import org.apache.log4j.Logger;
import org.wso2.siddhi.core.debugger.SiddhiDebugger;
import org.wso2.siddhi.core.debugger.SiddhiDebuggerCallback;
import org.wso2.siddhi.core.event.ComplexEvent;
import org.wso2.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger_callback.event_polling.EventQueue;
import org.wso2.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger_callback.event_polling.QueuedEvent;
import org.wso2.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger.QueryTerminalProxy;
import org.wso2.siddhi.pythonapi.proxy.core.stream.output.callback.stream_callback.StreamCallbackProxy;
import org.wso2.siddhi.pythonapi.threadfix.PyThreadFix;
import org.wso2.siddhi.pythonapi.threadfix.PyThreadFixCaller;


/**
 * Created by madhawa on 5/27/17.
 */
public class SiddhiDebuggerCallbackProxy implements SiddhiDebuggerCallback {
    private static final Logger log = Logger.getLogger(StreamCallbackProxy.class);

    private EventQueue debuggerEventQueue = new EventQueue();

    public EventQueue getEventQueue(){
        return this.debuggerEventQueue;
    }

    public void debugEvent(ComplexEvent complexEvent, String queryName, SiddhiDebugger.QueryTerminal queryTerminal, SiddhiDebugger siddhiDebugger) {
        PyThreadFixCaller.fix();

        log.info("Debug Event Called");
        debuggerEventQueue.addEvent(QueuedEvent.createDebugEvent(complexEvent,queryName,new QueryTerminalProxy(queryTerminal),siddhiDebugger));
    }

    @Override
    public void finalize() throws java.lang.Throwable {
        //We need to inform Python when Java GC collects so it can remove the references held
        log.info("Java GC Collection");
        debuggerEventQueue.addEvent(QueuedEvent.createGCEvent());
    }
}
