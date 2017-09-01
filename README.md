# PySiddhi

*You are currently in branch for PySiddhi 4.x*

The scope of this project is to develop a Python Wrapper on Siddhi CEP Library. The Python wrapper would support Siddhi 3.1 and Siddhi 4.0. A REST Client is also developed to interact with WSO2 Data Analytics Server (DAS) 4.0.

This is currently a work in progress, as a project for Google Summer of Code 2017 Program.

*Note: Currently the API is configured with __Siddhi CEP 3.1.0__ (in branch 3.x), __Siddhi CEP 4.0.0-M53__ (in branch master) and __WSO2 Data Analytics Server 4.0.0-M6__ (in branch master) for __Python 2.7.x__ and __Python 3.x__*

Project Goals
-----
1) Develop a Python Wrapper on Siddhi Java Library 3.1 and 4.0.
2) Extend the wrapper to support interactions with WSO2 DAS 4.0.
3) Testing, Documentation and Deployment

Current Progress
-----
- [x] Basic features of Siddhi CEP Core 3.1 and 4.0
- [x] Wrapper on Siddhi Debugger (for PySiddhi4 only)
- [x] Support to Siddhi Extensions Loading
- [x] Rest Client on WSO2 DAS 4.0 - Siddhi App Management (for PySiddhi4 only)
- [x] Rest Client on WSO2 DAS 4.0 Event Simulator (for PySiddhi4 only)
- [x] Unit Tests
- [x] Wiki
- [x] Deployment wheels

Installing the Library from Source
-----
1. Install following pre-requisites.
    - Python 2.7 or 3.x
    - Requests (`sudo apt-get install requests`)
    - Cython (`sudo apt-get install cython`)
    - Pyjnius (`sudo pip install pyjnius`)
    - Future (`sudo pip install future`)
    - Python Developer Package (`sudo apt-get install python-dev python3-dev python-dev`)
    - libboost for Python (`sudo apt-get install libboost-python-dev`)
    - Maven and Java 8
    - g++ and other development tools 
      - `sudo apt-get install build-essential g++ autotools-dev libicu-dev build-essential libbz2-dev libboost-all-dev`
    - For use of WSO2 DAS 4.0 Client functionality, it is required to have WSO2 DAS 4.0 installed and running.
    (Refer _Running the Tests_ section for installation details)
2. Install using Setup.py.
    - Clone the relevant branch (3.1 or 4.0) from GitHub Repository.
    - Navigate to project root and run `sudo pip install .`

3. Use the Library using Python.
    - For Siddhi CEP 3.1
    ```python
    from PySiddhi3.core.SiddhiManager import SiddhiManager
    sm = SiddhiManager()
    ....
    sm.shutdown()
    ```

    - For Siddhi CEP 4.0.0-M53
    ```python
    from PySiddhi4.core.SiddhiManager import SiddhiManager
    sm = SiddhiManager()
    ....
    sm.shutdown()
    ```
    *Refer Tests to get more familiar with library functionality.

Running the Tests
-----
1. Install pre-requisites mentioned in `Installing the Library from Source` section.
2. Compile Java Libraries.
    - Navigate to `PySiddhi/PySiddhi4Proxy` and run `mvn clean install`
3. For running tests on WSO2 DAS 4.0 Client, it is required to have WSO2 DAS 4.0 installed and running. 
    - Obtain WSO2 DAS 4.0-M6 binary distribution from https://github.com/wso2/product-das/releases/tag/v4.0.0-M6.
    - Extract `wso2das-4.0.0-SNAPSHOT.zip` to a suitable location (say `DAS_HOME`).
    - Navigate to `DAS_Home/bin/` and run `sh worker.sh`.
4. Run the tests cases in `PySiddhi/Tests` directory

*If mvn clean install throws errors, check the paths provided for imports of Python3 Developer Headers

Creating deployment wheel (for Linux)
-----
1. Install pre-requisites mentioned in `Installing the Library from Source` section.
2. Delete directory `build` if exist. 
3. Goto source root and run `python setup.py bdist_wheel --plat-name linux-x86_64`

_Note: You need to use linux operating system to build linux wheels._

Creating deployment wheel (for Windows)
-----
1. Install pre-requisites mentioned in `Installing the Library from Source` section.
2. Delete directory `build` if exist. 
3. Goto source root and run `python setup.py bdist_wheel --plat-name win-amd64`

_Note: You need to use Windows operating system to build Windows wheels._

Installing deployment wheel 
-----
1. Make sure all pre-requisites are met. 
(You may have to separately install cython using `pip install cython` if you use _virtual environments_)
2. Install python wheel using `pip install [path_to_wheel_file]`.

Background
-----
Siddhi is a Query Language and a Library for Realtime Complex Event Processing developed by WSO2 Inc. Siddhi CEP is currently used in WSO2 Data Analytics Server, an Enterprise Level Open Source Data Analytics Solution.

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

Contributors
-----
* __Madhawa Vidanapathirana__
   - Email: madhawavidanapathirana@gmail.com
   - Organization: University of Moratuwa

__Developer Mail Group__: dev@wso2.org
