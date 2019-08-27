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

# define JAVA_HOME here
JAVAHOME = ${JAVA_HOME}

# Please provide the python path according to the python version of the machine
LINUX_PYTHON_PATH = /usr/include/python

# Please provide the python path according to the python version of the machine
MACOS_PYTHON_PATH = /usr/local/var/homebrew/linked/python/Frameworks/Python.framework/Versions/3.7/include/python3.7m

OS = ${shell uname}

CP = cp

ifeq ($(OS), Darwin)
CFLAGS = -shared -flat_namespace -undefined suppress -dynamiclib
INCLUDES = -I "$(JAVAHOME)/include" -I "$(JAVAHOME)/include/darwin" -I "$(MACOS_PYTHON_PATH)"
OUT_EXT = dylib
else
CFLAGS = -shared -fPIC
INCLUDES = -I "$(JAVAHOME)/include" -I "$(JAVAHOME)/include/linux" -I "$(LINUX_PYTHON_PATH)"
OUT_EXT = so
endif

# build target details
TARGET_SOURCE_NAME = io_siddhi_pythonapi_threadfix_PyThreadFix
TARGET_OUTPUT_NAME = libio_siddhi_pythonapi_threadfix_pythreadfix
TARGET_INSTALL_NAME = libio_siddhi_pythonapi_threadfix_pythreadfix
TARGET = threadfix

all: install

$(TARGET_OUTPUT_NAME).$(OUT_EXT): $(TARGET_SOURCE_NAME).c $(TARGET_SOURCE_NAME).h
	@echo "Building Target..."
	$(CC) $(CFLAGS) $(INCLUDES) -o $(TARGET_OUTPUT_NAME).$(OUT_EXT) $(TARGET_SOURCE_NAME).c
	@echo

install: $(TARGET_OUTPUT_NAME).$(OUT_EXT)
	@echo "Copying Target to Root..."
	$(CP) $(TARGET_OUTPUT_NAME).$(OUT_EXT) ../$(TARGET_INSTALL_NAME).$(OUT_EXT)
	@echo

clean:
	$(RM) $(TARGET_OUTPUT_NAME).$(OUT_EXT)
