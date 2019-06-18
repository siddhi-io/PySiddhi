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

package io.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger_callback.event_polling;

import org.apache.log4j.Logger;
import io.siddhi.core.debugger.SiddhiDebugger;
import io.siddhi.core.event.ComplexEvent;
import io.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger.QueryTerminalProxy;

/**
 * Event queued in EventQueue
 */
public class QueuedEvent {

    private static final Logger log = Logger.getLogger(QueuedEvent.class);

    /**
     * Type of event
     */
    public enum QueuedEventType {
        /**
         * SiddhiDebuggerCallback Debug event
         */
        DebugEvent,

        /**
         * Java Garbage Collection event. This is raised when the debugger callback is destroyed from JVM.
         */
        GCEvent
    }

    /**
     * Create a QueuedEvent informing a SiddhiDebuggerCallback debugEvent
     *
     * @param complexEvent  event parameter of debugEvent
     * @param queryName     queryName of debugEvent
     * @param queryTerminal queryTerminal of debugEvent
     * @param debugger      debugger of debugEvent
     * @return QueuedEvent on debugEvent
     */
    public static QueuedEvent createDebugEvent(ComplexEvent complexEvent, String queryName,
                                               QueryTerminalProxy queryTerminal, SiddhiDebugger debugger) {
        Object[] params = {complexEvent, queryName, queryTerminal, debugger};
        return new QueuedEvent(QueuedEventType.DebugEvent, params);
    }

    /**
     * Create a QueuedEvent informing JVM Garbage Collection SiddhiDebuggerCallback
     *
     * @return QueuedEvent on JVM Garbage Collection
     */
    public static QueuedEvent createGCEvent() {
        return new QueuedEvent(QueuedEventType.GCEvent, null);
    }

    /**
     * Creates a QueuedEvent of given type and parameters
     *
     * @param eventType  Type of event
     * @param parameters Arguments to be provided to event callback
     */
    public QueuedEvent(QueuedEventType eventType, Object[] parameters) {
        this.eventType = eventType;
        this.parameters = parameters;
    }

    private QueuedEventType eventType;
    private Object[] parameters;

    /**
     * Retrieve event type
     *
     * @return event type
     */
    public QueuedEventType getEventType() {
        return eventType;
    }

    /**
     * Retrieve whether the QueuedEvent is a SiddhiDebuggerCallback debugEvent
     *
     * @return true if QueuedEvent is a SiddhiDebuggerCallback debugEvent. Otherwise return false.
     */
    public boolean isDebugEvent() {
        return eventType == QueuedEventType.DebugEvent;
    }

    /**
     * Retrieve whether the QueuedEvent is a GCEvent
     *
     * @return true if QueuedEvent is a GCEvent. Otherwise return false.
     */
    public boolean isGCEvent() {
        return eventType == QueuedEventType.GCEvent;
    }

    /**
     * Obtain parameter at given index as a @ComplexEvent
     *
     * @param parameterId Argument Index
     * @return @ComplexEvent which is passed as @parameterId argument of callback
     */
    public ComplexEvent getComplexEvent(int parameterId) {
        return (ComplexEvent) parameters[parameterId];
    }

    /**
     * Obtain parameter at given index as a @String
     *
     * @param parameterId Argument Index
     * @return @String which is passed as @parameterId argument of callback
     */
    public String getString(int parameterId) {
        return (String) parameters[parameterId];
    }

    /**
     * Obtain parameter at given index as a @SiddhiDebugger
     *
     * @param parameterId Argument Index
     * @return @SiddhiDebugger which is passed as @parameterId argument of callback
     */
    public SiddhiDebugger getSiddhiDebugger(int parameterId) {
        return (SiddhiDebugger) parameters[parameterId];
    }

    /**
     * Obtain parameter at given index as a @QueryTerminalProxy
     *
     * @param parameterId Argument Index
     * @return @SiddhiDebugger which is passed as @parameterId argument of callback
     */
    public QueryTerminalProxy getQueryTerminal(int parameterId) {
        return (QueryTerminalProxy) parameters[parameterId];
    }
}
