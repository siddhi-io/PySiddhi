package org.wso2.siddhi.pythonapi;

import com.sun.org.apache.xpath.internal.operations.Bool;

import java.util.logging.Logger;

/**
 * Created by madhawa on 6/1/17.
 */
public class DataWrapProxy {
    /**
     * Wrapper on Data sent between Python and Java. This wrapper is needed due to following reasons
     * - Python doesnt support long datatype
     * - Pyjnius require uniform data type objects in arrays
     */
    /**
     * Note: The approach taken here causes loss of precision in Double and Loss of range in Long.
     * TODO: Look for a better implementation of Double and Long, without loss of precision and range
     */
    private Object data;
    public DataWrapProxy(int data)
    {
        this.data = data;
    }
    public DataWrapProxy(boolean data)
    {
        this.data = data;
    }
    public DataWrapProxy(float data)
    {
        this.data = data;
    }
    public DataWrapProxy(String data)
    {
        this.data = data;
    }
    public DataWrapProxy(int data, boolean isLong)
    {
        this.data = (long)data;
    }

    public DataWrapProxy(int data, boolean isLong, boolean isNull)
    {
        if(isNull)
        {
            this.data = null;
        }
    }

    public DataWrapProxy(float data, boolean isLong, boolean isNull, boolean isDouble)
    {
        if(isDouble)
        {
            this.data = (double)data;
        }
    }

    public boolean isNull(){
        return this.data == null;
    }
    public boolean isLong(){
        return this.data instanceof Long;
    }
    public boolean isDouble(){
        return this.data instanceof Double;
    }
    public boolean isInt(){
        return this.data instanceof Integer;
    }
    public boolean isFloat(){
        return this.data instanceof Float;
    }
    public boolean isBoolean(){
        return this.data instanceof Boolean;
    }
    public boolean isString(){
        return this.data instanceof String;
    }

    public Object getData()
    {
        return data;
    }

    public static DataWrapProxy[] wrapArray(Object[] data)
    {
        DataWrapProxy[] results = new DataWrapProxy[data.length];
        for(int i = 0;i < data.length; i++)
            results[i] = DataWrapProxy.wrap(data[i]);
        return results;
    }

    public static DataWrapProxy wrap(Object data) {
        if(data == null)
            return new DataWrapProxy(null);
        if(data instanceof Integer)
            return new DataWrapProxy((Integer)data);
        else if(data instanceof Long)
            //TODO: Check removal of Integer casting here
            return new DataWrapProxy((int)(long)(Long) data,true);
        else if(data instanceof String)
            return new DataWrapProxy((String)data);
        else if(data instanceof Float)
            return new DataWrapProxy((Float)data);
        else if(data instanceof Boolean)
            return new DataWrapProxy((Boolean)data);
        else if(data instanceof Double)
            return new DataWrapProxy((float)(double)(Double)data,false,false,true);

        Logger.getLogger(DataWrapProxy.class.getName()).info("Unsupported Data Type: " +  data.getClass().toString());
        throw new RuntimeException("Unsupported Data Type");
    }

    public static Object[] unwrapArray(DataWrapProxy[] data)
    {
        Object[] results = new Object[data.length];
        for(int i = 0;i < data.length; i++)
            results[i] = data[i].getData();
        return results;
    }


}
