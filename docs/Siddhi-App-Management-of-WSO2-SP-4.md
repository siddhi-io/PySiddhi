# Siddhi App Management using PySiddhi Client

Using _WSO2 SP Client_ in _PySiddhi_, following operations can be undertaken on _Siddhi App Management_ of _WSO2 SP 4.0_.
* List all Siddhi Apps.
* Retrieve Siddhi App using name.
* Retrieve Status of Siddhi App.
* Save a new Siddhi App in SP.
* Update a Siddhi App stored in SP.
* Delete a Siddhi App stored in SP.

## Pre-requisites
1. Install _PySiddhi_ by following [Installation Guide](Installation-Guide.md).
2. WSO2 SP 4.0 must be already installed and running. If not, follow the steps below.
  - Obtain WSO2 SP 4.x.x binary distribution from [https://wso2.com/analytics](https://wso2.com/analytics).
  - Extract `wso2sp-4.x.x.zip` to a suitable location (say `SP_HOME`).
  - Navigate to `SP_Home/bin/` and run `sh worker.sh`.

## Supported API operations 

### List all Siddhi Apps
```python
from PySiddhi.sp.SPClient import SPClient

spPythonClient = SPClient('http://localhost:9090') # host URL of SP
siddhiAppManagementClient = spPythonClient.getSiddhiAppManagementClient()

print(siddhiAppManagementClient.listSiddhiApps()) # prints a list of siddhi apps
```
### Retrieve Siddhi App using Name
```python
from PySiddhi.sp.SPClient import SPClient
spPythonClient = SPClient('http://localhost:9090') # host URL of SP
siddhiAppManagementClient = spPythonClient.getSiddhiAppManagementClient()

app = siddhiAppManagementClient.retrieveSiddhiApp("TestSiddhiApp", username=admin, password=admin)
print(app)
```

### Retrieve Siddhi App Status
```python
from PySiddhi.sp.SPClient import SPClient
spPythonClient = SPClient('http://localhost:9090') # host URL of SP
siddhiAppManagementClient = spPythonClient.getSiddhiAppManagementClient()

status = siddhiAppManagementClient.retrieveStatusSiddhiApp("TestSiddhiApp", username=admin, password=admin)
print (status) # prints status of siddhi app (active)
```

### Save new Siddhi App
```python
from PySiddhi.sp.SPClient import SPClient

spPythonClient = SPClient('http://localhost:9090') # host URL of SP
siddhiAppManagementClient = spPythonClient.getSiddhiAppManagementClient()

siddhiApp = "@App:name('TestSiddhiApp1') " 
                "define stream FooStream(symbol string, price float, volume long); " 
                "@source(type='inMemory', topic='symbol', @map(type='passThrough')) " 
                "define stream BarStream(symbol string, price float, volume long); "
                "from FooStream select symbol, price, volume insert into BarStream; "

if siddhiAppManagementClient.saveSiddhiApp(siddhiApp, username=admin, password=admin):
    print("Successfully saved!")
```
### Update a saved Siddhi App
```python
from PySiddhi.sp.SPClient import SPClient
from PySiddhi.sp.SiddhiAppManagement.SiddhiAppManagementClient import UpdateAppStatusResponse

spPythonClient = SPClient('http://localhost:9090') # Host URL of SP
siddhiAppManagementClient = spPythonClient.getSiddhiAppManagementClient()

siddhiApp = "@App:name('TestSiddhiApp1') " 
                "define stream FooStream (symbol string, price float, volume long); " 
                "@source(type='inMemory', topic='symbol', @map(type='passThrough')) " 
                "define stream BarStream (symbol string, price float, volume long); " 
                "from FooStream select symbol, price, volume insert into BarStream; "

result = siddhiAppManagementClient.updateSiddhiApp(siddhiApp, username=admin, password=admin)
if result.name == UpdateAppStatusResponse.savedNew.name:
    print("Saved new Siddhi App")
elif result.name == UpdateAppStatusResponse.updated.name:
    print("Updated saved Siddhi App")
```
### Delete a Siddhi App
```python
from PySiddhi.sp.SPClient import SPClient

spPythonClient = SPClient('http://localhost:9090') # host URL of SP
siddhiAppManagementClient = spPythonClient.getSiddhiAppManagementClient()

siddhiAppManagementClient.deleteSiddhiApp("TestSiddhiApp1", username=admin, password=admin) # returns True if successfully deleted
```