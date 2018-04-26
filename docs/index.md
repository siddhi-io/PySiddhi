
Siddhi is a java library that listens to events from data streams, detects complex conditions described via a ***Streaming SQL language***, and triggers actions. It performs both ***Stream Processing*** and ***Complex Event Processing***.


The Siddhi Library is originally written in Java 8.0. ***PySiddhi*** is a Python wrapper on Siddhi Java Library.

- Siddhi 4 is wrapped by PySiddhi4.

PySiddhi4 includes a REST Client for WSO2 Stream Processor(SP) 4.x.x.

*Note: PySiddhi API is initiated by a project for Google Summer of Code 2017 Program.*

Content
---
* Introduction (this page)
* [Installation Guide](Installation-Guide.md)
* Full Quick Demo
    * [For Siddhi 4](Quick-Demo-(PySiddhi4).md)
    * [For WSO2 SP 4](Quick-Demo-(DAS-4.0))
* [Using Siddhi from Python](Using-Siddhi-from-Python)
* WSO2 Stream Processor 4 REST Client
    * [Siddhi App Management using Python Client](Siddhi-App-Management-of-WSO2-DAS-4.0)
    * [Using Event Simulator](Event-Simulator-WSO2-DAS-4.0)
* [Debugging Siddhi Queries](Debugging-Siddhi-Queries-(Siddhi-4.0)) 

## Quick Demo
Following is a quick demo of how to use PySiddhi4. For comprehensive demo please refer to [this link](Quick-Demo-(PySiddhi4).md)

**Step 1** - Define filter using Siddhi Query

```python
siddhiManager = SiddhiManager()
# Siddhi Query to filter events with volume less than 150 as output
siddhiApp = "define stream cseEventStream (symbol string, price float, volume long); " + \
"@info(name = 'query1') from cseEventStream[volume < 150] select symbol,price insert into outputStream;"

# Generate runtime
siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(siddhiApp)
```
For more details on Siddhi Query Language, refer [Siddhi Query Language Guide](https://wso2.github.io/siddhi/) in WSO2 Docs.

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

# Installation
PySiddhi can be installed as a Python Library from Source or can be download the python wheel using pip 

Refer [Build and Instaling from source](Installation-Guide) for installation prerequisites and other details. 
#### Installing PySiddhi4 from binary
```
pip install pysiddhi4
```
