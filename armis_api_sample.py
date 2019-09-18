#!/usr/bin/env python3
'''Example code to access the armisAPI/ Client'''
import json
from ArmisClient import ArmisClient

#CX_HOSTNAME = 'HOSTNAME of your instance ie xxxxxxxxxx.armis.com'
CX_HOSTNAME = 'xxxxxxxxxx.armis.com'

#APIKEY = 'You can find your API key under settings then click API Management '
APIKEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

DEVICE_ID_TO_FIND = 'Some Id ID to find'
RESOLVE_ALERT = 'Your Alert to Close'

def main():
    ''' Uncomment the functions as needed '''
    armis_api = ArmisClient(CX_HOSTNAME, APIKEY)

    #To test your api key
    #armis_api.auth_test()

    #Pull Devices By ID
    #device_json = armis_api.get_device_id(DEVICE_ID_TO_FIND)
    #print(json.dumps(device_json, indent=4))

    #Find All Unhandled Alerts
    #open_alerts = armis_api.unhandled_alerts()
    #print(json.dumps(open_alerts, indent=4))

    #Resolve an alert
    #resolve_details = armis_api.resolve_by_id(RESOLVE_ALERT)
    #print(resolve_details)

    #Search Anything
    # The query is converted to a url in the class, just copy & paste the AQL
    #aql_query('in:devices boundary:ICS', count=10)
    #aql_query = 'in:activity timeFrame:"7 Days" type:"Risk Level Increased"'
    #query_anything = armis_api.search_aql(aql_query, count=10)
    #print(json.dumps(query_anything, indent=4, sort_keys=True))

    #Add device info:
    # Add headers to the file as follows: 'id, mac, key, value'
    # Key fields above are
    #   "CATEGORY",
    #   "IP",
    #   "MODEL",
    #   "NAME",
    #   "OS",
    #   "OS_VERSION",
    #   "TAG",
    #   "TYPE",
    #   "USER"
    #send_csv_api = armis_api.send_csv('<your csv file here')
    #print(send_csv_api)
    
if __name__ == "__main__":
    main()
