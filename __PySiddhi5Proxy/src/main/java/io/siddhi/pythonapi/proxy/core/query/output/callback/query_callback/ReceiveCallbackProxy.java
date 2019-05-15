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

package io.siddhi.pythonapi.proxy.core.query.output.callback.query_callback;

import io.siddhi.core.event.Event;

/**
 * Proxy callback on receive method of io.siddhi.core.query.output.callback.QueryCallback
 */
public interface ReceiveCallbackProxy {
    void receive(long l, Event[] events, Event[] events1);

    void gc();

}
