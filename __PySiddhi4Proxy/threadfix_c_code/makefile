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