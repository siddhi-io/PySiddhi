# Run PySiddhi Client with WSO2 Stream Processor

PySiddhi REST Client enable you to manage [WSO2 Stream Processor](https://wso2.com/analytics) using Python.
The detail information on PySiddhi client APIs refer:  
* [Client APIs to Manage Siddhi App](Siddhi-App-Management-of-WSO2-SP-4.0)
* [Client APIs to Simulate Events](Event-Simulator-WSO2-SP-4.0)

The following steps demonstrate how PySiddhi SP Client can manage Siddhi Apps running on WSO2 Stream Processor 4.x.x. 
This code retrieves the list of Siddhi Apps published in WSO2SP.

**Step 1:** Setup WSO2 Stream Processor
  - Obtain WSO2 SP 4.x.x binary distribution from [https://wso2.com/analytics](https://wso2.com/analytics).
  - Extract `wso2sp-4.x.x.zip` to a suitable location (say `SP_HOME`).
  - Navigate to `SP_Home/bin/` and run `sh worker.sh`.

**Step 2:** Load Python Imports.
```python
from PySiddhi.sp.SPClient import SPClient
```
**Step 3:** Connect to WSO2 SP via REST API using the SiddhiApp Management Client.
```python
spPythonClient = SPClient('http://localhost:9090')
siddhiAppManagementClient = spPythonClient.getSiddhiAppManagementClient()
```
**Step 4:** Obtain list of Siddhi Apps published in WSO2 SP.
```python
print(siddhiAppManagementClient.listSiddhiApps())
```
**Sample Outputs**
```log
['TestSiddhiApp']
```
**Cleanup**

Stop WSO2 SP by sending `Ctrl+C` to terminal window running `worker.sh`. This would shutdown the SP server