/*
 * Copyright (c) 2016, WSO2 Inc. (http://www.wso2.org) All Rights Reserved.
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

package org.wso2.siddhi.pythonapi.proxy.core.event.event;

import org.wso2.siddhi.core.event.ComplexEvent;
import org.wso2.siddhi.core.event.Event;
import org.wso2.siddhi.pythonapi.DataWrapProxy;

/**
 * Proxy on org.wso2.siddhi.core.event.Event
 */
public class EventProxy {
    public Event createEvent(long timeStamp, DataWrapProxy[] data) {
        return new Event(timeStamp, DataWrapProxy.unwrapArray(data));
    }

    public DataWrapProxy[] getData(Event target) {
        return DataWrapProxy.wrapArray(target.getData());
    }

    public DataWrapProxy getDataItem(Event target, int index) {
        Object data = target.getData(index);
        return DataWrapProxy.wrap(data);
    }

    public void setData(Event target, DataWrapProxy[] data) {
        target.setData(DataWrapProxy.unwrapArray(data));
    }

    public void makeExpired(Event target) {
        target.setIsExpired(true);
    }

    public void makeUnExpired(Event target) {
        target.setIsExpired(false);
    }


}
