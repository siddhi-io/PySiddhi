from PySiddhi3 import SiddhiLoader

_event_printer_proxy = SiddhiLoader._loadType("org.wso2.siddhi.pythonapi.proxy.core.util.EventPrinterProxy")


def PrintEvent(timestamp, inEvents, outEvents):
    '''
    Prints Stream Event to Log
    :param timestamp:
    :param inEvents:
    :param outEvents:
    :return:
    '''

    if inEvents is not None:
      inEvents = [event._event_proxy for event in inEvents]

    if outEvents is not None:
      outEvents = [event._event_proxy for event in outEvents]
    _event_printer_proxy.printEvent(timestamp,inEvents,outEvents)


    # NOTE: We are unable to call org.wso2.siddhi.core.util.EventPrinter.print directly because print is a keyword of python