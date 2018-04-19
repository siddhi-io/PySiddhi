# PySiddhi

The scope of this project is to develop a Python Wrapper on Siddhi Library. The Python wrapper would support Siddhi 4.x. A REST Client is also developed to interact with WSO2 Stream Processor 4.x.x.

This was developed as a project for Google Summer of Code 2017 Program.


Features
-----
- [x] Basic functionalities of Siddhi 4.x.x
- [x] Wrapper on Siddhi Debugger
- [x] Support to Siddhi Extensions Loading
- [x] Rest Client on WSO2 SP 4.x.x - Siddhi App Management
- [x] Rest Client on WSO2 SP 4.x.x Event Simulator
- [x] Deployment wheels

Install PySiddhi from python package manager(pip)
----
Install pre-requisites mentioned in Installing the Library from Source section.

```
pip install pysiddhi4
```

Installing the Library from Source
-----
1. Install following pre-requisites.
- Linux
    -
    - Python 2.7 or 3.x
    - Requests (`sudo pip install requests`)
    - Cython (`sudo pip install cython`)
    - Pyjnius (`sudo pip install pyjnius`)
    - Future (`sudo pip install future`)
    - Python Developer Package (`sudo apt-get install python-dev python3-dev python-dev`)
    - libboost for Python (`sudo apt-get install libboost-python-dev`)
    - Maven and Java 8
    - g++ and other development tools
      - `sudo apt-get install build-essential g++ autotools-dev libicu-dev build-essential libbz2-dev libboost-all-dev`
- macOS
    -
    - install brew
    - install python using brew
    - Requests (`sudo pip install requests`)
    - Cython (`sudo pip install cython`)
    - Pyjnius (`sudo pip install pyjnius`)
    - Future (`sudo pip install future`)
    - boost for python (`brew install boost`)


- Download siddhi-sdk release from https://github.com/wso2/siddhi-sdk/releases and set the SIDDHISDK_HOME as a           environment variable(`export SIDDHISDK_HOME="<path-to-siddhi-sdk>"`)
- For use of WSO2 SP 4.x.x Client functionality, it is required to have a WSO2 SP 4.x.x worker instance up and running.
    (Refer _Running the Tests_ section for installation details)
2. Install using Setup.py.
    - Clone the branch from GitHub Repository.
    - Navigate to project root and run `sudo pip install .`

Use the Library using Python
-----
* Siddhi on python
    ```python
    from PySiddhi4.core.SiddhiManager import SiddhiManager
    sm = SiddhiManager()
    ....
    sm.shutdown()
    ```

* Refer Tests to get more familiar with library functionality.

Running the Tests
-----
1. Install pre-requisites mentioned in `Installing the Library from Source` section.
2. Compile Java Libraries.
    - Navigate to `PySiddhi/PySiddhi4Proxy` and run `mvn clean install`
3. For running tests on WSO2 SP 4.x.x , it is required to have WSO2 SP 4.x.x worker instance up and running.
    - Obtain WSO2 SP 4.x.x binary distribution from https://github.com/wso2/product-sp/releases/.
    - Extract `wso2sp-4.x.x.zip` to a suitable location (say `SP_HOME`).
    - Navigate to `SP_Home/bin/` and run `sh worker.sh`(in windows run worker.bat).
4. Run the tests cases in `PySiddhi/Tests` directory

* If mvn clean install throws errors, check the paths provided for imports of Python3 Developer Headers

Creating deployment wheel (for Linux)
-----
1. Install pre-requisites mentioned in `Installing the Library from Source` section.
2. Delete directory `build` if exist.
3. Goto source root and run `python setup.py bdist_wheel --plat-name manylinux1_x86_64`

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
Siddhi is a java library that listens to events from data streams, detects complex conditions described via a Streaming SQL language, and triggers actions. It performs both Stream Processing and Complex Event Processing.

Further information on above products are available in the links below.
- Siddhi 4.0 Library (In Development Version)
    - GitHub - https://github.com/wso2/siddhi
- WSO2 Stream Processor 4.x.x (In Development Version)
    - GitHub - https://github.com/wso2/product-sp
    - Documentation - https://docs.wso2.com/display/SP400/Quick+Start+Guide


Contributors
-----
* __Madhawa Vidanapathirana__
   - Email: madhawavidanapathirana@gmail.com
   - Organization: University of Moratuwa

How to Contribute
-----   
* Please report issues at
     <a target="_blank" href="https://github.com/wso2/PySiddhi/issues">GitHub Issue Tracker</a>.

* Send your contributions as pull requests to <a target="_blank" href="https://github.com/wso2/PySiddhi/tree/master">master branch</a>.

Contact us
-----

* Post your questions with the <a target="_blank" href="http://stackoverflow.com/search?q=siddhi">"Siddhi"</a> tag in <a target="_blank" href="http://stackoverflow.com/search?q=siddhi">Stackoverflow</a>.

* Siddhi developers can be contacted via the mailing lists:

    Developers List   : [dev@wso2.org](mailto:dev@wso2.org)

    Architecture List : [architecture@wso2.org](mailto:architecture@wso2.org)

Support
-----

   * We are committed to ensuring support for this extension in production. Our unique approach ensures that all support leverages our open development methodology and is provided by the very same engineers who build the technology.

   * For more details and to take advantage of this unique opportunity contact us via <a target="_blank" href="http://wso2.com/support?utm_source=gitanalytics&utm_campaign=gitanalytics_Jul17">http://wso2.com/support/</a>.
__Developer Mail Group__: dev@wso2.org
