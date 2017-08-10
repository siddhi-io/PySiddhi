package org.wso2.siddhi.pythonapi.proxy.core.event.event;

import org.wso2.siddhi.core.event.ComplexEvent;
import org.wso2.siddhi.core.event.Event;
import org.wso2.siddhi.pythonapi.DataWrapProxy;

/**
 * Created by madhawa on 6/16/17.
 */
public class EventProxy {
    public Event createEvent(long timeStamp, DataWrapProxy[] data)
    {
        return new Event(timeStamp,DataWrapProxy.unwrapArray(data));
    }

    public DataWrapProxy[] getData(Event target){
        return DataWrapProxy.wrapArray(target.getData());
    }

    public DataWrapProxy getDataItem(Event target,int index){
        Object data = target.getData(index);
        return DataWrapProxy.wrap(data);
    }

    public void setData(Event target, DataWrapProxy[] data){
        target.setData(DataWrapProxy.unwrapArray(data));
    }

    public void makeExpired(Event target)
    {
        target.setIsExpired(true);
    }

    public void makeUnExpired(Event target)
    {
        target.setIsExpired(false);
    }


}
