Siddhi Debugger is a new addition to Siddhi Library in version 4.0. The following features of Siddhi 4.0 Debugger has been exposed to Python using this API.
* Siddhi Debugger Callbacks
* Siddhi Breakpoints (Acquiring and Releasing)
* Querying details on Siddhi QueryState
* Debugging Multi-threaded Siddhi Apps

# Breakpoints and Siddhi Debugger Callbacks
Using Siddhi Debugger, it is possible to break the query execution on occurrences of designated events (input or output events) and analyze the state of the query. Placing a breakpoint would cause Siddhi Debugger Callback to be triggered whenever a breakpoint is reached. The following code snippet demonstrates a basic usage of Siddhi Debugger.

```python

# Obtain siddhi debugger from Siddhi App Runtime.
siddhiDebugger = siddhiAppRuntime.debug()

# Place a breakpoint.
siddhiDebugger.acquireBreakPoint("query 1", SiddhiDebugger.QueryTerminal.IN)

# Setup a callback to receive debug events.
class SiddhiDebuggerCallbackImpl(SiddhiDebuggerCallback):
    def debugEvent(self, event, queryName,queryTerminal, debugger):
        logging.info("Query: " + queryName + ":" + queryTerminal.name)
        logging.info(event)

        # Do assertions on event and check for special cases.

        # Obtain next debuggable element of breakpoint.
        # Alternatively can call debugger.play() to ignore pending
        # debuggable elements and continue from breakpoint.
        debugger.next()

# Assign the debugger callback
siddhiDebugger.setDebuggerCallback(SiddhiDebuggerCallbackImpl())

# Send test inputs using inputHandler
inputHandler.send(["WSO2", 50.0, 60])
inputHandler.send(["WSO2", 70.0, 40])
```

For the complete code on above example and many other examples refer [Siddhi Debugger Tests](https://github.com/wso2/PySiddhi/blob/master/Tests/SiddhiCoreTests/TestDebugger.py).