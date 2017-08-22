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

package org.wso2.siddhi.pythonapi;

import java.util.logging.Logger;


/**
 * Wrapper on Data sent between Python and Java. This wrapper is needed due to following reasons
 * - Python doesnt support long datatype
 * - Pyjnius require uniform data type objects in arrays
 *
 * Note: The approach taken here causes loss of precision in Double and Loss of range in Long.
 * TODO: Look for a better implementation of Double and Long, without loss of precision and range
 */
public class DataWrapProxy {

    private Object data;

    /**
     * Constructor for integer wrapping
     *
     * @param data
     */
    public DataWrapProxy(int data) {
        this.data = data;
    }

    /**
     * Constructor for boolean wrapping
     *
     * @param data
     */
    public DataWrapProxy(boolean data) {
        this.data = data;
    }

    /**
     * Constructor for float wrapping
     *
     * @param data
     */
    public DataWrapProxy(float data) {
        this.data = data;
    }


    /**
     * Constructor for String wrapping
     *
     * @param data
     */
    public DataWrapProxy(String data) {
        this.data = data;
    }


    /**
     * Constructor for long wrapping
     *
     * @param data
     * @param isLong
     */
    public DataWrapProxy(int data, boolean isLong) {
        this.data = (long) data;
    }

    /**
     * Constructor for null wrapping
     *
     * @param data
     * @param isLong
     * @param isNull
     */
    public DataWrapProxy(int data, boolean isLong, boolean isNull) {
        if (isNull) {
            this.data = null;
        }
    }

    /**
     * Constructor for double wrapping
     *
     * @param data
     * @param isLong
     * @param isNull
     * @param isDouble
     */
    public DataWrapProxy(float data, boolean isLong, boolean isNull, boolean isDouble) {
        if (isDouble) {
            this.data = (double) data;
        }
    }

    /**
     * Retrieve whether wrapped data is null
     *
     * @return
     */
    public boolean isNull() {
        return this.data == null;
    }

    /**
     * Retrieve whether wrapped data is long
     *
     * @return
     */
    public boolean isLong() {
        return this.data instanceof Long;
    }

    /**
     * Retrieve whether wrapped data is Double
     *
     * @return
     */
    public boolean isDouble() {
        return this.data instanceof Double;
    }

    /**
     * Retrieve whether wrapped data is Int
     *
     * @return
     */
    public boolean isInt() {
        return this.data instanceof Integer;
    }

    /**
     * Retrieve whether wrapped data is Float
     *
     * @return
     */
    public boolean isFloat() {
        return this.data instanceof Float;
    }

    /**
     * Retrieve whether wrapped data is boolean
     *
     * @return
     */
    public boolean isBoolean() {
        return this.data instanceof Boolean;
    }

    /**
     * Retrieve whether wrapped data is String
     *
     * @return
     */
    public boolean isString() {
        return this.data instanceof String;
    }

    /**
     * Retrieve wrapped data
     *
     * @return
     */
    public Object getData() {
        return data;
    }

    /**
     * Wrap data array
     *
     * @param data
     * @return
     */
    public static DataWrapProxy[] wrapArray(Object[] data) {
        DataWrapProxy[] results = new DataWrapProxy[data.length];
        for (int i = 0; i < data.length; i++)
            results[i] = DataWrapProxy.wrap(data[i]);
        return results;
    }

    /**
     * Wraps data item
     *
     * @param data data to be wrapped
     * @return
     */
    public static DataWrapProxy wrap(Object data) {
        if (data == null)
            return new DataWrapProxy(null);
        if (data instanceof Integer)
            return new DataWrapProxy((Integer) data);
        else if (data instanceof Long)
            //TODO: Check removal of Integer casting here
            return new DataWrapProxy((int) (long) (Long) data, true);
        else if (data instanceof String)
            return new DataWrapProxy((String) data);
        else if (data instanceof Float)
            return new DataWrapProxy((Float) data);
        else if (data instanceof Boolean)
            return new DataWrapProxy((Boolean) data);
        else if (data instanceof Double)
            return new DataWrapProxy((float) (double) (Double) data, false, false, true);

        Logger.getLogger(DataWrapProxy.class.getName()).info("Unsupported Data Type: "
                + data.getClass().toString());
        throw new RuntimeException("Unsupported Data Type");
    }


    /**
     * Unwraps wrapped data item.
     *
     * @param data wrappedData
     * @return
     */
    public static Object[] unwrapArray(DataWrapProxy[] data) {
        Object[] results = new Object[data.length];
        for (int i = 0; i < data.length; i++)
            results[i] = data[i].getData();
        return results;
    }


}
