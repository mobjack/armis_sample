'''Client to manage access to Armis API'''

import os
import sys
import codecs
from urllib import parse
from time import time
import requests
from requests.exceptions import ConnectionError, ReadTimeout, ConnectTimeout # pylint: disable=redefined-builtin

# pylint: disable=invalid-name

class ArmisClient():
    '''Handle access to the API and keep track of the tokens '''
    def __init__(self, cx_host, apikey):
        self.url_base = 'https://{0}/api/v1'.format(cx_host)
        self.cx_host = cx_host
        self.apikey = apikey
        self.token = None
        self.access_token = None
        self.init_time = int(time())
        self.token_endtime = self.init_time + 240 # 4 Minutes after init

    def _url(self, *args):
        return os.path.join(self.url_base, *args)

    def _authenticate(self):
        # Re auth if the token has timed out or has not been authenticated before
        if self.token is None or int(time()) > self.token_endtime:
            auth_url = self._url('access_token/')
            try: # Try to connect & verify domain name and access to the enviornment
                auth_res = requests.post(auth_url, data={'secret_key':self.apikey}).json()
            except (ConnectionError, ReadTimeout, ConnectTimeout):
                print('ERROR')
                print('Unable to resolve or connect check CX_HOSTNAME=%s is correct' % self.cx_host)
                print('Exit...')
                sys.exit()
            # Now that we can coonect check the key
            if auth_res['success'] is False:
                self.auth_test()
                sys.exit(1)
            else: # Set the token now that everything looks good
                self.access_token = auth_res['data']['access_token']


    def _get(self, url): # pylint: disable=too-many-locals
        ''' Internal GET function with specific URL needed.'''
        self._authenticate()

        first_url = url + '&from=1'
        get_headers = {'Authorization': self.access_token}
        get_res = requests.get(first_url, headers=get_headers)
        if get_res.status_code > 399:
            print("Error Code:")
            print(get_res.status_code)
            print("")

        responses = []
        results = get_res.json()
        r_total = results['data']['total']
        r_count = results['data']['count']

        for x_result in results['data']['results']:
            responses.append(x_result)

        if r_total > r_count:

            r_next = results['data']['next']
            last_page = r_total - r_count # last page to pull

            dupfound = 0
            while True:
                p_url = url + '&from=%s' % str(r_next)
                n_res = requests.get(p_url, headers=get_headers)
                fetch_json = n_res.json()

                # Verify pagination, this is to ensure we get all the proper results
                for one_result in fetch_json['data']['results']:
                    if one_result in responses:
                        dupfound += 1
                        continue
                responses.append(one_result) # pylint: disable=undefined-loop-variable

                if fetch_json['data']['next'] != last_page:
                    r_next = fetch_json['data']['next']
                else:
                    r_next = last_page

                # Finish Up we have a good set of entries
                if r_total <= len(responses):
                    break

        return responses

    def _post_csv(self, url, csv_data):
        self._authenticate()
        print(url)
        file_csv = codecs.open(csv_data, 'r', 'UTF-8')
        file_data=file_csv.read() # pylint: disable=unused-variable

        params = {'mimetype':'text/csv'}
        post_headers = {'Authorization': self.access_token}
        post_res = requests.post(url, headers=post_headers,
                                 params=params, files={'mycsv.csv':file_csv}).json()

        if post_res > 399:
            print("Errors")
        return post_res

    def _patch(self, url, patch_data):
        self._authenticate()

        patch_headers = {'Authorization': self.access_token,
                         'accept': 'application/json',
                         'content-type': 'application/x-www-form-urlencoded'
                        }

        get_patch = requests.patch(url, headers=patch_headers, data=patch_data)
        if get_patch.status_code > 399:
            print("Error Code:", str(get_patch.status_code))
            print(get_patch.status_code)
            print("")

        return get_patch

    def auth_test(self):
        '''Do a quick auth check for your api key'''
        test_url = self._url('access_token/')
        print('Connecting to: ' + test_url)
        res = requests.post(test_url, data={'secret_key':self.apikey})
        if res.status_code == 200:
            print('Api Connectivity is good')
        else:
            print('ERROR: Api returned error:' + str(res.status_code))

    def get_device_id(self, device_id):
        ''' Returns json given a device id '''
        device_id = str(device_id)
        device_url = 'devices/?id=%s' % device_id
        id_response = (self._get(self._url(device_url))).json() # pylint: disable=no-member
        return id_response

    def unhandled_alerts(self):
        ''' Returns all unhandled alerts '''
        handle_url = self._url('search/?aql=in%3Aalerts%20status%3AUnhandled&include_total=true')
        handle_response = self._get(handle_url).json() # pylint: disable=no-member
        return handle_response

    def resolve_by_id(self, device_id):
        ''' Resolves Armis API given alert id '''
        device_id = str(device_id)
        resolve_api = 'alerts/%s/' % device_id
        resolve_status = {'status': 'RESOLVED'}
        resolve_url = self._url(resolve_api)
        resolve_return = self._patch(resolve_url, resolve_status)
        return resolve_return

    def search_aql(self, aql_query, count=20):
        ''' Search any data via Armis Query Language (AQL) '''
        search_params = '&length={0}&include_total=true'.format(str(count))
        aql_query = parse.quote(aql_query) # Fix the aql for url
        search_url = self._url('search/?aql=' + aql_query + search_params)
        search_response = self._get(search_url)
        return search_response

    def send_csv(self, csv_path):
        ''' Upload a device CSV '''
        csv_url = self._url('devices', 'csv/')
        csv_resp = self._post_csv(csv_url, csv_path)
        return csv_resp
