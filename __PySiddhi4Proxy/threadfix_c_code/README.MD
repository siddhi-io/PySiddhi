threadfix is used in Python 3.4+ to treat a threading related bug introduced in Python 3.4.
In Python 3.4+, if a callback is received from a non Python created thread to a Python program, it causes Python Interpreter to fail. 

The threadfix_c_code directory contains source code of Native Java Class org.wso2.siddhi.pythonapi.threadfix.PyThreadFix. The above mentioned issue is fixed by the code in method fixThread of Jave Native Class org.wso2.siddhi.pythonapi.threadfix.PyThreadFix. The fixthread method should be called prior to sending callback event from Java to Python in order to avoid the mentioned bug.
