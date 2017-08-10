package org.wso2.siddhi.pythonapi.proxy.core.debugger.siddhi_debugger;

import org.wso2.siddhi.core.debugger.SiddhiDebugger;

/**
 * Created by madhawa on 5/26/17.
 */
public class QueryTerminalProxy {
    public SiddhiDebugger.QueryTerminal IN(){return SiddhiDebugger.QueryTerminal.IN;}
    public SiddhiDebugger.QueryTerminal OUT(){return SiddhiDebugger.QueryTerminal.OUT;}

    private SiddhiDebugger.QueryTerminal enclosedValue = SiddhiDebugger.QueryTerminal.IN;

    public QueryTerminalProxy(){
        //Constructor let open to allow access of IN and OUT methods from Python (because Pyjnius doesn't support class level methods)
    }
    public QueryTerminalProxy(SiddhiDebugger.QueryTerminal enclosedValue){
        this.enclosedValue = enclosedValue;
    }

    public SiddhiDebugger.QueryTerminal getValue(){
        return this.enclosedValue;
    }

    public boolean isValueIn(){
        return this.enclosedValue == IN();
    }

    public boolean isValueOut(){
        return this.enclosedValue == OUT();
    }
}
