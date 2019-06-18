/*
 * Copyright (c) 2017, WSO2 Inc. (http://www.wso2.org) All Rights Reserved.
 *
 * WSO2 Inc. licenses this file to you under the Apache License,
 * Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied. See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

package io.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger_callback;

import org.apache.log4j.Logger;
import io.siddhi.core.debugger.SiddhiDebugger;
import io.siddhi.core.debugger.SiddhiDebuggerCallback;
import io.siddhi.core.event.ComplexEvent;
import io.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger_callback.event_polling.EventQueue;
import io.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger_callback.event_polling.QueuedEvent;
import io.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger.QueryTerminalProxy;
import io.siddhi.pythonapi.proxy.core.stream.output.callback.stream_callback.StreamCallbackProxy;
import io.siddhi.pythonapi.threadfix.PyThreadFixCaller;

/**
 * Proxy on io.siddhi.core.debugger.SiddhiDebuggerCallback
 */
public class SiddhiDebuggerCallbackProxy implements SiddhiDebuggerCallback {
    private static final Logger log = Logger.getLogger(StreamCallbackProxy.class);

    private EventQueue debuggerEventQueue = new EventQueue();

    public EventQueue getEventQueue() {
        return this.debuggerEventQueue;
    }

    public void debugEvent(ComplexEvent complexEvent, String queryName,
                           SiddhiDebugger.QueryTerminal queryTerminal, SiddhiDebugger siddhiDebugger) {
        PyThreadFixCaller.fix();
        log.info("Debug Event Called");
        debuggerEventQueue.addEvent(QueuedEvent.createDebugEvent(complexEvent, queryName,
                new QueryTerminalProxy(queryTerminal), siddhiDebugger));
    }

    @Override
    public void finalize() throws java.lang.Throwable {
        //We need to inform Python when Java GC collects so it can remove the references held
        log.info("Java GC Collection");
        debuggerEventQueue.addEvent(QueuedEvent.createGCEvent());
    }
}
