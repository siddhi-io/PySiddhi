# PySiddhi

*You are currently in branch for PySiddhi 3.x*

The scope of this project is to develop a Python Wrapper on Siddhi CEP Library. Additionally, the Python API would support Siddhi Configuration on WSO2 Data Analytics Server (DAS). The Python wrapper would support Siddhi 3.1, Siddhi 4.0, WSO2 DAS 3.1 and WSO2 DAS 4.0.

This is currently a work in progress, as a project for Google Summer of Code 2017 Program.

*Note: Currently the API is configured with __Siddhi CEP 3.1.0__ (in branch 3.1) and __Siddhi CEP 4.0.0-M33__  (in branch 4.0) for __Python 2.7.x__ and __Python 3.x__*

Project Goals
-----
1) Develop a Python Wrapper on Siddhi Java Library 3.1 and 4.0.
2) Extend Python API in (1) to support interactions with WSO2 Data Analytics Server 3.1 and 4.0.
3) Testing, Documentation and Deployment

Current Progress
-----
Currently, the project is in very early stage with discussions on the scope.
- [x] Basic features of Siddhi CEP Core 3.1 and 4.0
- [x] Wrapper on Siddhi Debugger (for Siddhi 4.0 only)
- [x] Support to Siddhi Extensions Loading
- [x] Unit Tests

Installing the Library from Source
-----
1. Install following pre-requisites.
    - Python 2.7 or 3.x
    - Cython (`sudo apt-get install cython`)
    - Pyjnius (`sudo pip install pyjnius`)
    - Future (`sudo pip install future`)
    - Python Developer Package (`sudo apt-get install python-dev python3-dev python-dev`)
    - libboost for Python (`sudo apt-get install libboost-python-dev`)
    - Maven and Java 8
    - g++ and other development tools
      - `sudo apt-get install build-essential g++ autotools-dev libicu-dev build-essential libbz2-dev libboost-all-dev`

2. Install using Setup.py.
    - Clone the relevant branch (3.1 or 4.0) from GitHub Repository.
    - Navigate to project root and run `sudo pip3 install .`

3. Use the Library using Python.
    - For Siddhi CEP 3.1
    ```python
    from PySiddhi3.core.SiddhiManager import SiddhiManager
    sm = SiddhiManager()
    ....
    sm.shutdown()
    ```

    - For Siddhi CEP 4.0.0-M33
    ```python
    from PySiddhi3.core.SiddhiManager import SiddhiManager
    sm = SiddhiManager()
    ....
    sm.shutdown()
    ```
    *Refer Tests to get more familiar with library functionality.

Running the Tests
-----
1. Install pre-requisites mentioned in `Installing the Library from Source` section.
2. Compile Java Libraries.
    - Navigate to `PySiddhi/__PySiddhi3Proxy` and run `mvn install`
    - Navigate to `SiddhiCEPPythonAPI/SiddhiCEP4/ProxyClasses/SiddhiCEP4Proxy` and run `mvn clean install`
    - Run the tests cases in `PySiddhi/Tests/PySiddhi3Tests` directory

*If build.sh throws errors, check the paths provided for imports of Python3 Developer Headers

Background
-----
Siddhi is a Query Language and a Library for Realtime Streaming Complex Event Processing developed by WSO2 Inc. Siddhi CEP is currently used in WSO2 Data Analytics Server, an Enterprise Level Open Source Data Analytics Solution.

Further information on above products are available in the links below.

- Siddhi 4.0 Library (In Development Version)
    - GitHub - https://github.com/wso2/siddhi
- Siddhi 3.1 Library (Stable Release)
    - GitHub - https://github.com/wso2/siddhi/tree/3.1.x
    - Documentation - https://docs.wso2.com/display/CEP420/SiddhiQL+Guide+3.1
- WSO2 Data Analytics Server 4.0 (In Development Version)
    - GitHub - https://github.com/wso2/product-das
    - Documentation - https://docs.wso2.com/display/DAS400/Quick+Start+Guide
- WSO2 Data Analytics Server 3.1 (Stable Release)
    - Release - http://wso2.com/smart-analytics
    - GitHub - https://github.com/wso2/product-das/tree/release-3.1.0-RC3
    - Documentation - https://docs.wso2.com/display/DAS310/WSO2+Data+Analytics+Server+Documentation

Contact
-----
Madhawa - madhawavidanapathirana@gmail.com

#GSoC2017 #WSO2
