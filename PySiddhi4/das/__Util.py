def encodeField(value, encode_function=str):
    '''
    Encodes a field value using encode_function
    :param value: 
    :param encode_function: 
    :return: 
    '''
    if value is None:
        return None
    return encode_function(value)

def decodeField(value, decode_function):
    '''
    Decodes a field value using given decode_function
    :param value: 
    :param decode_function: 
    :return: 
    '''
    if value is None:
        return None
    return decode_function(value)


def decodeObject(jsonObject,target, decodeMap):
    '''
    Decodes a JSON Object and assigns attributes to target.
    :param jsonObject: 
    :param target: 
    :param decodeMap: 
    :return: 
    '''
    for (key,value) in jsonObject.items():
        setattr(target, key,decodeField(value, decodeMap[key]))
    return target