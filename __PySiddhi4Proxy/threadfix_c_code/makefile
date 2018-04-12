# ---------------------------------------------------------------------------
#  Copyright (c) 2017, WSO2 Inc. (http://www.wso2.org) All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# use g++ compiler
CC = g++

CFLAGS = -shared -fPIC -c

# define JAVA_HOME here
JAVAHOME = ${JAVA_HOME}

LINUX_PYTHON_PATH = /usr/include/python

MACOS_PYTHON_PATH = /usr/local/var/homebrew/linked/python/Frameworks/Python.framework/Versions/3.6/include/python3.6m

OS = ${shell uname}

CP = cp

#Find include files
INCLUDES_LINUX = -I "$(JAVAHOME)/include" -I "$(JAVAHOME)/include/linux" -I "$(LINUX_PYTHON_PATH)"

INCLUDES_MACOS = -I "$(JAVAHOME)/include" -I "$(JAVAHOME)/include/darwin" -I "$(MACOS_PYTHON_PATH)"




# build target details
TARGET_SOURCE_NAME = org_wso2_siddhi_pythonapi_threadfix_PyThreadFix
TARGET_OUTPUT_NAME = liborg_wso2_siddhi_pythonapi_threadfix_pythreadfix
TARGET_INSTALL_NAME = liborg_wso2_siddhi_pythonapi_threadfix_pythreadfix
TARGET = threadfix

all: install

$(TARGET_OUTPUT_NAME).so: $(TARGET_SOURCE_NAME).c $(TARGET_SOURCE_NAME).h
	@echo "Building Target..."
ifeq ($(OS), Darwin)
	$(CC) $(CFLAGS) $(INCLUDES_MACOS) -o $(TARGET_OUTPUT_NAME).so $(TARGET_SOURCE_NAME).c
else ifeq ($(OS), linux-gnu)
	$(CC) $(CFLAGS) $(INCLUDES_LINUX) -o $(TARGET_OUTPUT_NAME).so $(TARGET_SOURCE_NAME).c
endif
	@echo

install: $(TARGET_OUTPUT_NAME).so
	@echo "Copying Target to Root..."
	$(CP) $(TARGET_OUTPUT_NAME).so ../$(TARGET_INSTALL_NAME).so
	@echo

clean:
	$(RM) $(TARGET_OUTPUT_NAME).so