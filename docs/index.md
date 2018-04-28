# PySiddhi

***PySiddhi*** is a Python wrapper for [Siddhi](https://wso2.github.io/siddhi/). Which can listens to events from data streams, detects complex conditions
described via a ***Streaming SQL language***, and triggers actions. It performs both ***Stream Processing*** and 
***Complex Event Processing*** on streaming data. Its Siddhi core is written in Java library. 

- PySiddhi4 wraps [Siddhi 4](https://wso2.github.io/siddhi/)
- PySiddhi4 includes a REST Client for [WSO2 Stream Processor(SP) 4.x.x](https://wso2.com/analytics).

## Content

* Introduction and Quick Demo (this page)
* [Installation Guide](Installation-Guide.md)
* [Run PySiddhi4](Run-PySiddhi4.md)
* [Debug PySiddhi4](Debugging-Siddhi-Queries.md)
* [Advanced Concepts of PySiddhi](Using-Siddhi-from-Python.md)
* Using PySiddhi REST Client to Manage WSO2 Stream Processor
    * [Demo Managing Siddhi Apps on WSO2 SP](Quick-Demo-(SP4).md)
    * [APIs to Manage Siddhi App](Siddhi-App-Management-of-WSO2-SP-4.md)
    * [APIs to Simulate Events](Event-Simulator-of-SP-4.md)

## Installation

PySiddhi4 can be installed using pip.

```
pip install pysiddhi4
```

For detail insulation and prerequisite refer section on [Installation Guide](Installation-Guide). 

## Quick Demo
Following is a quick demo of how to use PySiddhi4. For comprehensive demo please refer [Quick-Demo-PySiddhi4](Run-PySiddhi4.md)

**Step 1** - Define filter using Siddhi Query.

```python
siddhiManager = SiddhiManager()
# Siddhi Query to filter events with volume less than 150 as output
siddhiApp = "define stream cseEventStream (symbol string, price float, volume long);" + \
            "@info(name = 'query1') " + \
            "from cseEventStream[volume < 150] " + \
            "select symbol, price " + \
            "insert into outputStream;"

# Generate runtime
siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(siddhiApp)
```
For more details on Siddhi Query Language, refer [Siddhi Query Language Guide](https://wso2.github.io/siddhi/).

**Step 2** - Define a listener for filtered events.

```python
# Add listener to capture output events
class QueryCallbackImpl(QueryCallback):
    def receive(self, timestamp, inEvents, outEvents):
        PrintEvent(timestamp, inEvents, outEvents)
siddhiAppRuntime.addCallback("query1",QueryCallbackImpl())
```
**Step 3** - Test filter query using sample input events.

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

```python
siddhiManager.shutdown()
```

## Contribution 

_PySiddhi is initiated by a project for Google Summer of Code 2017 Program._

Contributed by: __Madhawa Vidanapathirana__ </br>
Email: madhawavidanapathirana@gmail.com </br>
Organization: University of Moratuwa, Sri Lanka.

## How to Contribute
* Report issues at <a target="_blank" href="https://github.com/wso2/PySiddhi/issues">GitHub Issue Tracker</a>.
* Feel free to try out the <a target="_blank" href="https://github.com/wso2/PySiddhi">PySiddhi source code</a> and send your contributions as pull requests to the <a target="_blank" href="https://github.com/wso2/PySiddhi/tree/master">master branch</a>. 
 
## Contact us 
 * Post your questions with the <a target="_blank" href="http://stackoverflow.com/search?q=siddhi">"Siddhi"</a> tag in <a target="_blank" href="http://stackoverflow.com/search?q=siddhi">Stackoverflow</a>. 
 * For more details and support contact us via <a target="_blank" href="http://wso2.com/support?utm_source=gitanalytics&utm_campaign=gitanalytics_Jul17">http://wso2.com/support/</a>
 
## Support 
* We are committed to ensuring support for [Siddhi](https://wso2.github.io/siddhi/) (with its <a target="_blank" href="https://wso2.github.io/siddhi/extensions/">extensions</a>) and <a target="_blank" href="http://wso2.com/analytics?utm_source=gitanalytics&utm_campaign=gitanalytics_Jul17">WSO2 Stream Processor</a> from development to production. 
* Our unique approach ensures that all support leverages our open development methodology and is provided by the very same engineers who build the technology. 
* For more details and to take advantage of this unique opportunity, contact us via <a target="_blank" href="http://wso2.com/support?utm_source=gitanalytics&utm_campaign=gitanalytics_Jul17">http://wso2.com/support/</a>. 
