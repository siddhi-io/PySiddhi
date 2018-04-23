The following example demonstrates a streaming events filter to detect stock records with volume less than 150. This code is written using Siddhi 4.0 via PySiddhi4.

```python
from PySiddhi4.DataTypes.LongType import LongType
from PySiddhi4.core.SiddhiManager import SiddhiManager
from PySiddhi4.core.query.output.callback.QueryCallback import QueryCallback
from PySiddhi4.core.util.EventPrinter import PrintEvent
from time import sleep

siddhiManager = SiddhiManager()
# Siddhi Query to filter events with volume less than 150 as output
siddhiApp = "define stream cseEventStream (symbol string, price float, volume long); " + \
"@info(name = 'query1') from cseEventStream[volume < 150] select symbol,price insert into outputStream;"

# Generate runtime
siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(siddhiApp)

# Add listener to capture output events
class QueryCallbackImpl(QueryCallback):
    def receive(self, timestamp, inEvents, outEvents):
        PrintEvent(timestamp, inEvents, outEvents)
siddhiAppRuntime.addCallback("query1",QueryCallbackImpl())

# Retrieving input handler to push events into Siddhi
inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")

# Starting event processing
siddhiAppRuntime.start()

# Sending events to Siddhi
inputHandler.send(["IBM",700.0,LongType(100)])
inputHandler.send(["WSO2", 60.5, LongType(200)])
inputHandler.send(["GOOG", 50, LongType(30)])
inputHandler.send(["IBM", 76.6, LongType(400)])
inputHandler.send(["WSO2", 45.6, LongType(50)])

# Wait for response
sleep(0.1)

```
Above example is comprehensively described bellow.

**Initialization** 

- Initialize the Library and Imports

Add [this file](https://github.com/wso2/PySiddhi/blob/master/log4j.xml) to working directory in order to enable log4j logging. Log4j is used by PrintEvent to generate output.

```python
from PySiddhi4.DataTypes.LongType import LongType
from PySiddhi4.core.SiddhiManager import SiddhiManager
from PySiddhi4.core.query.output.callback.QueryCallback import QueryCallback
from PySiddhi4.core.util.EventPrinter import PrintEvent
from time import sleep
```

**Step 1** - Define filter using Siddhi Query
```python
siddhiManager = SiddhiManager()
# Siddhi Query to filter events with volume less than 150 as output
siddhiApp = "define stream cseEventStream (symbol string, price float, volume long); " + \
"@info(name = 'query1') from cseEventStream[volume < 150] select symbol,price insert into outputStream;"

# Generate runtime
siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(siddhiApp)
```
For more details on Siddhi Query Language, refer [Siddhi Query Language Guide](https://wso2.github.io/siddhi/documentation/siddhi-4.0/) in WSO2 Docs.

**Step 2** - Define a listener for filtered events.
```python
# Add listener to capture output events
class QueryCallbackImpl(QueryCallback):
    def receive(self, timestamp, inEvents, outEvents):
        PrintEvent(timestamp, inEvents, outEvents)
siddhiAppRuntime.addCallback("query1",QueryCallbackImpl())
```
**Step 3** - Test filter using sample input events
```python
# Retrieving input handler to push events into Siddhi
inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")

# Starting event processing
siddhiAppRuntime.start()

# Sending events to Siddhi
inputHandler.send(["IBM",700.0,LongType(100)])
inputHandler.send(["WSO2", 60.5, LongType(200)])
inputHandler.send(["GOOG", 50, LongType(30)])
inputHandler.send(["IBM", 76.6, LongType(400)])
inputHandler.send(["WSO2", 45.6, LongType(50)])

# Wait for response
sleep(0.1)
```
**Output**

The 3 events with volume less than 150 are printed in log.
```log
INFO  EventPrinter - Events{ @timestamp = 1497708406678, inEvents = [Event{timestamp=1497708406678, id=-1, data=[IBM, 700.0], isExpired=false}], RemoveEvents = null }
INFO  EventPrinter - Events{ @timestamp = 1497708406685, inEvents = [Event{timestamp=1497708406685, id=-1, data=[GOOG, 50], isExpired=false}], RemoveEvents = null }
INFO  EventPrinter - Events{ @timestamp = 1497708406687, inEvents = [Event{timestamp=1497708406687, id=-1, data=[WSO2, 45.6], isExpired=false}], RemoveEvents = null }
```

**Clean Up** - Remember to shutdown the Siddhi Manager when your done.
```
siddhiManager.shutdown()
```