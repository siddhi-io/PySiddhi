The following is a demo code on Siddhi App Management using PySiddhi4 SP Client. This code retrieves the list of Siddhi Apps published in WSO2 SP 4.0.

**Step 1** 

  - Obtain WSO2 SP 4.x.x binary distribution from [here](https://github.com/wso2/product-sp/releases/).
  - Extract `wso2sp-4.x.x.zip` to a suitable location (say `SP_HOME`).
  - Navigate to `SP_Home/bin/` and run `sh worker.sh`.

**Step 2** - Load Python Imports.
```python
from PySiddhi4.sp.SPClient import SPClient
```
**Step 3** - Connect to WSO2 SP 4.x.x via REST API and obtain SiddhiApp Management Client.
```python
spPythonClient = SPClient('http://localhost:9090')
siddhiAppManagementClient = spPythonClient.getSiddhiAppManagementClient()
```
**Step 4** - Obtain list of Siddhi Apps published in WSO2 DAS.
```python
print(siddhiAppManagementClient.listSiddhiApps())
```
**Receive Outputs**
```log
['TestSiddhiApp']
```
**Cleanup** - Stop WSO2 SP 4.x.x by sending Ctrl+C to terminal window running worker.sh. This would shutdown the SP server