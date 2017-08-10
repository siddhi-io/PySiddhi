package org.wso2.siddhi.pythonapi.proxy.core.event.complex_event;

import org.wso2.siddhi.core.event.ComplexEvent;
import org.wso2.siddhi.pythonapi.DataWrapProxy;

/**
 * Created by madhawa on 6/1/17.
 */
public class ComplexEventProxy {
    public DataWrapProxy[] getOutputData(ComplexEvent target){
        return DataWrapProxy.wrapArray(target.getOutputData());
    }

    public void setOutputData(ComplexEvent target, DataWrapProxy data, int index){
        target.setOutputData(data.getData(),index);
    }
}
