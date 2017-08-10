#include <jni.h>
#include <stdio.h>

#include <boost/python.hpp>

#include "org_wso2_siddhi_pythonapi_threadfix_PyThreadFix.h"

JNIEXPORT void JNICALL Java_org_wso2_siddhi_pythonapi_threadfix_PyThreadFix_fixThread(JNIEnv *env, jobject thisObj)
{

   PyGILState_STATE state;

   PyInterpreterState *istate = PyInterpreterState_Head();
   PyThreadState_New(istate);

   state = PyGILState_Ensure();
   PyGILState_Release(state);

   //printf("Thread issue fixed\n");

   return;
}
