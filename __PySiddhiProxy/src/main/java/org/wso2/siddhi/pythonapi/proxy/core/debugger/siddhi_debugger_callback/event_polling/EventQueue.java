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

package org.wso2.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger_callback.event_polling;

import org.apache.log4j.Logger;
import org.wso2.siddhi.pythonapi.proxy.core.stream.output.callback.stream_callback.StreamCallbackProxy;

import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.Semaphore;

/**
 * Shared Queue of events between Java and Python. Used to pass Debug Events to Python from Java using polling.
 */
public class EventQueue {
    private Queue<QueuedEvent> queuedEvents = null;
    private Semaphore eventsBlock = null; //Used to block getQueuedEvents when no events are present
    private boolean blocked = false; //Indicates whether a blocked getQueuedEvents is pending

    /**
     * Instantiate a new EventQueue
     */
    public EventQueue() {
        this.queuedEvents = new ConcurrentLinkedQueue<QueuedEvent>();
        this.eventsBlock = new Semaphore(0);
        this.blocked = false;
    }

    private static final Logger log = Logger.getLogger(EventQueue.class);

    /**
     * Retrieve the next event in queue. Blocks if no events in queue.
     *
     * @return
     */
    public QueuedEvent getQueuedEvent() {

        if (queuedEvents.isEmpty()) {
            try {
                synchronized (this) {
                    this.blocked = true;
                }
                log.trace("Event Block Check");
                eventsBlock.acquire();
                log.trace("Event Block Acquired");
                synchronized (this) {
                    this.blocked = false;
                }
                log.trace("Block unset");
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        log.trace("Returning queued events");
        return queuedEvents.remove();
    }

    /**
     * Interrupts a pending blocking call to getQueuedEvent.
     * Interrupt should be used when SiddhiDebuggerCallback is changed to release the event processing thread
     * from blocking getQueuedEvent call
     */
    public void interrupt() {
        synchronized (this) {
            if (blocked) {
                eventsBlock.release();
                log.trace("Interrupt Released");
                this.blocked = false;
            }
        }
    }

    /**
     * Retrieve the next event in queue. Return null if no event.
     *
     * @return
     */
    public QueuedEvent getQueuedEventAsync() {
        if (queuedEvents.isEmpty())
            return null;

        return queuedEvents.remove();
    }

    /**
     * Adds an event to event queue.
     *
     * @param event Event to be added
     */
    public void addEvent(QueuedEvent event) {
        log.trace("Event Added");
        queuedEvents.add(event);
        synchronized (this) {
            if (blocked) {
                eventsBlock.release();
                this.blocked = false;
            }

        }
    }
}

