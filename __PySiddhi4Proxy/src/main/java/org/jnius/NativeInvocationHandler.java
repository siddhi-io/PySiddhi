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

        if ( DEBUG ) {
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

        if ( DEBUG ) {
            Logger log = Logger.getLogger(NativeInvocationHandler.class);
            log.info("+ java:invoke returned: ");
            log.info(ret);
        }

        return ret;
    }

    native Object invoke0(Object proxy, Method method, Object[] args);
}