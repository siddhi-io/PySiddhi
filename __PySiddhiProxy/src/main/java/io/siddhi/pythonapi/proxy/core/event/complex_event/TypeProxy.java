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

package io.siddhi.pythonapi.proxy.core.event.complex_event;

import io.siddhi.core.event.ComplexEvent;

/**
 * Proxy on type of ComplexEvent
 */
public class TypeProxy {
    public ComplexEvent.Type CURRENT() {
        return ComplexEvent.Type.CURRENT;
    }

    public ComplexEvent.Type EXPIRED() {
        return ComplexEvent.Type.EXPIRED;
    }

    public ComplexEvent.Type TIMER() {
        return ComplexEvent.Type.TIMER;
    }

    public ComplexEvent.Type RESET() {
        return ComplexEvent.Type.RESET;
    }

    private ComplexEvent.Type enclosedValue = ComplexEvent.Type.CURRENT;

    public TypeProxy() {
        //Constructor let open to allow access of CURRENT, EXPIRED, TIMER and RESET (because Pyjnius doesn't
        // support class level methods)
    }

    public TypeProxy(ComplexEvent.Type enclosedValue) {
        this.enclosedValue = enclosedValue;
    }

    public ComplexEvent.Type getValue() {
        return this.enclosedValue;
    }

    public boolean isValueCurrent() {
        return this.enclosedValue == CURRENT();
    }

    public boolean isValueExpired() {
        return this.enclosedValue == EXPIRED();
    }

    public boolean isValueTimer() {
        return this.enclosedValue == TIMER();
    }

    public boolean isValueReset() {
        return this.enclosedValue == RESET();
    }
}
