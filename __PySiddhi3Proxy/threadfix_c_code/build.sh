echo "Compiling C++ Code used for fixing threading issue"
echo "Invoking G++ Compiler"
g++ -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/linux" -I "/usr/include/python3.5" -shared -fPIC -o liborg_wso2_siddhi_pythonapi_threadfix_pythreadfix.so org_wso2_siddhi_pythonapi_threadfix_PyThreadFix.c
echo "Copying output library to ../../../../SiddhiCEP3"
cp liborg_wso2_siddhi_pythonapi_threadfix_pythreadfix.so ../../../liborg_wso2_siddhi_pythonapi_threadfix_pythreadfix.so
echo "All is well!"