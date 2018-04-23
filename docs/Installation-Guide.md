# Build and instaling PySiddhi4 from source

## Prerequisites
The current version is tested with Microsoft Windows and Unix/Linux based operating systems. 

The following dependencies should be installed prior to installation of library.

- **Linux**
    
    - Python 2.7 or 3.x
    - Cython (`sudo pip install cython`)
    - Python Developer Package (`sudo apt-get install python-dev python3-dev python-dev`)
    - libboost for Python (`sudo apt-get install libboost-python-dev`)
    - Maven and Java 8
    - g++ and other development tools
        (`sudo apt-get install build-essential g++ autotools-dev libicu-dev build-essential libbz2-dev libboost-all-dev`)

- **macOS**
    
    - Install brew
    - Install python using brew
    - Cython (`sudo pip install cython`)
    - boost for python (`brew install boost`)

- **Windows**

    - Install Python 
    - Install Visual Studio Build tools
    - Cython (`sudo pip install cython`)
    - Maven and Java 8

- Download siddhi-sdk release from [here](https://github.com/wso2/siddhi-sdk/releases) and set the SIDDHISDK_HOME as a           environment variable(`export SIDDHISDK_HOME="<path-to-siddhi-sdk>"`)
- For use of WSO2 SP 4.x.x Client functionality, it is required to have a WSO2 SP 4.x.x worker instance up and running.
    (Refer _Running the Tests_ section for installation details)
- Download siddhi-python-api-proxy-4-1.0.0.jar from [here](https://github.com/wso2/PySiddhi/releases) and copy to `<SIDDHISDK_HOME>/lib` directory

## Install PySiddhi4 from Online Code
Using the following PIP command, PySiddhi4 can be directly installed from online code available in GitHub.
```
pip install git+https://github.com/wso2/PySiddhi.git
```
*Note: In case of permission errors, use `sudo`*

## Install from Downloaded Code
Switch to the branch `master` for PySiddhi4.

Navigate to source code root and execute the following PIP command.
```
pip install .
```
*Note the period (.) at end of command. In case of permission errors, use `sudo`*

## Uninstall
If the library has been installed as explained above, it could be uninstalled using the following pip command.
```
pip uninstall pysiddhi4
```
