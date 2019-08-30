import json
import sys
import os
import requests
import logging
from logging.handlers import RotatingFileHandler

class ArmisClient(object):
    def __init__(self, cx_host, apikey):
        self.url_base = 'https://{0}/api/v1'.format(cx_host)
        self.apikey = apikey
        self.token = None

    def _utc_convert(self, xtimestamp):
        pass

    def _url(self, *args):
        return os.path.join(self.url_base, *args)

    def _authenticate(self):
        auth_url = self._url('access_token/')
        auth_res = requests.post(auth_url, data = {'secret_key':self.apikey}).json()
        self.access_token = auth_res['data']['access_token']
        utc_token_timeout = auth_res['data']['expiration_utc']

    def _get(self, url):
        if self.token is None:
            self._authenticate()

        print(url)
        
        get_headers = {'Authorization': self.access_token} 
        get_res = requests.get(url, headers=get_headers)
        if get_res.status_code > 399:
            print("Error Code:")
            print(get_res.status_code)
            print("")

        return(get_res)
    
    def _patch(self, url, patch_data):
        if self.token is None:
            self._authenticate()
        
        patch_headers = {'Authorization': self.access_token,
                        'accept': 'application/json',
                        'content-type': 'application/x-www-form-urlencoded'
                        }

        get_patch = requests.patch(url, headers=patch_headers, data=patch_data)
        
        if get_patch.status_code == 400:
            return("Alert Already Closed")

        if get_patch.status_code > 399:
            print("Error Code:")
            print(get_patch.status_code)
            print("")
        
        return(get_patch)


    def auth_test(self):
        '''Do a quick auth check for your api key'''
        test_url = self._url('access_token/')
        print('Connecting to: ' + test_url)
        res = requests.post(test_url, data = {'secret_key':self.apikey})
        if res.status_code == 200:
            print('Api Connectivity is good')
        else:
            print('Api returned error:' + str(res.status_code))
    
    def get_device_id(self, device_id): 
        ''' Returns json given a device id '''
        device_id = str(device_id)
        device_url = 'devices/?id=%s' % device_id
        id_response = (self._get(self._url(device_url))).json()
        return(id_response)
    
    def resolve_by_id(self, device_id):
        ''' Resolves Armis API given alert id '''
        device_id = str(device_id)
        resolve_api = 'alerts/%s/' % device_id
        resolve_status = {'status': 'RESOLVED'}
        resolve_url = self._url(resolve_api)
        resolve_return = self._patch(resolve_url, resolve_status)
        return(resolve_return)
