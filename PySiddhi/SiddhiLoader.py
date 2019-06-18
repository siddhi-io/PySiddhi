# Copyright (c) 2017, WSO2 Inc. (http://www.wso2.org) All Rights Reserved.
#
# WSO2 Inc. licenses this file to you under the Apache License,
# Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

import logging
import os

import sys

import PySiddhi

# Instantiate Global Variables
siddhi_api_core = None
siddhi_api_core_inst = None

_java_method = None
_PythonJavaClass = None
_JavaClass = None

def addExtensionPath():
    '''
    Adds an Extension to Siddhi. Should be called prior to importing any Siddhi Libraries.
    :param class_path: Path to Jar File. Wild Card (*) directory selection is accepted
    :return: 
    '''
    siddhi_home = os.getenv("SIDDHISDK_HOME")
    class_path = os.path.join(siddhi_home, "lib", "*")
    if "siddhi_api_configured" in globals():
        raise Exception("Cannot add extensions after loading library.")

    if not "extensions" in globals():
        globals()["extensions"] = []

    globals()["extensions"].append(class_path)


def _resumeLibrary():
    '''
    Resumes values of global variables from backup
    :return: 
    '''
    if not "siddhi_api_configured" in globals():
        logging.info("Premature library resume ignored")
        return

    # Resume Global variables values from backup
    global t_siddhi_api_core, t_siddhi_api_core_inst, t_java_method, t_PythonJavaClass, t_JavaClass
    global siddhi_api_core, siddhi_api_core_inst, _java_method, _PythonJavaClass, _JavaClass

    siddhi_api_core = t_siddhi_api_core
    siddhi_api_core_inst = t_siddhi_api_core_inst
    _java_method = t_java_method
    _PythonJavaClass = t_PythonJavaClass
    _JavaClass = t_JavaClass


# Resume global variables values from backup
_resumeLibrary()


def loadLibrary():
    '''
    Loads Siddi Library
    :return: 
    '''
    siddhi_home = os.getenv("SIDDHISDK_HOME")
    # Test whether Java Library is already loaded
    if "siddhi_api_configured" in globals():
        if globals()["siddhi_api_configured"] != 4:
            raise Exception("Unable to use multiple versions of Siddhi Library")
        # Resume global variables if already loaded
        _resumeLibrary()
        return

    # Add Java library to class path of jvm
    import jnius_config

    # NOTE: The following code-line is required on Linux Kernel 4.4.0-81-generic and above to avoid segmentation fault
    # at initialization of pyjnius
    jnius_config.add_options('-Xss1280k')

    jnius_config.add_options('-Djava.library.path=' + PySiddhi.root_path + "/__PySiddhiProxy")

    # Determine library class path
    class_paths = ['.', os.path.join(siddhi_home, 'lib', '*')]

    # Add Extensions
    if not "extensions" in globals():
        global extensions
        extensions = []

    for extension in extensions:
        class_paths.append(extension)

    jnius_config.set_classpath(*(tuple(class_paths)))

    # Mark API configured
    global siddhi_api_configured
    siddhi_api_configured = 4

    logging.info("Classpath Configured")

    # Load Pyjnius (Starts JVM)
    from jnius import autoclass, java_method, PythonJavaClass, JavaClass

    # Generate references and store in backup
    global t_siddhi_api_core, t_siddhi_api_core_inst, t_java_method, t_PythonJavaClass, t_JavaClass
    t_siddhi_api_core = autoclass("io.siddhi.pythonapi.proxy.core.SiddhiAPICoreProxy")
    t_siddhi_api_core_inst = t_siddhi_api_core(sys.version_info[0], sys.version_info[1])
    t_java_method = java_method
    t_PythonJavaClass = PythonJavaClass
    t_JavaClass = JavaClass

    # Resume references stored in backup
    _resumeLibrary()


def _loadType(type_name):
    loadLibrary()
    from jnius import autoclass
    return autoclass(type_name)


def _detachThread():
    loadLibrary()
    import jnius
    jnius.detach()
