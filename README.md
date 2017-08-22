# PySiddhi

*You are currently in branch for PySiddhi 3.x*

The scope of this project is to develop a Python Wrapper on Siddhi CEP Library. The Python wrapper would support Siddhi 3.1 and Siddhi 4.0.

This is currently a work in progress, as a project for Google Summer of Code 2017 Program.

*Note: Currently the API is configured with __Siddhi CEP 3.1.0__ (in branch 3.1) and __Siddhi CEP 4.0.0-M43-SNAPSHOT__  (in branch 4.0) for __Python 2.7.x__ and __Python 3.x__*

Project Goals
-----
1) Develop a Python Wrapper on Siddhi Java Library 3.1 and 4.0.
2) Testing, Documentation and Deployment

Current Progress
-----
- [x] Basic features of Siddhi CEP Core 3.1 and 4.0
- [x] Wrapper on Siddhi Debugger (for Siddhi 4.0 only)
- [x] Support to Siddhi Extensions Loading
- [x] Unit Tests
- [x] Wiki
- [x] Deployment wheels

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

    - For Siddhi CEP 4.0.0-M43-SNAPSHOT
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

*If mvn clean install throws errors, check the paths provided for imports of Python3 Developer Headers

Creating deployment wheel (for Linux)
-----
1. Install pre-requisites mentioned in `Installing the Library from Source` section.
2. Delete directory `build` if exist. 
3. Goto source root and run `python setup.py bdist_wheel --plat-name linux-x86_64`
4. Wheel file will be generated in `dist` directory.

_Note: You need to use linux operating system to build linux wheels._

Creating deployment wheel (for Windows)
-----
1. Install pre-requisites mentioned in `Installing the Library from Source` section.
2. Delete directory `build` if exist. 
3. Goto source root and run `python setup.py bdist_wheel --plat-name win-amd64`
4. Wheel file will be generated in `dist` directory.

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
