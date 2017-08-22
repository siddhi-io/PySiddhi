import requests
class RestClient(object):
    '''
    REST Client used internally to communicate with REST server
    '''
    def __init__(self, base_url):
        '''
        Instantiate Rest Client
        :param base_url: root url used
        '''
        self.base_url = base_url

    def _sendGetRequest(self, sub_url, params=None):
        '''
        Sends a GET Request to Server 
        :param sub_url: endpoint url which is to be appended to base url
        :param params: get parameters
        :return: 
        '''
        headers = {'content-type': 'text/plain'}
        resp = requests.get(self.base_url + sub_url, params=params, headers = headers)
        return resp

    def _sendPostRequest(self, sub_url, data=None, params = None, files=None, headers=None):
        '''
        Sends a POST Request to server
        :param sub_url: endpoint url which is to be appended to base url
        :param data: Payload data sent
        :param params: URL Parameters
        :param files: File Uploads
        :param headers: Custom headers
        :return: 
        '''
        resp = requests.post(self.base_url + sub_url, params=params, data=data, headers = headers,files=files)
        return resp

    def _sendPutRequest(self, sub_url, data=None, params=None, files=None, headers=None):
        '''
        Sends a PUT Request to server
        :param sub_url: endpoint url which is to be appended to base url
        :param data: Payload data sent
        :param params: URL Parameters
        :param files: File Uploads
        :param headers: Custom headers
        :return: 
        '''
        resp = requests.put(self.base_url + sub_url, params=params, files=files ,data=data, headers=headers)
        return resp

    def _sendDeleteRequest(self, sub_url,params = None):
        '''
        Sends a DELETE Request to server
        :param sub_url: endpoint url which is to be appended to base url
        :param params: URL Parameters
        :return: 
        '''
        headers = {'content-type': 'text/plain'}
        resp = requests.delete(self.base_url + sub_url, params=params, headers = headers)
        return resp