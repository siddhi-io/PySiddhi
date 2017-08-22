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

package org.wso2.siddhi.pythonapi.proxy.core.stream.input.input_handler;

import org.wso2.siddhi.core.stream.input.InputHandler;
import org.wso2.siddhi.pythonapi.DataWrapProxy;

import java.util.HashMap;

/**
 * Proxy wrapper on org.wso2.siddhi.core.stream.input.InputHandler
 */
public class InputHandlerProxy {
    /**
     * Sends input via InputHandler
     *
     * @param target target InputHandler
     * @param data   data fed into InputHandler
     * @throws InterruptedException
     */
    public void send(InputHandler target, DataWrapProxy[] data) throws InterruptedException {
        target.send(DataWrapProxy.unwrapArray(data));

        HashMap<String, Object> hm = new HashMap<String, Object>();

    }
}
