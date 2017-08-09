package org.wso2.siddhi.pythonapi.proxy.core.event.complex_event;

import org.wso2.siddhi.core.event.ComplexEvent;

/**
 * Created by madhawa on 6/1/17.
 */
public class TypeProxy {
    public ComplexEvent.Type CURRENT(){return ComplexEvent.Type.CURRENT;}
    public ComplexEvent.Type EXPIRED(){return ComplexEvent.Type.EXPIRED;}
    public ComplexEvent.Type TIMER(){return ComplexEvent.Type.TIMER;}
    public ComplexEvent.Type RESET(){return ComplexEvent.Type.RESET;}

    private ComplexEvent.Type enclosedValue = ComplexEvent.Type.CURRENT;

    public TypeProxy(){
        //Constructor let open to allow access of CURRENT, EXPIRED, TIMER and RESET (because Pyjnius doesn't support class level methods)
    }
    public TypeProxy(ComplexEvent.Type enclosedValue){
        this.enclosedValue = enclosedValue;
    }

    public ComplexEvent.Type getValue(){
        return this.enclosedValue;
    }

    public boolean isValueCurrent(){
        return this.enclosedValue == CURRENT();
    }

    public boolean isValueExpired(){
        return this.enclosedValue == EXPIRED();
    }

    public boolean isValueTimer(){
        return this.enclosedValue == TIMER();
    }

    public boolean isValueReset(){
        return this.enclosedValue == RESET();
    }
}
