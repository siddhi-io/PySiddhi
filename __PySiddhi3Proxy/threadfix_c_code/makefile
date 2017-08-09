# use g++ compiler
CC = g++

CFLAGS = -shared -fPIC

# define JAVA_HOME here
JAVAHOME = ${JAVA_HOME}

#define python interpreter home here
PYTHONHOME = /usr/include/python3.5

CP = cp

#Find include files
INCLUDES = -I "$(JAVAHOME)/include" -I "$(JAVAHOME)/include/linux" -I "$(PYTHONHOME)"

# build target details
TARGET_SOURCE_NAME = org_wso2_siddhi_pythonapi_threadfix_PyThreadFix
TARGET_OUTPUT_NAME = liborg_wso2_siddhi_pythonapi_threadfix_pythreadfix
TARGET_INSTALL_NAME = liborg_wso2_siddhi_pythonapi_threadfix_pythreadfix
TARGET = threadfix

all: install

$(TARGET_OUTPUT_NAME).so: $(TARGET_SOURCE_NAME).c $(TARGET_SOURCE_NAME).h
	@echo "Building Target..."
	$(CC) $(CFLAGS) $(INCLUDES) -o $(TARGET_OUTPUT_NAME).so $(TARGET_SOURCE_NAME).c
	@echo

install: $(TARGET_OUTPUT_NAME).so
	@echo "Copying Target to Root..."
	$(CP) $(TARGET_OUTPUT_NAME).so ../../$(TARGET_INSTALL_NAME).so
	@echo

clean:
	$(RM) $(TARGET_OUTPUT_NAME).so