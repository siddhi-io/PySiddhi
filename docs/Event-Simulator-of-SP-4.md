# Event Simulation using PySiddhi Client

Following operations are supported by WSO2 Stream Processor 4 Event Simulator Client of PySiddhi4.

* Single Simulations
* Saving a simulation configuration
* Editing a simulation configuration
* Deleting a simulation configuration
* Retrieving a simulation configuration
* Uploading a CSV file
* Editing and uploaded CSV file
* Deleting an uploaded CSV file
* Pausing an event simulation
* Resuming an event simulation
* Stopping an event simulation

Refer [Documentation of WSO2 SP 4.0 Event simulator REST API](https://docs.wso2.com/display/SP400/Simulating+Events) for more details.

## Pre-requisites
1. Install _PySiddhi4_ by following [Installation Guide](Installation-Guide).
2. WSO2 SP 4.0 must be already installed and running. If not, follow the steps below.
  - Obtain WSO2 SP 4.x.x binary distribution from https://github.com/wso2/product-sp/releases.
  - Extract `wso2sp-4.x.x.zip` to a suitable location (say `SP_HOME`).
  - Navigate to `SP_Home/bin/` and run `sh worker.sh`.

## Supported API operations 

### Single Simulations
```python
from PySiddhi4.sp.SPClient import SPClient
from PySiddhi4.sp.EventSimulator.SingleSimulationConfiguration import SingleSimulationConfiguration

spPythonClient = SPClient('http://localhost:9090') # host URL of SP
eventSimulatorClient = spPythonClient.getEventSimulatorClient()

singleSimulationConfiguration = SingleSimulationConfiguration("TestSiddhiApp","FooStream",[None, 9, 45])

if eventSimulatorClient.simulateSingleEvent(singleSimulationConfiguration, username="admin", password="admin"):
    logging.info("Successfully Simulated Single Event")
```

### Saving a Simulation Configuration (Feed Simulation Configuration)
```python
from PySiddhi4.sp.SPClient import SPClient
from PySiddhi4.sp.EventSimulator.AttributeConfiguration import AttributeConfiguration
from PySiddhi4.sp.EventSimulator.FeedSimulationConfiguration import FeedSimulationConfiguration
from PySiddhi4.sp.EventSimulator.SimulationSource import SimulationSource

spPythonClient = SPClient('http://localhost:9090') # host URL of SP
eventSimulatorClient = spPythonClient.getEventSimulatorClient()

svr = FeedSimulationConfiguration("simulationPrimitive")
svr.properties.timestampStartTime = 1488615136958
svr.properties.timestampEndTime = None
svr.properties.noOfEvents = 8
svr.properties.timeInterval = 1000

sm1 = SimulationSource(simulationType=SimulationSource.Type.RANDOM_DATA_SIMULATION, streamName="FooStream", siddhiAppName="TestSiddhiApp", timestampInterval=5)

sm1.attributeConfiguration.append(AttributeConfiguration(AttributeConfiguration.Type.PRIMITIVE_BASED, length=10))
sm1.attributeConfiguration.append(AttributeConfiguration(AttributeConfiguration.Type.PRIMITIVE_BASED, min=35000, max=30000, precision=2))
sm1.attributeConfiguration.append(AttributeConfiguration(AttributeConfiguration.Type.PRIMITIVE_BASED, min=150, max=300))

svr.sources.append(sm1)

if eventSimulatorClient.saveSimulationFeedConfiguration(svr, username="admin", password="admin"):
    print("Successfully Saved Simulation Feed Configuration")
```

For more examples on Event Simulator, refer [EventSimulatorTests](https://github.com/wso2/PySiddhi/blob/master/Tests/SPTests/EventSimulatorTests.py).