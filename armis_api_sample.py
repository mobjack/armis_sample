#!/usr/bin/env python3
import json
from armisClient import ArmisClient


#cx_hostname = 'HOSTNAME of your instance ie customer_name.armis.net'
cx_hostname = 'customer_name.armis.net'
#apikey='You can find your API key under settings then click API Management '
apikey='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

device_to_find_id = 'Some Id ID to find'
resolve_alert = 'Your Alert to Close'


def main():
    armis_api = ArmisClient(cx_hostname, apikey)

    '''To test your api key:'''
    armis_api.auth_test()

    '''Pull Devices By ID'''
    #device_json = armis_api.get_device_id(device_to_find_id)
    #print(json.dumps(device_json, indent=4))

    ''' Resolve an alert '''
    #resolve_details = armis_api.resolve_by_id(resolve_alert)
    #print(resolve_details)


if __name__ == "__main__":
    main()