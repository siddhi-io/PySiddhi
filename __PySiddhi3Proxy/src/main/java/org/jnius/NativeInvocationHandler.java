/*
* This file has been directly extracted from Project pyjnius (https://github.com/kivy/pyjnius/) by kivy which
* is subjected to following MIT License.
*
* Copyright (c) 2010-2017 Kivy Team and other contributors
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
* THE SOFTWARE.
*/

package org.jnius;

import org.apache.log4j.Logger;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;

public class NativeInvocationHandler implements InvocationHandler {
    static boolean DEBUG = false;
    private long ptr;

    public NativeInvocationHandler(long ptr) {
        this.ptr = ptr;
    }

    public Object invoke(Object proxy, Method method, Object[] args) {
        if (DEBUG) {
            Logger log = Logger.getLogger(NativeInvocationHandler.class);
            log.info("+ java:invoke(<proxy>, ");
            // don't call it, or recursive lookup/proxy will go!
            //log.info(proxy);
            //log.info(", ");
            log.info(method);
            log.info(", ");
            log.info(args);
            log.info(")");
        }

        Object ret = invoke0(proxy, method, args);

        if (DEBUG) {
            Logger log = Logger.getLogger(NativeInvocationHandler.class);
            log.info("+ java:invoke returned: ");
            log.info(ret);
        }

        return ret;
    }

    native Object invoke0(Object proxy, Method method, Object[] args);
}