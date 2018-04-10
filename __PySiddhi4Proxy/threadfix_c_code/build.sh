#!/usr/bin/env bash
echo "Compiling C++ Code used for fixing threading issue"
echo "Invoking G++ Compiler"

if [["$OSTYPE" == "darwin"*]]; then
    g++ -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/darwin" -I "$PYTHONHOME" -shared -fPIC -o liborg_wso2_siddhi_pythonapi_threadfix_pythreadfix.so org_wso2_siddhi_pythonapi_threadfix_PyThreadFix.c
elif [["$OSTYPE" == "linux-gnu"]]; then
    g++ -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/linux" -I "$PYTHONHOME" -shared -fPIC -o liborg_wso2_siddhi_pythonapi_threadfix_pythreadfix.so org_wso2_siddhi_pythonapi_threadfix_PyThreadFix.c
fi

echo "Copying output library to ../../../../SiddhiCEP4"
cp liborg_wso2_siddhi_pythonapi_threadfix_pythreadfix.so ../../../liborg_wso2_siddhi_pythonapi_threadfix_pythreadfix.so
echo "All is well!"