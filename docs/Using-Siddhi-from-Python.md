# Advanced Concepts of PySiddhi

## Key Points
The PySiddhi API is a wrapper on Siddhi Java Library, exposing it's core features to Python. It is important to keep 
following points in mind when using PySiddhi API.

* __It is a wrapper. Not a port.__ - Whenever you use the PySiddhi API, the [Siddhi Java Library](https://github.com/wso2/siddhi) is loaded in background using Java Virtual Machine.
* __The wrapper is focused on functionality provided by [siddhi-core](https://github.com/wso2/siddhi/tree/master/modules/siddhi-core/src/main/java/org/wso2/siddhi/core)__ which is found in package `org.wso2.siddhi.core`. The future versions of API may have the ability to load Siddhi Extensions directly from Java Packages and use them in Siddhi Queries. However, the individual Java classes of extensions will not be wrapped. 
* __Only the classes that are required for API users are wrapped.__  Classes which are designed to be used by Siddhi Java Library for its internal work will not be wrapped. 
* __Python doesn't differentiate _Integer_ from _Long_. But Siddhi do.__ Python 3 does not differentiate _Integer_ and _Long_ Data Types. All Python _Integers_ fed into Siddhi (via _InputHandler_) are converted into Java _Integers_. To feed Java _Long_ to Siddhi (via _InputHandler_), use _[DataTypes.LongType](https://github.com/wso2/PySiddhi/blob/master/PySiddhi/DataTypes/LongType.py)_. All _Long_ outputs received from Siddhi (via callbacks) will also be converted to _DataTypes.LongType_.
  - Example: `inputHandler.send(["IBM",700.0,LongType(100)])`
* __Clean up everything when you are done.__ Remember to call *shutdown* of *SiddhiManager* and *SiddhiAppRuntime*.

# Java Siddhi to PySiddhi Mappings

The PySiddhi wrapper is focused on functionality provided by [siddhi-core](https://github.com/wso2/siddhi/tree/master/modules/siddhi-core/src/main/java/org/wso2/siddhi/core). 
The classes in Java package `org.wso2.siddhi.core` are mapped to `PySiddhi.core` using hand written logic. These are not an auto-generated. 
The follow table demonstrates major mappings of PySiddhi.

| Java Class    | Python Import       |
| ------------- |---------------------|
| [org.wso2.siddhi.core.SiddhiManager](https://github.com/wso2/siddhi/tree/master/modules/siddhi-core/src/main/java/org/wso2/siddhi/core/SiddhiManager.java) | ```from PySiddhi.core.SiddhiManager import SiddhiManager```|
| [org.wso2.siddhi.core.ExecutionPlanRuntime](https://github.com/wso2/siddhi/tree/master/modules/siddhi-core/src/main/java/org/wso2/siddhi/core/SiddhiAppRuntime.java) | ```from PySiddhi.core.SiddhiAppRuntime import SiddhiAppRuntime```|
| [org.wso2.siddhi.core.event.Event](https://github.com/wso2/siddhi/blob/master/modules/siddhi-core/src/main/java/org/wso2/siddhi/core/event/Event.java)| ```from PySiddhi.core.event.Event import Event```|
| [org.wso2.siddhi.core.event.ComplexEvent](https://github.com/wso2/siddhi/blob/master/modules/siddhi-core/src/main/java/org/wso2/siddhi/core/event/ComplexEvent.java)| ```from PySiddhi.core.event.ComplexEvent import ComplexEvent```|
| [org.wso2.siddhi.core.stream.input.InputHandler](https://github.com/wso2/siddhi/tree/master/modules/siddhi-core/src/main/java/org/wso2/siddhi/core/stream/input/InputHandler.java) | ```from PySiddhi.core.stream.input.InputHandler import InputHandler``` |
| [org.wso2.siddhi.core.stream.output.StreamCallback](https://github.com/wso2/siddhi/tree/master/modules/siddhi-core/src/main/java/org/wso2/siddhi/core/stream/output/StreamCallback.java) | ```from PySiddhi.core.stream.output.StreamCallback import StreamCallback```|
|[org.wso2.siddhi.core.query.output.callback.QueryCallback](https://github.com/wso2/siddhi/tree/master/modules/siddhi-core/src/main/java/org/wso2/siddhi/core/query/output/callback/QueryCallback.java)| ```from PySiddhi.core.query.output.callback.QueryCallback import QueryCallback``` |
|[org.wso2.siddhi.core.debugger.SiddhiDebugger](https://github.com/wso2/siddhi/blob/master/modules/siddhi-core/src/main/java/org/wso2/siddhi/core/debugger/SiddhiDebugger.java)|```from PySiddhi.core.debugger.SiddhiDebugger import SiddhiDebugger```|
|[org.wso2.siddhi.core.debugger.SiddhiDebuggerCallback](https://github.com/wso2/siddhi/blob/master/modules/siddhi-core/src/main/java/org/wso2/siddhi/core/debugger/SiddhiDebuggerCallback.java) | ```from PySiddhi.core.debugger.SiddhiDebuggerCallback import SiddhiDebuggerCallback``` |
|[org.wso2.siddhi.core.util.EventPrinter](https://github.com/wso2/siddhi/tree/master/modules/siddhi-core/src/main/java/org/wso2/siddhi/core/util/EventPrinter.java) | ```import PySiddhi.core.util.EventPrinter```|